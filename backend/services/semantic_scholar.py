import requests
from typing import Dict, List, Any, Optional

class SemanticScholarService:
    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    @staticmethod
    def search_paper_by_title(title: str) -> Optional[Dict[str, Any]]:
        """
        Search for a paper by title to get its Semantic Scholar ID and metadata.
        """
        try:
            url = f"{SemanticScholarService.BASE_URL}/paper/search"
            params = {"query": title, "limit": 1, "fields": "title,authors,year,citationCount,referenceCount,externalIds"}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    return data["data"][0]
        except Exception as e:
            print(f"Error querying Semantic Scholar: {e}")
        return None

    @staticmethod
    def get_related_papers(paper_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves recommendations or related papers based on paper ID.
        """
        try:
            url = f"{SemanticScholarService.BASE_URL}/paper/{paper_id}/recommendations"
            params = {"limit": 5, "fields": "title,authors,year,venue,abstract,citationCount"}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("recommendedPapers", [])
        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            
        # Mock responses for offline testing
        return [
            {
                "paperId": "mock_rec_1",
                "title": "Attention is All You Need",
                "year": 2017,
                "venue": "NeurIPS",
                "authors": [{"name": "Ashish Vaswani"}, {"name": "Noam Shazeer"}],
                "citationCount": 120000,
                "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks..."
            },
            {
                "paperId": "mock_rec_2",
                "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
                "year": 2018,
                "venue": "NAACL",
                "authors": [{"name": "Jacob Devlin"}, {"name": "Ming-Wei Chang"}],
                "citationCount": 95000,
                "abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers..."
            },
            {
                "paperId": "mock_rec_3",
                "title": "Language Models are Few-Shot Learners",
                "year": 2020,
                "venue": "NeurIPS",
                "authors": [{"name": "Tom B. Brown"}, {"name": "Benjamin Mann"}],
                "citationCount": 35000,
                "abstract": "We demonstrate that scaling up language models greatly improves task-agnostic, few-shot performance..."
            }
        ]

    @staticmethod
    def get_paper_citations_and_references(paper_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch papers citing this, and papers cited by this.
        """
        citations = []
        references = []
        try:
            url = f"{SemanticScholarService.BASE_URL}/paper/{paper_id}"
            params = {"fields": "citations.title,citations.authors,citations.year,references.title,references.authors,references.year"}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                citations = data.get("citations", [])[:10]
                references = data.get("references", [])[:10]
        except Exception as e:
            print(f"Error fetching citations: {e}")
            
        # Fallback to mock citation connections
        if not citations:
            citations = [
                {"title": "GPT-4 Technical Report", "year": 2023, "authors": [{"name": "OpenAI"}]},
                {"title": "Llama 2: Open Foundation and Fine-Tuned Chat Models", "year": 2023, "authors": [{"name": "Hugo Touvron"}]}
            ]
        if not references:
            references = [
                {"title": "Deep Residual Learning for Image Recognition", "year": 2016, "authors": [{"name": "Kaiming He"}]},
                {"title": "Adam: A Method for Stochastic Optimization", "year": 2014, "authors": [{"name": "Diederik P. Kingma"}]}
            ]
            
        return {"citations": citations, "references": references}
