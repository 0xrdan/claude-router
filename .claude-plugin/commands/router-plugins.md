---
name: router-plugins
description: List and toggle official plugin integrations
---

# /router-plugins Command

Manage integrations with official Claude Code plugins.

## Usage

```
/router-plugins                     # List all plugins and status
/router-plugins enable <name>       # Enable integration
/router-plugins disable <name>      # Disable integration
/router-plugins detect              # Re-detect installed plugins
```

## Supported Plugins

| Plugin | Integration |
|--------|-------------|
| hookify | Pattern-based behavior rules |
| ralph-wiggum | Iterative development loops |
| code-review | Multi-agent PR review |
| feature-dev | 7-phase feature development |

## Example Output

```
Plugin Integrations
───────────────────
  hookify:       [x] Detected  [ ] Enabled
  ralph-wiggum:  [ ] Not found
  code-review:   [x] Detected  [x] Enabled
  feature-dev:   [x] Detected  [ ] Enabled
```

## Notes

All plugins are **optional** - Claude Router works fully without them.
Install plugins with: `/plugin install <name>@claude-plugins-official`
