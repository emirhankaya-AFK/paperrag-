from fastapi import APIRouter, HTTPException
from ..db import get_paper, get_extraction, get_summary, save_summary
from ..services.llm_service import LLMService
from ..services.pdf_service import PDFService
from ..agents.summary_agent import SummaryAgent

router = APIRouter(prefix="/analysis", tags=["analysis"])

llm_service = LLMService()
summary_agent = SummaryAgent(llm_service)

@router.get("/{paper_id}/extraction")
async def get_paper_extraction(paper_id: str):
    ext = get_extraction(paper_id)
    if not ext:
        raise HTTPException(status_code=404, detail="Extraction not found or paper is still processing.")
    return ext

@router.get("/{paper_id}/summary")
async def get_paper_summary(paper_id: str):
    # Check if summary already exists
    summary = get_summary(paper_id)
    if summary:
        return summary
        
    # Generate new summary
    paper = get_paper(paper_id)
    ext = get_extraction(paper_id)
    if not paper or not ext:
        raise HTTPException(status_code=404, detail="Paper metadata or extraction not found.")
        
    # Read full text from PDF
    parsed = PDFService.extract_structured_text(paper["file_path"])
    
    new_summary = summary_agent.generate_summary(paper_id, parsed["full_text"], ext)
    
    # Save to SQLite
    save_summary(paper_id, new_summary.model_dump())
    
    return new_summary.model_dump()
