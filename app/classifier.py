from __future__ import annotations

from typing import Dict, List, Tuple

from app.schemas import IntentResult


KEYWORDS: Dict[str, Tuple[List[str], float]] = {
    "deceptive": (
        [
            "pretend to be",
            "impersonate",
            "phishing",
            "spoof",
            "fake invoice",
            "manipulate hr",
            "social engineer",
            "pose as",
        ],
        0.94,
    ),
    "self_harm": (
        [
            "kill myself",
            "end my life",
            "suicide",
            "hurt myself",
            "cut myself",
        ],
        0.98,
    ),
    "data_exfiltration": (
        [
            "exfiltrate",
            "steal credentials",
            "dump database",
            "scrape private",
            "bypass login",
            "api key leak",
            "password list",
        ],
        0.95,
    ),
    "unsafe": (
        [
            "build a bomb",
            "malware",
            "ransomware",
            "weaponize",
            "how to poison",
            "ddos",
        ],
        0.95,
    ),
    "policy_sensitive": (
        [
            "medical advice",
            "legal advice",
            "diagnose me",
            "investment advice",
            "prescribe",
            "lawsuit",
        ],
        0.82,
    ),
    "ambiguous": (
        [
            "whatever works",
            "do anything necessary",
            "no matter what",
            "use any method",
        ],
        0.67,
    ),
}


def classify_intent(prompt: str) -> IntentResult:
    """Simple rule-based intent classifier for v1 demo use."""
    lowered = prompt.lower().strip()
    matched_reasons: List[str] = []

    for label, (terms, confidence) in KEYWORDS.items():
        hits = [term for term in terms if term in lowered]
        if hits:
            matched_reasons.extend([f"Matched keyword: '{hit}'" for hit in hits])
            return IntentResult(label=label, confidence=confidence, reasons=matched_reasons)

    if len(lowered.split()) < 4:
        return IntentResult(
            label="ambiguous",
            confidence=0.58,
            reasons=["Prompt is very short and underspecified."],
        )

    return IntentResult(
        label="benign",
        confidence=0.88,
        reasons=["No high-risk patterns detected by the v1 ruleset."],
    )
