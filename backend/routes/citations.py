from fastapi import APIRouter, HTTPException
from ..db import get_paper
from ..services.llm_service import LLMService
from ..services.pdf_service import PDFService
from ..services.citation_service import CitationService
from ..services.visualization import CitationVisualizationService
from ..agents.citation_agent import CitationAgent

router = APIRouter(prefix="/citations", tags=["citations"])

llm_service = LLMService()
citation_service = CitationService()
citation_agent = CitationAgent(llm_service, citation_service)

@router.get("/{paper_id}/network")
async def get_citation_network(paper_id: str):
    paper = get_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")
        
    parsed = PDFService.extract_structured_text(paper["file_path"])
    network = citation_agent.analyze_citations(paper_id, paper["title"], parsed["references"])
    
    # Generate visualization
    # We parse the citing and referenced lists
    citations = [{"title": title} for title in network.cited_by]
    references = [{"title": ref.title if ref.title else ref.raw_text} for ref in network.references]
    
    fig = CitationVisualizationService.generate_network_graph(paper["title"], citations, references)
    
    return {
        "network": network.model_dump(),
        "graph_json": fig.to_json()
    }

@router.get("/{paper_id}/related")
async def get_related_papers(paper_id: str):
    paper = get_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")
        
    recommendations = citation_agent.get_recommendations(paper["title"])
    return recommendations
