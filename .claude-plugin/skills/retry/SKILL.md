---
name: retry
description: Retry the last query with an escalated model
user_invokable: true
---

# Retry Skill

Retry the last query with a more capable model when the initial attempt failed or was insufficient.

## What This Does

When a query routed to a cheaper model (Haiku or Sonnet) produces unsatisfactory results, errors, or timeouts, use `/retry` to:
1. Re-route to the next tier up (Haiku -> Sonnet -> Opus)
2. Preserve the original query context
3. Give the more capable model a chance to succeed

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

## How It Works

1. Read the last routing decision from session state (`~/.claude/router-session.json`)
2. Determine the appropriate escalation:
   - `fast` (Haiku) -> `standard` (Sonnet)
   - `standard` (Sonnet) -> `deep` (Opus)
   - `deep` (Opus) -> Already at max, suggest different approach
3. Re-execute the last query with the escalated model
4. Update session state with the new route

## Instructions

When this skill is invoked:

1. **Check for explicit model** - Did user specify `deep`/`opus` or `standard`/`sonnet`?
   - **YES**: Use that model. **DO NOT auto-escalate. Honor the explicit choice.**
   - **NO**: Proceed to escalation logic
2. **Read session state** from `~/.claude/router-session.json`
3. **Determine escalation** (only if no explicit model):
   - From `fast`: Escalate to `standard`
   - From `standard`: Escalate to `deep`
   - From `deep`: Already at max, suggest different approach
4. **Inform the user** of the escalation
5. **Spawn the appropriate subagent** using Task tool

**CRITICAL: If user specifies a model (`/retry deep`, `/retry standard`), use exactly that model. No exceptions.**

## Example

User ran a complex refactoring query that was routed to Haiku.
Haiku produced incomplete results.

```
User: /retry
Assistant: Escalating from Haiku to Sonnet...
           Re-running your refactoring query with more capable model.
           [Spawns standard-executor with the original query]
```

## Notes

- This skill reads the session state, which persists for 30 minutes
- If no previous query exists, inform the user
- Consider the failure reason when suggesting the escalation level
