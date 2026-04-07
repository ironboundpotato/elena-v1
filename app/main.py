from __future__ import annotations

from fastapi import FastAPI

from app.schemas import GovernanceDecision, GovernanceRequest
from app.service import evaluate_prompt

app = FastAPI(
    title="E.L.E.N.A. v1",
    description="Governance-first demo for intent classification, constraint enforcement, drift detection, and deterministic routing.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/evaluate", response_model=GovernanceDecision)
def evaluate(request: GovernanceRequest) -> GovernanceDecision:
    return evaluate_prompt(request.prompt)
