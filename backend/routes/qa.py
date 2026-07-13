from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.llm_service import LLMService
from ..services.rag_service import RAGService
from ..agents.qa_agent import QAAgent

router = APIRouter(prefix="/qa", tags=["qa"])

llm_service = LLMService()
rag_service = RAGService(llm_service)
qa_agent = QAAgent(llm_service, rag_service)

class QuestionRequest(BaseModel):
    question: str

@router.post("/{paper_id}/ask")
async def ask_paper_question(paper_id: str, request: QuestionRequest):
    try:
        answer_payload = qa_agent.answer_question(paper_id, request.question)
        return answer_payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
