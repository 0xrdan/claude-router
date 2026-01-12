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

1. **Read session state** from `~/.claude/router-session.json`
2. **Check last route** to determine escalation path
3. **Inform the user** of the escalation:
   ```
   Escalating from [last_model] to [new_model]...
   Re-running last query with more capable model.
   ```
4. **Spawn the appropriate subagent** using Task tool with the escalated model

## Escalation Guidance

If the user doesn't specify a target:
- From `fast`: Escalate to `standard` (Sonnet is usually sufficient)
- From `standard`: Escalate to `deep` (Opus for complex tasks)
- From `deep`: Suggest alternative approaches (already at max capability)

If the user specifies `deep`, always use Opus regardless of last route.

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
