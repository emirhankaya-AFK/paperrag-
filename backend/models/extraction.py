from pydantic import BaseModel
from typing import List

class ExtractionResult(BaseModel):
    title: str
    authors: str
    key_contributions: List[str]
    methodology: str
    main_results: List[str]
    limitations: List[str]
