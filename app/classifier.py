from dataclasses import dataclass


@dataclass
class IntentResult:
    label: str
    confidence: float
    reasons: list[str]


def _normalize(text: str) -> str:
    return " ".join((text or "").lower().strip().split())


def _contains_any(text: str, patterns: list[str]) -> bool:
    return any(pattern in text for pattern in patterns)


def classify_intent(user_input: str) -> IntentResult:
    text = _normalize(user_input)

    credential_terms = [
        "credential",
        "credentials",
        "password",
        "passwords",
        "login credential",
        "login credentials",
        "auth token",
        "auth tokens",
        "access token",
        "access tokens",
        "session token",
        "session tokens",
        "api key",
        "api keys",
        "secret key",
        "secret keys",
    ]

    data_terms = [
        "client data",
        "customer data",
        "user data",
        "private user data",
        "private data",
        "sensitive data",
        "confidential data",
        "personal data",
        "customer records",
        "private customer records",
        "employee records",
        "internal employee records",
        "database contents",
        "records",
    ]

    extraction_terms = [
        "get",
        "retrieve",
        "pull",
        "collect",
        "gather",
        "extract",
        "export",
        "dump",
        "list",
        "enumerate",
        "compile",
        "access",
    ]

    disguise_terms = [
        "audit",
        "security testing",
        "testing",
        "for research",
        "research purposes",
        "quietly",
        "help me",
        "sample",
    ]

    deceptive_patterns = [
        "pretend to be my boss",
        "pretend to be someone else",
        "impersonate",
        "pressure hr",
        "trick hr",
        "social engineer",
        "phishing",
        "spoof",
        "fake identity",
    ]

    ambiguity_patterns = [
        "get the data",
        "handle it",
        "do what needs to be done",
        "take care of it",
        "make it happen",
    ]

    safe_patterns = [
        "write a friendly email",
        "explain database security best practices",
        "database security best practices",
        "how do companies protect sensitive data",
        "protect sensitive data",
        "protecting customer data",
        "secure a database",
        "secure a database against credential theft",
        "how do i secure a database",
        "how do companies handle sensitive records safely",
        "best practices for protecting customer data",
        "make this clearer",
        "rewrite this",
        "summarize this",
    ]

    if _contains_any(text, deceptive_patterns):
        return IntentResult(
            label="deceptive",
            confidence=0.95,
            reasons=["Deceptive impersonation or pressure pattern detected."],
        )

    if _contains_any(text, credential_terms):
        if _contains_any(text, extraction_terms) or _contains_any(text, disguise_terms):
            return IntentResult(
                label="credential_theft",
                confidence=0.99,
                reasons=["Credential theft or secret extraction intent detected."],
            )

    if _contains_any(text, data_terms):
        if _contains_any(text, extraction_terms) or _contains_any(text, disguise_terms):
            return IntentResult(
                label="data_exfiltration",
                confidence=0.97,
                reasons=["Sensitive/private data extraction intent detected."],
            )

    if _contains_any(text, ambiguity_patterns):
        return IntentResult(
            label="ambiguous",
            confidence=0.82,
            reasons=["Prompt is too underspecified for safe, precise execution."],
        )

    if _contains_any(text, safe_patterns):
        return IntentResult(
            label="benign",
            confidence=0.92,
            reasons=["Safe informational or writing-assistance pattern detected."],
        )

    return IntentResult(
        label="benign",
        confidence=0.88,
        reasons=["No high-risk patterns detected by the v1 ruleset."],
    )