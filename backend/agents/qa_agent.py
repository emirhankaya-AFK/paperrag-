from typing import Dict, Any, List
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService

class QAAgent:
    def __init__(self, llm_service: LLMService, rag_service: RAGService):
        self.llm = llm_service
        self.rag = rag_service

    def answer_question(self, paper_id: str, question: str) -> Dict[str, Any]:
        """
        Answers a research question about a specific paper using indexed sections.
        """
        # Retrieve relative chunks
        chunks = self.rag.query_paper(paper_id=paper_id, query_text=question, n_results=4)
        
        if not chunks:
            return {
                "answer": "Not discussed in this paper (No indexed sections found).",
                "sources": []
            }
            
        # Format the context block
        context_parts = []
        sources = []
        for i, c in enumerate(chunks):
            sec_name = c["metadata"].get("section_type", "unknown")
            text_chunk = c["text"]
            context_parts.append(f"--- Chunk {i+1} (Section: {sec_name}) ---\n{text_chunk}")
            sources.append({
                "section": sec_name,
                "score": float(c["score"]),
                "snippet": text_chunk[:150] + "..."
            })
            
        context = "\n\n".join(context_parts)
        
        variables = {
            "context": context,
            "question": question
        }
        
        answer = self.llm.generate_text("qa", variables)
        
        # Format citations on the bottom if found
        return {
            "answer": answer,
            "sources": sources
        }
