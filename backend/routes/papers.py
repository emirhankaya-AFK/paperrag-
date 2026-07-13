import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List, Dict, Any

from ..config import settings
from ..db import save_paper, list_papers, get_paper, delete_paper, save_extraction
from ..services.pdf_service import PDFService
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService
from ..agents.extraction_agent import ExtractionAgent

router = APIRouter(prefix="/papers", tags=["papers"])

# Initialize services/agents for local use
llm_service = LLMService()
rag_service = RAGService(llm_service)
extraction_agent = ExtractionAgent(llm_service)

def process_paper_background(paper_id: str, file_path: str, title: str):
    """
    Process PDF in the background: parse text, extract structured data, index in ChromaDB.
    """
    try:
        # 1. Parse text
        parsed_data = PDFService.extract_structured_text(file_path)
        
        # 2. Extract structured fields using LLM Agent
        ext_result = extraction_agent.extract_paper_data(parsed_data["full_text"], title)
        
        # 3. Index text chunks in ChromaDB RAG
        metadata = {
            "title": ext_result.title,
            "authors": [a.strip() for a in ext_result.authors.split(",")],
            "year": parsed_data["references"][0]["year"] if parsed_data["references"] else 2024,
            "topic": "General"
        }
        rag_service.index_paper(paper_id, parsed_data, metadata)
        
        # 4. Save paper metadata in DB
        paper_record = {
            "id": paper_id,
            "title": ext_result.title,
            "authors": metadata["authors"],
            "pub_date": str(metadata["year"]),
            "venue": "Unknown Venue",
            "abstract": parsed_data["sections"].get("abstract", "")[:2000],
            "file_path": file_path,
            "keywords": ["Research"]
        }
        save_paper(paper_record)
        
        # 5. Save structured extraction in DB
        save_extraction(paper_id, ext_result.model_dump())
        print(f"Background processing completed for paper {paper_id}")
    except Exception as e:
        print(f"Error processing paper {paper_id}: {e}")

@router.post("/upload")
async def upload_paper(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    paper_id = str(uuid.uuid4())
    safe_filename = f"{paper_id}.pdf"
    dest_path = UPLOAD_DIR = settings.UPLOAD_DIR / safe_filename
    
    # Save file to upload directory
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Trigger background parsing
    background_tasks.add_task(
        process_paper_background,
        paper_id,
        str(dest_path),
        file.filename
    )
    
    return {
        "message": "Paper uploaded successfully and is being processed in the background.",
        "paper_id": paper_id
    }

@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_papers():
    return list_papers()

@router.get("/{paper_id}")
async def get_single_paper(paper_id: str):
    paper = get_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")
    return paper

@router.delete("/{paper_id}")
async def remove_paper(paper_id: str):
    paper = get_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")
        
    # Delete PDF file
    pdf_path = Path(paper["file_path"])
    if pdf_path.exists():
        pdf_path.unlink()
        
    # Delete SQLite metadata
    delete_paper(paper_id)
    # Delete ChromaDB index
    rag_service.delete_paper_index(paper_id)
    
    return {"message": f"Paper {paper_id} deleted successfully."}
