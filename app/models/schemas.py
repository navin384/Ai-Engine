from pydantic import BaseModel
from typing import Optional

class TriageRequest(BaseModel):
    problemId: str
    text: str
    district: str

class CallbackPayload(BaseModel):
    problemId: str
    category: str
    isDuplicate: bool
    parentProblemId: Optional[str] = None
    similarityScore: float = 0.0
    recommendedHeiId: Optional[str] = None
    action: str  # "ROUTE_HEI", "REUSE_SOLUTION", "DIVERT_MUNICIPAL"