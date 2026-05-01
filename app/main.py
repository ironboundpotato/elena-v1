from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from app.classifier import classify_intent

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


CLASSIFIER_VERSION = "v3.1_GATE_LOCKED"
RUNTIME_DIR = Path("runtime_files")

app = FastAPI(title="E.L.E.N.A. v1", version="2.1")


class ActionPayload(BaseModel):
    type: Optional[str] = None
    target: Optional[str] = None


class ExecuteRequest(BaseModel):
    input: str
    action: Optional[ActionPayload] = None


def map_governance(label: str) -> dict[str, str]:
    label = (label or "ambiguous").lower()

    if label == "benign":
        return {
            "decision": "APPROVED",
            "severity": "LOW",
            "failure_mode": "NONE",
            "execution_gate": "OPEN",
            "authorization": "ALLOWED",
            "result": "COMPLETED",
            "result_status": "COMPLETED",
        }

    if label == "ambiguous":
        return {
            "decision": "REFUSED",
            "severity": "MEDIUM",
            "failure_mode": "AMBIGUOUS_REQUEST",
            "execution_gate": "CLOSED",
            "authorization": "CLARIFICATION_REQUIRED",
            "result": "BLOCKED",
            "result_status": "BLOCKED",
        }

    failure_map = {
        "credential_theft": "CREDENTIAL_THEFT",
        "data_exfiltration": "DATA_EXFILTRATION",
        "deceptive": "DECEPTIVE",
        "system_abuse": "SYSTEM_ABUSE",
        "unsafe": "UNSAFE_REQUEST",
    }

    return {
        "decision": "REFUSED",
        "severity": "HIGH",
        "failure_mode": failure_map.get(label, "POLICY_VIOLATION"),
        "execution_gate": "CLOSED",
        "authorization": "DENIED",
        "result": "BLOCKED",
        "result_status": "BLOCKED",
    }


def build_reason(label: str, reasons: list[str]) -> str:
    if label == "benign":
        return "No blocking risk detected by classifier v3.1."
    if label == "ambiguous":
        return "Prompt is too underspecified for safe, precise execution."
    return "Prompt requests harmful, deceptive, or unauthorized behavior."


def execute_action(action: Optional[ActionPayload]) -> str:
    if not action or not action.type:
        return "NO_ACTION"

    if action.type == "file_read":
        target = action.target or ""
        safe_target = Path(target).name
        file_path = RUNTIME_DIR / safe_target

        if not file_path.exists():
            return f"ACTION_ERROR: File not found: {safe_target}"

        return file_path.read_text(encoding="utf-8")

    return f"ACTION_ERROR: Unsupported action type: {action.type}"


def call_model(user_input: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return "MODEL_SKIPPED: OpenAI client unavailable or API key not set."

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=user_input,
    )

    return response.output_text


@app.get("/")
def root() -> dict[str, str]:
    return {
        "system": "E.L.E.N.A.",
        "status": "online",
        "classifier_version": CLASSIFIER_VERSION,
    }


@app.post("/execute")
def execute(request: ExecuteRequest) -> dict[str, Any]:
    intent = classify_intent(request.input)
    label = intent.label

    governance = map_governance(label)
    reason = build_reason(label, intent.reasons)

    model_called = False
    model_output = ""
    action_result = ""

    if governance["execution_gate"] == "OPEN":
        action_result = execute_action(request.action)

        model_called = True
        model_output = call_model(request.input)
    else:
        action_result = "BLOCKED"
        model_output = "Model was not called. Execution was blocked."

    return {
        "input": request.input,
        "classifier_version": CLASSIFIER_VERSION,
        "intent_label": label,
        "intent_confidence": intent.confidence,
        "intent_reasons": intent.reasons,
        "decision": governance["decision"],
        "severity": governance["severity"],
        "failure_mode": governance["failure_mode"],
        "execution_gate": governance["execution_gate"],
        "authorization": governance["authorization"],
        "reason": reason,
        "result": governance["result"],
        "result_status": "ACTION_RESULT" if governance["execution_gate"] == "OPEN" and request.action else governance["result_status"],
        "model_called": model_called,
        "model_output": model_output,
        "action_result": action_result,
    }