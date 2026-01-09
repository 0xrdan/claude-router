---
name: learn-off
description: Disable continuous learning mode
---

# /learn-off Command

Disable continuous learning mode.

## Usage

```
/learn-off
```

## What It Does

Stops automatic insight extraction. Manual `/learn` commands still work.

## Instructions

1. Read `knowledge/state.json`
2. Set `learning_mode` to `false`
3. Set `learning_mode_since` to `null`
4. Write updated state back
5. Confirm to user with session summary
