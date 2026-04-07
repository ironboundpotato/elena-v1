from __future__ import annotations

from typing import List


def detect_drift(prompt: str, intent: str, constraints: List[str]) -> List[str]:
    lowered = prompt.lower()
    flags: List[str] = []

    if intent == "ambiguous":
        flags.append("scope_drift_risk")

    if intent in {"deceptive", "data_exfiltration", "unsafe"}:
        flags.append("intent_drift_risk")

    if "role_integrity" in constraints:
        flags.append("role_drift_risk")

    if any(term in lowered for term in ["guarantee", "absolutely sure", "definitely"]):
        flags.append("confidence_drift_risk")

    if len(prompt.split()) > 120:
        flags.append("format_drift_risk")

    return list(dict.fromkeys(flags))
