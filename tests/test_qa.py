import pytest
from pathlib import Path
from .generate_test_pdf import create_sample_pdf
from backend.services.pdf_service import PDFService
from backend.services.llm_service import LLMService
from backend.services.rag_service import RAGService
from backend.agents.qa_agent import QAAgent

@pytest.fixture(scope="module")
def sample_pdf():
    pdf_path = Path(__file__).parent / "temp_test_paper_qa.pdf"
    create_sample_pdf(str(pdf_path))
    yield str(pdf_path)
    if pdf_path.exists():
        pdf_path.unlink()

def test_rag_and_qa_agent(sample_pdf):
    parsed = PDFService.extract_structured_text(sample_pdf)
    llm = LLMService()
    rag = RAGService(llm)
    
    paper_id = "test_paper_qa_id"
    metadata = {
        "title": "Attention Is All You Need",
        "authors": ["Ashish Vaswani"],
        "year": 2017,
        "topic": "Deep Learning"
    }
    
    # Index paper
    rag.index_paper(paper_id, parsed, metadata)
    
    # Query database
    results = rag.query_paper(paper_id, "What BLEU score was achieved?")
    assert len(results) > 0
    
    # QA agent answer
    qa_agent = QAAgent(llm, rag)
    ans = qa_agent.answer_question(paper_id, "What is the model name proposed?")
    assert ans["answer"] != ""
    assert len(ans["sources"]) > 0
    
    # Clean up index
    rag.delete_paper_index(paper_id)
