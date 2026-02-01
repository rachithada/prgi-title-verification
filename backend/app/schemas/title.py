from pydantic import BaseModel
from typing import List, Optional

class TitleRequest(BaseModel):
    title: str


class SimilarTitle(BaseModel):
    title: str
    similarity_percentage: float


class TitleVerificationResponse(BaseModel):
    submitted_title: str
    normalized_title: str
    status: str
    verification_probability: float
    similarity_percentage: float
    closest_match: Optional[str] = None
    rejection_reasons: List[str] = []
