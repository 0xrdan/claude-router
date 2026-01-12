---
name: migrate-marketplace
description: Migrate from deprecated marketplace to 0xrdan/claude-plugins
---

# /migrate-marketplace Command

Migrate from the deprecated `claude-router-marketplace` to the new `0xrdan/claude-plugins` marketplace.

## Usage

```
/migrate-marketplace
```

## What It Does

Guides you through migrating to the new centralized marketplace. This is a **marketplace change only** - the plugin repo (`0xrdan/claude-router`) stays the same.

## Why Migrate?

- Old marketplace is deprecated
- Future updates only via new marketplace
- Old marketplace will stop working in a future release

## Migration Commands

```
/plugin uninstall claude-router@claude-router-marketplace
/plugin marketplace remove claude-router-marketplace
/plugin marketplace add 0xrdan/claude-plugins
/plugin install claude-router
```

Then restart Claude Code.

## Notes

- Your settings and stats are preserved
- Plugin functionality is identical
- One-time migration
