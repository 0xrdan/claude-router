---
name: knowledge
description: Display knowledge base status and recent learnings
---

# /knowledge Command

View the current state of the project's knowledge base.

## Usage

```
/knowledge
```

## What It Does

Shows:
- Learning mode status (on/off)
- Entry counts per category (patterns, quirks, decisions)
- Recent learnings extracted
- Cache statistics

## Instructions

1. Read `knowledge/state.json` for learning mode status
2. Read each learnings file and count entries
3. Extract recent entries (last 5)
4. Format and display the summary
5. If empty, show getting started guidance
