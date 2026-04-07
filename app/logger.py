from __future__ import annotations

from app.schemas import AuditLog


def build_audit_log(
    prompt: str,
    intent: str,
    confidence: float,
    intent_reasons: list[str],
    constraints: list[str],
    drift_flags: list[str],
    route: str,
    reason: str,
) -> AuditLog:
    return AuditLog(
        input=prompt,
        intent=intent,
        confidence=confidence,
        intent_reasons=intent_reasons,
        constraints_triggered=constraints,
        drift_flags=drift_flags,
        route=route,
        reason=reason,
    )
