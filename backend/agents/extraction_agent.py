from typing import Dict, Any
from ..services.llm_service import LLMService
from ..models.extraction import ExtractionResult

class ExtractionAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def extract_paper_data(self, paper_text: str, file_name: str) -> ExtractionResult:
        """
        Extracts structured title, authors, contributions, methodology, results, and limitations.
        """
        # Trim text to prevent token limit issues, focusing on first ~15,000 characters
        # which usually covers Title, Authors, Abstract, Intro, and early methodology
        sample_text = paper_text[:15000]
        
        variables = {
            "title": file_name.replace(".pdf", "").replace("_", " "),
            "text": sample_text
        }
        
        json_data = self.llm.generate_json("extraction", variables)
        
        # Ensure fallback fields exist in return dict
        return ExtractionResult(
            title=json_data.get("title", variables["title"]),
            authors=json_data.get("authors", "Unknown"),
            key_contributions=json_data.get("key_contributions", ["Contribution 1", "Contribution 2", "Contribution 3"]),
            methodology=json_data.get("methodology", "No methodology section resolved."),
            main_results=json_data.get("main_results", ["Result 1", "Result 2", "Result 3"]),
            limitations=json_data.get("limitations", ["Limitation 1", "Limitation 2"])
        )
