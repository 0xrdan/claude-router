---
name: learn-on
description: Enable continuous learning mode for automatic insight extraction
---

# /learn-on Command

Enable continuous learning mode.

## Usage

```
/learn-on
```

## What It Does

Activates automatic insight extraction during the session. The router will periodically extract insights without manual `/learn` commands.

## Instructions

1. Read `knowledge/state.json`
2. Set `learning_mode` to `true`
3. Set `learning_mode_since` to current timestamp
4. Write updated state back
5. Confirm to user that continuous learning is enabled
