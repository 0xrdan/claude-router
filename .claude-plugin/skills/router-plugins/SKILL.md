---
name: router-plugins
description: List and toggle official plugin integrations
user_invokable: true
---

# Router Plugins

Manage integrations with official Claude Code plugins.

## What This Does

Claude Router can optionally integrate with these official plugins:
- **hookify**: Pattern-based behavior rules
- **ralph-wiggum**: Iterative development loops
- **code-review**: Multi-agent PR review
- **feature-dev**: 7-phase feature development

When enabled, Claude Router can suggest using these plugins for appropriate tasks.

## Usage

```
/router-plugins                     # List all plugins and status
/router-plugins enable <name>       # Enable integration
/router-plugins disable <name>      # Disable integration
/router-plugins detect              # Re-detect installed plugins
```

## Example Output

```
Plugin Integrations
───────────────────

  hookify:       [x] Detected  [ ] Enabled
  ralph-wiggum:  [ ] Not found
  code-review:   [x] Detected  [x] Enabled
  feature-dev:   [x] Detected  [ ] Enabled

Use `/router-plugins enable <name>` to enable integration.
```

## Instructions

When this skill is invoked:

### List Mode (no arguments or just `/router-plugins`)

1. Read plugin detection from `~/.claude/plugins/` and `~/.config/claude-code/plugins/`
2. Read enabled state from `knowledge/state.json` under `plugin_integrations`
3. Display status table showing:
   - Plugin name
   - Detection status (Detected / Not found)
   - Enabled status (if detected)

### Enable Mode (`/router-plugins enable <name>`)

1. Check if plugin is in supported list: hookify, ralph-wiggum, code-review, feature-dev
2. Check if plugin is detected (installed)
3. If not detected, inform user how to install:
   ```
   Plugin "ralph-wiggum" not found.
   Install with: /plugin install ralph-wiggum@claude-plugins-official
   ```
4. If detected, update `knowledge/state.json`:
   ```json
   {
     "plugin_integrations": {
       "<name>": {"enabled": true, "detected": true}
     }
   }
   ```
5. Confirm: `Plugin integration "hookify" enabled.`

### Disable Mode (`/router-plugins disable <name>`)

1. Update `knowledge/state.json` to set `enabled: false`
2. Confirm: `Plugin integration "hookify" disabled.`

### Detect Mode (`/router-plugins detect`)

1. Scan plugin locations for installed plugins
2. Update `detected` flags in state
3. Report findings

## Integration Behavior

When integrations are enabled:

- **hookify**: Routing can suggest creating hookify rules for repeated patterns
- **ralph-wiggum**: Orchestrated tasks may suggest `/ralph-loop` for iterative work
- **code-review**: PR review queries may suggest using the code-review plugin
- **feature-dev**: Feature requests may suggest the structured feature-dev workflow

These are suggestions only - all plugins work independently of claude-router.

## Notes

- Plugins are optional enhancements, not dependencies
- Claude Router works fully without any plugins installed
- Detection checks common install locations
- State is stored in project-local `knowledge/state.json`
