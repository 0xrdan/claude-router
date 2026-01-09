---
name: learn
description: Extract and persist insights from the current conversation to the knowledge base
---

# /learn Command

Extract insights from the current conversation and save them to the project's knowledge base.

## Usage

```
/learn
```

## What It Does

Analyzes the conversation to identify:
- **Patterns** - Approaches that worked well
- **Quirks** - Project-specific gotchas discovered
- **Decisions** - Architectural choices made with rationale

Saves insights to `knowledge/learnings/` for future sessions.

## Instructions

1. Analyze the current conversation for extractable insights
2. Categorize each as pattern, quirk, or decision
3. Read the appropriate file from `knowledge/learnings/`
4. Append new entries in the correct format
5. Update `knowledge/state.json` with extraction timestamp
6. Report what was learned to the user
