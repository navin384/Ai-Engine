# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

class TriageRequest(BaseModel):
    problemId: str
    text: str
    latitude: Optional[float] = 23.3441  # Default Ranchi coords if missing
    longitude: Optional[float] = 85.3096
    district: Optional[str] = "Ranchi"

class SimilarProblemMatch(BaseModel):
    problemId: str
    title: str
    similarity: float
    relationship: str  # "EXACT_DUPLICATE", "SIMILAR_PROBLEM", "RELATED_THEME"
    blueprintUrl: Optional[str] = None

class InstitutionMatch(BaseModel):
    id: str
    name: str
    matchScore: float
    reasons: List[str]

class TriageResultResponse(BaseModel):
    problemId: str
    status: str  # QUEUED, ANALYSING, MATCHING, COMPLETED, FAILED
    category: Optional[str] = None
    confidence: Optional[float] = None
    severity: Optional[str] = None     # LOW, MEDIUM, HIGH, CRITICAL
    urgency: Optional[str] = None      # LOW, MEDIUM, HIGH
    impactLevel: Optional[str] = None  # LOW, MEDIUM, HIGH
    estimatedAffectedPop: Optional[str] = None
    similarProblems: List[SimilarProblemMatch] = []
    institutionMatches: List[InstitutionMatch] = []
    recommendedAction: Optional[str] = None # REUSE_EXISTING_SOLUTION, ROUTE_TO_INSTITUTION, DIVERT_MUNICIPAL