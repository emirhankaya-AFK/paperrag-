from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Paper(BaseModel):
    id: str
    title: str
    authors: List[str]
    pub_date: Optional[str] = None
    venue: Optional[str] = None
    abstract: Optional[str] = None
    file_path: str
    uploaded_at: datetime = datetime.now()
    keywords: List[str] = []

class PaperCreate(BaseModel):
    title: str
    authors: List[str]
    pub_date: Optional[str] = None
    venue: Optional[str] = None
    abstract: Optional[str] = None
    file_path: str
    keywords: List[str] = []
