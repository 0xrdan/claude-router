---
name: orchestrate
description: Execute complex multi-step tasks with forked context
---

# /orchestrate Command

Execute complex, multi-step tasks using the Opus Orchestrator with context forking.

## Usage

```
/orchestrate <your complex task description>
```

## What It Does

Spawns a forked context where the Opus Orchestrator can:
- Decompose complex tasks into subtasks
- Delegate to Haiku (simple) and Sonnet (moderate) agents
- Keep intermediate work isolated from your main conversation

## Examples

```
/orchestrate Refactor the authentication system to use JWT tokens
/orchestrate Add comprehensive error handling across all API endpoints
/orchestrate Implement a caching layer for database queries
```

## Benefits

- **Clean History**: Subtask chatter stays in the fork
- **Cost Optimized**: 40-50% cheaper through smart delegation
- **Better Focus**: Orchestrator can iterate without cluttering context
