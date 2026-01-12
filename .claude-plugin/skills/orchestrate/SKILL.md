---
name: orchestrate
description: Execute complex multi-step tasks with forked subtask contexts for clean conversation history
context: fork
agent: claude-router:opus-orchestrator
---

# Orchestrate Skill

Execute complex, multi-step tasks using the Opus Orchestrator with context forking.

## What This Does

This skill spawns a forked context where the Opus Orchestrator can:
- Decompose complex tasks into subtasks
- Delegate appropriately to Haiku (simple) and Sonnet (moderate) agents
- Handle complex analysis and synthesis itself
- Keep intermediate work isolated from your main conversation

## When to Use

Use `/orchestrate` when you have:
- Multi-file refactoring tasks
- Complex feature implementations spanning multiple components
- Tasks requiring research, planning, and implementation phases
- Workflows with many sequential steps

## Benefits of Forked Context

1. **Clean History** - Subtask chatter stays in the fork, not your main conversation
2. **Better Focus** - Orchestrator can iterate without cluttering your context
3. **Automatic Cleanup** - Fork is discarded when task completes

## Usage

```
/orchestrate <your complex task description>
```

## Examples

```
/orchestrate Refactor the authentication system to use JWT tokens
/orchestrate Add comprehensive error handling across all API endpoints
/orchestrate Implement a caching layer for database queries
```

## How It Works

1. Your task is passed to the Opus Orchestrator in a forked context
2. Orchestrator analyzes and decomposes the task
3. Simple subtasks are delegated to Haiku (fast, cheap)
4. Moderate subtasks go to Sonnet (balanced)
5. Complex analysis stays with Opus
6. Results are synthesized and returned to your main conversation

## Cost Optimization

By delegating 60-70% of work to cheaper models, orchestrated tasks typically cost 40-50% less than running everything on Opus while maintaining quality.
