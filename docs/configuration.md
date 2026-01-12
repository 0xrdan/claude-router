# Configuration & Commands

## Hybrid Classification

By default, Claude Router uses rule-based classification (instant, free). For edge cases with low confidence, it can use Haiku LLM for smarter routing.

To enable LLM fallback, set your API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Or add it to your project's `.env` file.

---

## Commands Reference

Claude Router provides slash commands for routing, knowledge management, and more.

### Routing Commands

#### `/route <model> <query>`

Override automatic routing and force a specific model:

```
/route opus What's the syntax for a TypeScript interface?
/route haiku Fix the authentication bug
/route sonnet Design a caching system
```

Models: `haiku`/`fast`, `sonnet`/`standard`, `opus`/`deep`

#### `/router-stats`

View your routing statistics and cost savings:

```
/router-stats
```

---

### Knowledge Commands (v1.4)

#### `/learn`

Extract insights from current conversation NOW.

#### `/learn-on`

Enable continuous learning (auto-extracts every 10 queries).

#### `/learn-off`

Disable continuous learning.

#### `/knowledge`

View knowledge base status and recent learnings.

#### `/learn-reset`

Clear all knowledge and start fresh.

See [Knowledge System](knowledge-system.md) for full documentation.

---

### Context Forking Commands (v2.0)

#### `/orchestrate <task>`

Execute complex multi-step tasks with forked context:

```
/orchestrate Refactor the authentication system to use JWT tokens
/orchestrate Add comprehensive error handling across all API endpoints
```

**Benefits:**
- Clean history (subtasks stay in fork)
- Cost optimized (40-50% cheaper)
- Better focus

#### `/router-analytics`

Generate interactive HTML analytics dashboard:

```
/router-analytics
/router-analytics --output ~/Desktop/router-report.html
```

Generates charts for:
- Route distribution
- Daily/weekly trends
- Cost savings

---

### Error Recovery Commands (v2.0)

#### `/retry`

Retry last query with an escalated model:

```
/retry              # Escalate to next tier
/retry deep         # Force escalation to Opus
/retry standard     # Force escalation to Sonnet
```

**Use when:**
- Timeout or error occurred
- Incomplete answer
- Wrong approach
- Need more depth

**Escalation path:**
- `fast` (Haiku) → `standard` (Sonnet)
- `standard` (Sonnet) → `deep` (Opus)
- `deep` (Opus) → Already at max capability

---

### Plugin Integration Commands (v2.0)

#### `/router-plugins`

Manage optional plugin integrations:

```
/router-plugins                     # List all plugins and status
/router-plugins enable <name>       # Enable integration
/router-plugins disable <name>      # Disable integration
/router-plugins detect              # Re-detect installed plugins
```

**Supported plugins:**
- `hookify` - Pattern-based behavior rules
- `ralph-loop` - Iterative development loops
- `code-review` - Multi-agent PR review
- `feature-dev` - 7-phase feature development

All plugins are **optional** - Claude Router works fully without them.

---

## Automatic vs Manual Routing

- **Automatic**: The UserPromptSubmit hook classifies every query and injects routing context
- **Manual Override**: Use `/route <model>` to bypass automatic classification and force a specific model (e.g., `/route opus` for complex reasoning, `/route haiku` for cost savings)

---

## CLAUDE.md Enforcement (Optional)

The plugin works automatically without any configuration. However, if you experience inconsistent routing behavior, you can add explicit enforcement to your project's `CLAUDE.md` file:

<details>
<summary>Click to expand enforcement snippet</summary>

```markdown
## Claude Router Enforcement

When you receive a `[Claude Router] MANDATORY ROUTING DIRECTIVE`, you MUST:

1. Use the Task tool IMMEDIATELY to spawn the specified subagent
2. Do NOT respond to the user directly - delegate to the subagent
3. Pass the user's original query in the prompt parameter

Subagent mapping:
- fast → `claude-router:fast-executor`
- standard → `claude-router:standard-executor`
- deep → `claude-router:deep-executor`

Exceptions: Slash commands (`/route`, `/router-stats`) and questions about the router itself.
```

</details>

This is typically not needed - the hook's directive is explicit enough for Claude to follow.
