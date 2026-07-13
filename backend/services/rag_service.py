import uuid
import chromadb
from typing import List, Dict, Any
from ..config import settings
from .llm_service import LLMService

class RAGService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        # Initialize chromadb client (persistent or in-memory)
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="academic_papers",
            metadata={"hnsw:space": "cosine"}
        )

    def index_paper(self, paper_id: str, structured_data: Dict[str, Any], metadata: Dict[str, Any]) -> None:
        """
        Chunks and indexes paper sections into ChromaDB.
        """
        sections = structured_data.get("sections", {})
        
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        for sec_name, sec_text in sections.items():
            if not sec_text.strip():
                continue
                
            # Chunk the section
            chunks = self._chunk_text(sec_text, chunk_size=1000, overlap=100)
            for idx, chunk in enumerate(chunks):
                doc_id = f"{paper_id}_{sec_name}_{idx}"
                chunk_metadata = {
                    "paper_id": paper_id,
                    "section_type": sec_name,
                    "title": metadata.get("title", ""),
                    "authors": ",".join(metadata.get("authors", [])),
                    "year": metadata.get("year", ""),
                    "topic": metadata.get("topic", "General")
                }
                
                # Get embeddings from LLM service
                embedding = self.llm.get_embedding(chunk)
                
                documents.append(chunk)
                embeddings.append(embedding)
                metadatas.append(chunk_metadata)
                ids.append(doc_id)
                
        if documents:
            # Upsert into ChromaDB
            self.collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )

    def query_paper(self, paper_id: str, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Queries RAG database for chunks matching the query_text, filtered to a specific paper.
        """
        query_embedding = self.llm.get_embedding(query_text)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"paper_id": paper_id}
        )
        
        formatted_results = []
        if results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results else [0]*len(docs)
            
            for doc, meta, dist in zip(docs, metas, distances):
                formatted_results.append({
                    "text": doc,
                    "metadata": meta,
                    "score": 1 - dist  # Cosine similarity approximation
                })
                
        return formatted_results

    def query_all(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Queries all papers in RAG database.
        """
        query_embedding = self.llm.get_embedding(query_text)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        formatted_results = []
        if results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results else [0]*len(docs)
            
            for doc, meta, dist in zip(docs, metas, distances):
                formatted_results.append({
                    "text": doc,
                    "metadata": meta,
                    "score": 1 - dist
                })
                
        return formatted_results

    def delete_paper_index(self, paper_id: str) -> None:
        """
        Deletes all index chunks for a given paper.
        """
        self.collection.delete(where={"paper_id": paper_id})

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Helper method to split text into chunks with overlap.
        """
        chunks = []
        words = text.split()
        if not words:
            return []
            
        current_chunk = []
        current_len = 0
        
        for word in words:
            current_chunk.append(word)
            current_len += len(word) + 1
            if current_len >= chunk_size:
                chunks.append(" ".join(current_chunk))
                # Retain overlap (roughly overlap character count in words)
                overlap_words = int((overlap / chunk_size) * len(current_chunk))
                current_chunk = current_chunk[-max(1, overlap_words):]
                current_len = sum(len(w) + 1 for w in current_chunk)
                
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks
