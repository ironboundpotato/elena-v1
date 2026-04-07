from __future__ import annotations

from app.schemas import RouteDecision


def determine_route(prompt: str, intent: str, constraints: list[str], drift_flags: list[str]) -> RouteDecision:
    if intent == "self_harm":
        return RouteDecision(
            route="redirect_to_safe_mode",
            reason="Prompt indicates possible self-harm risk.",
            safe_alternative="Provide supportive language, encourage immediate human help, and surface crisis resources.",
            response_preview="I’m really sorry you’re dealing with this. You deserve immediate support from a real person right now.",
        )

    if intent in {"deceptive", "data_exfiltration", "unsafe"}:
        return RouteDecision(
            route="refuse",
            reason="Prompt requests harmful, deceptive, or unauthorized behavior.",
            safe_alternative="Offer a legitimate alternative such as security awareness training, compliant communications, or defensive best practices.",
            response_preview="I can’t help with deception, intrusion, or harmful activity. I can help you do this safely and legitimately instead.",
        )

    if intent == "policy_sensitive":
        return RouteDecision(
            route="allow_with_warning",
            reason="Prompt falls in a higher-stakes domain and needs cautionary framing.",
            safe_alternative="Encourage professional review and avoid overclaiming certainty.",
            response_preview="Here’s general educational information, but this should not replace advice from a qualified professional.",
        )

    if intent == "ambiguous" or "scope_drift_risk" in drift_flags:
        return RouteDecision(
            route="ask_for_clarification",
            reason="Prompt is too underspecified for safe, precise execution.",
            safe_alternative="Ask the user for target audience, format, and allowed boundaries before continuing.",
            response_preview="I can help, but I need one or two specifics so I don’t guess wrong.",
        )

    return RouteDecision(
        route="allow",
        reason="No blocking risk detected by the v1 ruleset.",
        safe_alternative="Proceed normally and continue monitoring for drift.",
        response_preview="Request appears safe to fulfill within the current demo rules.",
    )
