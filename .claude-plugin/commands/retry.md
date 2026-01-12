---
name: retry
description: Retry last query with an escalated model
---

# /retry Command

Retry the last query with a more capable model when the initial attempt was insufficient.

## Usage

```
/retry              # Escalate to next tier
/retry deep         # Force escalation to Opus
/retry standard     # Force escalation to Sonnet
```

## When to Use

- **Timeout or error**: Query failed due to complexity
- **Incomplete answer**: Model didn't fully address the question
- **Wrong approach**: Model misunderstood the task
- **Need more depth**: Initial answer was too superficial

## Escalation Path

Auto-escalation (when no model specified):
- `fast` (Haiku) → `standard` (Sonnet)
- `standard` (Sonnet) → `deep` (Opus)
- `deep` (Opus) → Already at max capability

**When user specifies `/retry deep` or `/retry standard`, use that model exactly. Do not auto-escalate.**

## Notes

Session state persists for 30 minutes. If no previous query exists, you'll be informed.
