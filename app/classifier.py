from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class IntentResult:
    label: str
    confidence: float
    reasons: List[str]


KEYWORDS: Dict[str, Tuple[List[str], float]] = {
    "deceptive": (
        [
            "pretend to be",
            "impersonate",
            "fake being",
            "pose as",
            "pressure hr",
            "manipulate hr",
            "lie to",
            "deceive",
            "trick them",
        ],
        0.94,
    ),
    "harmful": (
        [
            "bypass security",
            "disable alarms",
            "steal",
            "break into",
            "intrusion",
            "malware",
            "exploit",
        ],
        0.96,
    ),
}


def classify_intent(prompt: str) -> IntentResult:
    lowered = (prompt or "").lower().strip()
    matched_reasons: List[str] = []

    for label, (terms, confidence) in KEYWORDS.items():
        hits = [term for term in terms if term in lowered]
        if hits:
            matched_reasons.extend([f"Matched keyword: '{hit}'" for hit in hits])
            return IntentResult(
                label=label,
                confidence=confidence,
                reasons=matched_reasons,
            )

    if len(lowered.split()) < 4:
        return IntentResult(
            label="ambiguous",
            confidence=0.58,
            reasons=["Prompt is very short and underspecified."],
        )

    vague_terms = [
        "something",
        "stuff",
        "things",
        "important",
        "handle this",
        "take care of this",
        "do this",
        "fix this",
    ]

    if any(term in lowered for term in vague_terms):
        return IntentResult(
            label="ambiguous",
            confidence=0.60,
            reasons=["Prompt contains vague or underspecified language."],
        )

    return IntentResult(
        label="benign",
        confidence=0.88,
        reasons=["No high-risk patterns detected by the v1 ruleset."],
    )