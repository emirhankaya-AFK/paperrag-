from pydantic import BaseModel
from typing import List, Optional

class Reference(BaseModel):
    raw_text: str
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    year: Optional[int] = None

class CitationNetwork(BaseModel):
    paper_id: str
    references: List[Reference]
    cited_by: List[str] = []  # External papers citing this one
    cites: List[str] = []     # External papers this one cites
