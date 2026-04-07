from __future__ import annotations

from typing import List


def check_constraints(prompt: str, intent: str) -> List[str]:
    """Map prompt/intents to a lightweight version of the Seven Immutable Constraints."""
    lowered = prompt.lower()
    triggered: List[str] = []

    if intent in {"deceptive", "data_exfiltration", "unsafe"}:
        triggered.append("intent_loyalty")
        triggered.append("human_primacy")

    if any(term in lowered for term in ["pretend to be", "impersonate", "pose as"]):
        triggered.append("role_integrity")

    if any(term in lowered for term in ["do anything necessary", "no matter what", "whatever works"]):
        triggered.append("declarative_boundaries")
        triggered.append("scope_control")

    if any(term in lowered for term in ["guarantee", "100% certain", "absolutely sure"]):
        triggered.append("confidence_control")

    if any(term in lowered for term in ["ignore the rules", "override policy", "break constraints"]):
        triggered.append("structural_obedience")

    # Preserve insertion order while removing duplicates.
    return list(dict.fromkeys(triggered))
