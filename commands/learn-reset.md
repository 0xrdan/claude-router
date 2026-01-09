---
name: learn-reset
description: Clear the knowledge base and start fresh
---

# /learn-reset Command

Clear all accumulated knowledge and reset to a fresh state.

## Usage

```
/learn-reset
```

## What It Does

- Clears all entries from learnings files
- Resets the classification cache
- Resets learning state

**Warning:** This cannot be undone.

## Instructions

1. Confirm with user before proceeding
2. Reset each file in `knowledge/learnings/` to empty state
3. Clear `knowledge/cache/classifications.md`
4. Reset `knowledge/state.json` to initial values
5. Confirm completion with summary of what was cleared
