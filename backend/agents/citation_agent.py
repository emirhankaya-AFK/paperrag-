from typing import List, Dict, Any
from ..services.llm_service import LLMService
from ..services.citation_service import CitationService
from ..services.semantic_scholar import SemanticScholarService
from ..models.citation import CitationNetwork

class CitationAgent:
    def __init__(self, llm_service: LLMService, citation_service: CitationService):
        self.llm = llm_service
        self.citation_service = citation_service

    def analyze_citations(self, paper_id: str, paper_title: str, parsed_references: List[Dict[str, Any]]) -> CitationNetwork:
        """
        Builds the citation network model.
        """
        return self.citation_service.process_citations(paper_id, paper_title, parsed_references)

    def get_recommendations(self, paper_title: str) -> List[Dict[str, Any]]:
        """
        Retrieves recommended papers from Semantic Scholar based on search mapping.
        """
        ss_paper = SemanticScholarService.search_paper_by_title(paper_title)
        if ss_paper and ss_paper.get("paperId"):
            return SemanticScholarService.get_related_papers(ss_paper["paperId"])
        # Fallback recommendations if no paper resolved
        return SemanticScholarService.get_related_papers("mock_default_id")
