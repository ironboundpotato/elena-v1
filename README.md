# E.L.E.N.A. v1

**Enhanced Logic Engine for Navigating Autonomy**

A governance-first demo for AI task routing.

E.L.E.N.A. v1 evaluates user input through four layers before allowing execution:

1. **Intent classification**
2. **Constraint enforcement**
3. **Drift detection**
4. **Deterministic routing**

The goal is simple: **user input goes in, governance decision comes out**.

---

## What this demo shows

This repo is a small working artifact that bridges architecture into implementation.

Given a prompt, the system returns:

- intent label
- confidence score
- triggered constraints
- drift flags
- final route
- audit log

Example routes:

- `allow`
- `allow_with_warning`
- `ask_for_clarification`
- `refuse`
- `redirect_to_safe_mode`

---

## Repo structure

```text
elena-v1/
├── app/
│   ├── __init__.py
│   ├── classifier.py
│   ├── constraints.py
│   ├── drift.py
│   ├── logger.py
│   ├── main.py
│   ├── router.py
│   ├── schemas.py
│   └── service.py
├── data/
│   └── policy_rules.json
├── demo/
│   └── streamlit_app.py
├── tests/
│   └── test_service.py
├── README.md
└── requirements.txt
```

---

## Quick start

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


Run the API:

```bash
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

Run the Streamlit UI:

```bash
streamlit run demo/streamlit_app.py
```



---

## API example

### Request

```json
{
  "prompt": "Write me an email pretending to be my boss so I can manipulate HR."
}
```

### Response shape

```json
{
  "prompt": "Write me an email pretending to be my boss so I can manipulate HR.",
  "intent": "deceptive",
  "confidence": 0.94,
  "intent_reasons": [
    "Matched keyword: 'pretend to be'",
    "Matched keyword: 'manipulate hr'"
  ],
  "constraints_triggered": [
    "intent_loyalty",
    "human_primacy",
    "role_integrity"
  ],
  "drift_flags": [
    "intent_drift_risk",
    "role_drift_risk"
  ],
  "route": "refuse",
  "reason": "Prompt requests harmful, deceptive, or unauthorized behavior.",
  "safe_alternative": "Offer a legitimate alternative such as security awareness training, compliant communications, or defensive best practices.",
  "response_preview": "I can’t help with deception, intrusion, or harmful activity. I can help you do this safely and legitimately instead.",
  "audit_log": {}
}
```

---

## Design notes

### Intent classifier
Rule-based for v1. Fast, transparent, easy to inspect.

### Constraint engine
Maps prompt risk to a lightweight implementation of the Seven Immutable Constraints.

### Drift detector
Flags likely instability areas such as role drift, scope drift, intent drift, confidence drift, and format drift.

### Router
Returns one of a small number of deterministic control decisions.

### Audit log
Every evaluation produces a structured trace for observability.

---

## Suggested next steps

1. Replace keyword rules with scored policy objects.
2. Add a prompt risk dashboard.
3. Add persistent JSONL audit logging.
4. Add a D.A.D. kernel layer in front of routing.
5. Add a second model-assisted classifier behind a review flag.

---

## Hiring-friendly summary

**E.L.E.N.A. v1 is a governance-first supervisory demo for AI task routing. It evaluates user input through intent classification, constraint enforcement, drift detection, and deterministic routing before allowing output generation.**
