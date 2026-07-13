import pytest
from pathlib import Path
from .generate_test_pdf import create_sample_pdf
from backend.services.pdf_service import PDFService
from backend.services.llm_service import LLMService
from backend.services.citation_service import CitationService
from backend.agents.citation_agent import CitationAgent

@pytest.fixture(scope="module")
def sample_pdf():
    pdf_path = Path(__file__).parent / "temp_test_paper_citations.pdf"
    create_sample_pdf(str(pdf_path))
    yield str(pdf_path)
    if pdf_path.exists():
        pdf_path.unlink()

def test_citations_processing(sample_pdf):
    parsed = PDFService.extract_structured_text(sample_pdf)
    assert len(parsed["references"]) > 0
    
    # Assert specific references are parsed
    ref1 = parsed["references"][0]
    assert ref1["year"] == 2016
    assert "Deep residual learning" in ref1["title"]
    
    llm = LLMService()
    cit_service = CitationService()
    agent = CitationAgent(llm, cit_service)
    
    network = agent.analyze_citations("test_paper_cit_id", "Attention Is All You Need", parsed["references"])
    assert network.paper_id == "test_paper_cit_id"
    assert len(network.references) > 0
    assert len(network.cited_by) > 0
