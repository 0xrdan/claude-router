---
name: migrate-marketplace
description: Migrate from deprecated claude-router-marketplace to new 0xrdan/claude-plugins marketplace
user_invokable: true
---

# Migrate Marketplace Skill

Helps users migrate from the deprecated `claude-router-marketplace` to the new centralized `0xrdan/claude-plugins` marketplace.

## What This Does

This is a **marketplace change only** - the claude-router plugin repo remains the same. We're simply moving to a centralized marketplace that will host multiple plugins.

## Why Migrate?

- The old `claude-router-marketplace` is deprecated
- Future updates will only be available via `0xrdan/claude-plugins`
- The old marketplace will stop working in a future release

## Migration Steps

When this skill is invoked, guide the user through these steps:

### Step 1: Uninstall from old marketplace
```
/plugin uninstall claude-router@claude-router-marketplace
```

### Step 2: Remove old marketplace
```
/plugin marketplace remove claude-router-marketplace
```

### Step 3: Add new marketplace
```
/plugin marketplace add 0xrdan/claude-plugins
```

### Step 4: Install from new marketplace
```
/plugin install claude-router
```

### Step 5: Restart Claude Code
Tell the user to restart their Claude Code session to activate the plugin.

## Instructions

When this skill is invoked:

1. **Explain the change**: This is just a marketplace reorganization. The claude-router plugin itself hasn't moved - it's still at `github.com/0xrdan/claude-router`. We're moving to a centralized marketplace to support multiple plugins.

2. **Show the commands**: Present all migration commands clearly so the user can copy them.

3. **Reassure the user**:
   - Their settings and stats are preserved (stored in `~/.claude/`)
   - The plugin functionality is identical
   - This is a one-time migration

4. **Offer to help**: Ask if they want you to explain any step or if they have questions.

## Example Response

```
The claude-router marketplace has moved to a new centralized location.
This is just a distribution change - the plugin itself is the same.

To migrate, run these commands in order:

1. /plugin uninstall claude-router@claude-router-marketplace
2. /plugin marketplace remove claude-router-marketplace
3. /plugin marketplace add 0xrdan/claude-plugins
4. /plugin install claude-router
5. Restart Claude Code

Your settings and statistics are preserved - they're stored separately from the plugin.

The old marketplace will stop working in a future update, so please migrate soon!
```

## Notes

- All user data (stats, learnings, settings) is stored in `~/.claude/` and is NOT affected
- The plugin source code hasn't changed location
- This enables us to publish additional plugins through the same marketplace
