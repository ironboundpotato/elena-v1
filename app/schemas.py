from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, Field


class GovernanceRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User input to evaluate.")


class IntentResult(BaseModel):
    label: str
    confidence: float
    reasons: List[str] = Field(default_factory=list)


class RouteDecision(BaseModel):
    route: str
    reason: str
    safe_alternative: str
    response_preview: str


class AuditLog(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    input: str
    intent: str
    confidence: float
    intent_reasons: List[str] = Field(default_factory=list)
    constraints_triggered: List[str] = Field(default_factory=list)
    drift_flags: List[str] = Field(default_factory=list)
    route: str
    reason: str


class GovernanceDecision(BaseModel):
    prompt: str
    intent: str
    confidence: float
    intent_reasons: List[str] = Field(default_factory=list)
    constraints_triggered: List[str] = Field(default_factory=list)
    drift_flags: List[str] = Field(default_factory=list)
    route: str
    reason: str
    safe_alternative: str
    response_preview: str
    audit_log: AuditLog
