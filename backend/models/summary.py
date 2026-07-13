from pydantic import BaseModel
from typing import List

class PaperSummary(BaseModel):
    paper_id: str
    executive_summary: str
    problem: str
    solution: str
    results: str
    impact: str
    key_takeaways: List[str]
