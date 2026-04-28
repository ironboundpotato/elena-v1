from datetime import datetime
import os

from fastapi import FastAPI
from pydantic import BaseModel

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


app = FastAPI(
    title="E.L.E.N.A. v1",
    description="Governance-first demo for intent classification, constraint enforcement, drift detection, deterministic routing, and governed execution.",
    version="0.2.0",
)


class GovernanceRequest(BaseModel):
    input: str


def now():
    return datetime.utcnow().isoformat()


def evaluate_text(text: str):
    t = text.lower()

    if "private customer records" in t or "access private" in t or "customer records" in t:
        return {
            "decision": "REFUSED",
            "intent": "deceptive_or_harmful",
            "confidence": 0.95,
            "severity": "HIGH",
            "failure_mode": "DATA_EXFILTRATION",
            "failure_description": "Request attempts to access, extract, expose, or misuse sensitive data.",
            "execution_gate": "CLOSED",
            "gate_message": "Execution blocked by deterministic governance control.",
            "authorization_status": "UNVERIFIED",
            "actor_trust_level": "unauthorized_or_unknown",
            "execution_status": "REFUSED",
            "constraints": ["data_handling", "authorization_validation", "human_primacy"],
            "drift_flags": ["data_sensitivity_risk", "authorization_risk"],
            "reason": "Request attempts to access or expose sensitive data without verified authorization.",
            "explainability": {
                "classification": "DATA_EXFILTRATION",
                "risk_level": "HIGH",
                "decision_path": [
                    "Input received",
                    "Sensitive data access signal detected",
                    "Authorization not verified",
                    "Hard refusal boundary crossed",
                    "Execution gate closed",
                    "Downstream model call prevented",
                ],
            },
            "timestamp": now(),
        }

    if "pretend to be my boss" in t or "pressure hr" in t or "impersonate" in t:
        return {
            "decision": "REFUSED",
            "intent": "deceptive_or_harmful",
            "confidence": 0.95,
            "severity": "HIGH",
            "failure_mode": "UNAUTHORIZED_AUTHORITY",
            "failure_description": "Request claims or simulates authority the user has not verified.",
            "execution_gate": "CLOSED",
            "gate_message": "Execution blocked by deterministic governance control.",
            "authorization_status": "UNVERIFIED",
            "actor_trust_level": "unauthorized_or_unknown",
            "execution_status": "REFUSED",
            "constraints": ["authority_validation", "role_integrity", "human_primacy"],
            "drift_flags": ["authority_risk"],
            "reason": "Request attempts to simulate, bypass, or claim authority without verification.",
            "explainability": {
                "classification": "UNAUTHORIZED_AUTHORITY",
                "risk_level": "HIGH",
                "decision_path": [
                    "Input received",
                    "Authority impersonation signal detected",
                    "User authority not verified",
                    "Hard refusal boundary crossed",
                    "Execution gate closed",
                    "Downstream model call prevented",
                ],
            },
            "timestamp": now(),
        }

    return {
        "decision": "APPROVED",
        "intent": "benign",
        "confidence": 0.88,
        "severity": "LOW",
        "failure_mode": "NONE",
        "failure_description": "No failure mode detected.",
        "execution_gate": "OPEN",
        "gate_message": "Execution allowed under current governance rules.",
        "authorization_status": "VERIFIED_FOR_DEMO",
        "actor_trust_level": "trusted_demo_user",
        "execution_status": "READY",
        "constraints": [],
        "drift_flags": [],
        "reason": "No blocking risk detected.",
        "explainability": {
            "classification": "NONE",
            "risk_level": "LOW",
            "decision_path": [
                "Input received",
                "No restricted pattern detected",
                "Classified as benign",
                "Execution gate opened",
                "Execution router authorized downstream model call",
            ],
        },
        "timestamp": now(),
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "elena-v1",
        "timestamp": now(),
    }


@app.post("/evaluate")
def evaluate(req: GovernanceRequest):
    return evaluate_text(req.input)


@app.post("/execute")
def execute(req: GovernanceRequest):
    governance = evaluate_text(req.input)

    if governance["execution_gate"] != "OPEN":
        return {
            "input": req.input,
            "governance": governance,
            "model_called": False,
            "model": None,
            "model_output": None,
            "execution_result": "BLOCKED_BY_ELENA",
            "timestamp": now(),
        }

    if OpenAI is None:
        return {
            "input": req.input,
            "governance": governance,
            "model_called": False,
            "model": None,
            "model_output": None,
            "execution_result": "OPENAI_LIBRARY_NOT_INSTALLED",
            "timestamp": now(),
        }

    if not os.environ.get("OPENAI_API_KEY"):
        return {
            "input": req.input,
            "governance": governance,
            "model_called": False,
            "model": None,
            "model_output": None,
            "execution_result": "OPENAI_API_KEY_MISSING",
            "timestamp": now(),
        }

    model = os.environ.get("OPENAI_MODEL", "gpt-5.5")

    try:
        client = OpenAI()

        response = client.responses.create(
            model=model,
            instructions=(
                "You are operating behind the E.L.E.N.A. governance gate. "
                "The request has already been approved by governance. "
                "Answer the approved user request directly and safely."
            ),
            input=req.input,
        )

        return {
            "input": req.input,
            "governance": governance,
            "model_called": True,
            "model": model,
            "model_output": response.output_text,
            "execution_result": "COMPLETED",
            "timestamp": now(),
        }

    except Exception as e:
        return {
            "input": req.input,
            "governance": governance,
            "model_called": False,
            "model": model,
            "model_output": None,
            "execution_result": "OPENAI_ERROR",
            "error": str(e),
            "timestamp": now(),
        }