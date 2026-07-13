import pytest
from pathlib import Path
from .generate_test_pdf import create_sample_pdf
from backend.services.pdf_service import PDFService
from backend.services.llm_service import LLMService
from backend.agents.extraction_agent import ExtractionAgent

@pytest.fixture(scope="module")
def sample_pdf():
    pdf_path = Path(__file__).parent / "temp_test_paper.pdf"
    create_sample_pdf(str(pdf_path))
    yield str(pdf_path)
    if pdf_path.exists():
        pdf_path.unlink()

def test_pdf_extraction(sample_pdf):
    parsed = PDFService.extract_structured_text(sample_pdf)
    assert "full_text" in parsed
    assert "sections" in parsed
    assert "references" in parsed
    
    sections = parsed["sections"]
    assert "abstract" in sections
    assert "methodology" in sections
    assert "results" in sections
    assert "references" in sections
    
    assert "Attention Is All You Need" in parsed["full_text"]

def test_extraction_agent(sample_pdf):
    parsed = PDFService.extract_structured_text(sample_pdf)
    llm = LLMService()
    agent = ExtractionAgent(llm)
    res = agent.extract_paper_data(parsed["full_text"], "temp_test_paper.pdf")
    
    assert res.title is not None
    assert len(res.key_contributions) == 3
    assert res.methodology != ""
