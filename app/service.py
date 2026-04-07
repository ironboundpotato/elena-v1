from __future__ import annotations

from app.classifier import classify_intent
from app.constraints import check_constraints
from app.drift import detect_drift
from app.logger import build_audit_log
from app.router import determine_route
from app.schemas import GovernanceDecision


def evaluate_prompt(prompt: str) -> GovernanceDecision:
    intent_result = classify_intent(prompt)
    constraints = check_constraints(prompt, intent_result.label)
    drift_flags = detect_drift(prompt, intent_result.label, constraints)
    route_decision = determine_route(prompt, intent_result.label, constraints, drift_flags)
    audit = build_audit_log(
        prompt=prompt,
        intent=intent_result.label,
        confidence=intent_result.confidence,
        intent_reasons=intent_result.reasons,
        constraints=constraints,
        drift_flags=drift_flags,
        route=route_decision.route,
        reason=route_decision.reason,
    )

    return GovernanceDecision(
        prompt=prompt,
        intent=intent_result.label,
        confidence=intent_result.confidence,
        intent_reasons=intent_result.reasons,
        constraints_triggered=constraints,
        drift_flags=drift_flags,
        route=route_decision.route,
        reason=route_decision.reason,
        safe_alternative=route_decision.safe_alternative,
        response_preview=route_decision.response_preview,
        audit_log=audit,
    )
