# Claude Router

**Intelligent model routing for Claude Code** - Automatically routes queries to the optimal Claude model (Haiku/Sonnet/Opus) based on complexity, reducing costs by up to 80% without sacrificing quality.

## What Makes This Novel

| What Exists | What Claude Router Does |
|-------------|-------------------------|
| Multi-provider routers (OpenRouter, etc.) | **Intra-Claude optimization** (Haiku/Sonnet/Opus) |
| Manual `/model` switching | **Automatic routing** via UserPromptSubmit hook |
| Generic LLM complexity scoring | **Coding-task specific** pattern recognition |
| External API wrapper approach | **Native Claude Code integration** using subagents |

**Technical Achievements:**
- Zero-latency rule-based classification with LLM fallback
- Token-optimized agent definitions (3.4k vs 11.9k tokens)
- Multi-turn context awareness and follow-up detection
- Persistent knowledge system across sessions

## Key Metrics

| Metric | Value |
|--------|-------|
| Classification latency | ~0ms (rules) or ~100ms (LLM fallback) |
| Classification cost | $0 (rules) or ~$0.001 (Haiku fallback) |
| Cost savings (simple queries) | **~80%** (Haiku vs Opus) |
| Cost savings (mixed workload) | **Est. 50-70%** |
| Additional savings (orchestration) | **~40%** on complex tasks |

## Installation

```bash
# Step 1: Add the marketplace (one-time, per project)
/plugin marketplace add 0xrdan/claude-router

# Step 2: Install the plugin
/plugin install claude-router@claude-router-marketplace

# Step 3: Restart Claude Code session to activate
```

That's it! The plugin automatically routes queries - no configuration needed.

```bash
# Update
/plugin marketplace update claude-router-marketplace

# Uninstall
/plugin uninstall claude-router@claude-router-marketplace
```

## Quick Start

**Automatic routing** works out of the box:
- Simple queries → Haiku (fast, cheap)
- Coding tasks → Sonnet (balanced)
- Complex analysis → Opus (powerful)

**Manual override** when needed:
```bash
/route opus "Design a microservice architecture"
/route haiku "What is JSON?"
```

**View statistics:**
```bash
/router-stats
```

## Commands

| Command | Description |
|---------|-------------|
| `/route <model>` | Override routing for a query |
| `/router-stats` | View usage statistics |
| `/learn` | Extract insights from conversation |
| `/knowledge` | View knowledge base status |
| `/orchestrate` | Execute complex tasks with forking |
| `/router-analytics` | Generate HTML dashboard |
| `/retry` | Retry with escalated model |
| `/router-plugins` | Manage plugin integrations |

See [Configuration & Commands](docs/configuration.md) for full documentation.

## Documentation

| Document | Description |
|----------|-------------|
| [How It Works](docs/how-it-works.md) | Default vs Router behavior, cost savings |
| [Routing Rules](docs/routing.md) | Classification rules, example output |
| [Configuration](docs/configuration.md) | All commands and settings |
| [Knowledge System](docs/knowledge-system.md) | Persistent learning across sessions |
| [Architecture](docs/architecture.md) | Project structure, data flow |
| [Roadmap](docs/roadmap.md) | Completed phases, coming soon |
| [Contributing](docs/CONTRIBUTING.md) | How to contribute |

## How It Works

Claude Router intercepts queries and routes them to the optimal model:

```
"What is JSON?"        → Haiku   (~$0.01)  ✓ Fast, cheap
"Fix this typo"        → Haiku   (~$0.01)  ✓ Fast, cheap
"Run all tests"        → Sonnet  (~$0.03)  ✓ Balanced
"Design architecture"  → Opus    (~$0.06)  ✓ Powerful
```

For complex tasks, the Opus Orchestrator delegates subtasks to cheaper models:
- Opus handles strategy → expensive reasoning
- Haiku handles file reads → cheap I/O
- Sonnet handles edits → balanced implementation

**Result:** Same quality, ~40% less cost on complex workflows.

See [How It Works](docs/how-it-works.md) for detailed comparison.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built for the Claude Code community** | [Report Issues](https://github.com/0xrdan/claude-router/issues) | [Follow @dannymonteiro on LinkedIn](https://linkedin.com/in/dannymonteiro)
