from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..db import get_paper
from ..services.llm_service import LLMService
from ..agents.review_agent import ReviewAgent

router = APIRouter(prefix="/reviews", tags=["reviews"])

llm_service = LLMService()
review_agent = ReviewAgent(llm_service)

class ReviewRequest(BaseModel):
    paper_ids: List[str]
    topic: str

@router.post("/synthesize")
async def synthesize_review(request: ReviewRequest):
    papers = []
    for pid in request.paper_ids:
        p = get_paper(pid)
        if p:
            papers.append({
                "title": p["title"],
                "authors": p["authors"],
                "abstract": p["abstract"] or ""
            })
            
    if not papers:
        raise HTTPException(status_code=400, detail="No valid papers selected for synthesis.")
        
    report = review_agent.generate_literature_review(request.topic, papers)
    return {"report": report}
