# Claude Router

**Intelligent model routing for Claude Code** - Automatically routes queries to the optimal Claude model (Haiku/Sonnet/Opus) based on complexity, reducing costs by up to 98% without sacrificing quality.

## What Makes This Novel

This project fills a gap that no existing tool addresses:

| What Exists | What Claude Router Does |
|-------------|-------------------------|
| Multi-provider routers (OpenRouter, etc.) | **Intra-Claude optimization** (Haiku/Sonnet/Opus) |
| Manual `/model` switching | **Automatic routing** via UserPromptSubmit hook |
| Generic LLM complexity scoring | **Coding-task specific** pattern recognition |
| External API wrapper approach | **Native Claude Code integration** using subagents |

### Technical Achievements

1. **Discovered the right architecture** - Researched hooks, MCP, and subagents to find the only viable approach
2. **Solved the hook integration** - UserPromptSubmit hook injects routing context that triggers subagent spawning
3. **Optimized token overhead** - Minimal agent definitions reduced overhead by 70% (from 11.9k to 3.4k tokens)
4. **Built hybrid classification** - Rule-based for speed, LLM fallback for accuracy

## The Problem

When using Claude Code, you're typically on a single model:
- **Always Opus?** You're overpaying 5x for simple queries
- **Always Sonnet?** Complex architecture tasks may need deeper reasoning
- **Manual switching?** Tedious and requires knowing which model fits

**Claude Router solves this** by automatically analyzing each query and routing it to the most cost-effective model.

## Key Metrics

| Metric | Value |
|--------|-------|
| Classification latency | ~0ms (rule-based) or ~100ms (LLM fallback) |
| Classification cost | $0 (rules) or ~$0.001 (Haiku fallback) |
| Subagent token overhead | ~3.4k tokens (optimized) |
| Cost savings (simple queries) | **~98%** (Haiku vs Opus) |
| Cost savings (mixed workload) | **Est. 50-70%** |

## Why This Matters: Three-Fold Savings

Intelligent routing creates a **win-win** for everyone:

### 1. Consumer Savings (API Costs)

LLM pricing has two components, and you save on both:

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Haiku | $0.25 | $1.25 |
| Sonnet | $3 | $15 |
| Opus | $15 | $75 |

For a typical query (1K input, 2K output tokens):
- **Opus cost:** $0.015 + $0.15 = **$0.165**
- **Haiku cost:** $0.00025 + $0.0025 = **$0.00275**
- **Your savings:** ~98%

### 2. Anthropic Savings (Compute Resources)

Haiku is a much smaller, faster model than Opus. When simple queries are routed to Haiku:
- Less GPU compute required per request
- Lower inference latency (faster responses for you)
- More efficient resource allocation across Anthropic's infrastructure
- Frees up Opus capacity for queries that genuinely need it

### 3. Better Developer Experience

- Simple queries get instant answers (Haiku is faster)
- Complex queries get thorough analysis (Opus when needed)
- No manual model switching required

### 4. Subscriber Benefits (Pro/Max Users)

For Claude Pro and Max subscribers, intelligent routing means:
- **Extended usage limits** - Smaller models use less of your monthly capacity
- **Longer sessions** - Less context consumed = fewer auto-compacts
- **Faster responses** - Haiku responds 3-5x faster than Opus

**The result:** You pay less (or extend your subscription further), Anthropic uses fewer resources, and everyone gets appropriately-powered responses. This is sustainable AI usage.

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                   Your Query                                │
│                       │                                     │
│                       ▼                                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │          UserPromptSubmit Hook                         │ │
│  │          (classify-prompt.py)                          │ │
│  │                                                        │ │
│  │  1. Rule-based patterns (instant, free)                │ │
│  │  2. Haiku LLM fallback (for edge cases, ~$0.001)       │ │
│  └───────────────────────────────────────────────────────┘ │
│                       │                                     │
│         ┌─────────────┼─────────────┐                       │
│         ▼             ▼             ▼                       │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐                 │
│  │   fast    │ │ standard  │ │   deep    │                 │
│  │  (Haiku)  │ │ (Sonnet)  │ │  (Opus)   │                 │
│  │   $0.25   │ │    $3     │ │   $15     │  per 1M input   │
│  └───────────┘ └───────────┘ └───────────┘                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Option 1: Claude Code Plugin (Recommended)

Run these commands in any Claude Code session:

```bash
# Step 1: Add the marketplace (one-time, per project)
/plugin marketplace add 0xrdan/claude-router

# Step 2: Install the plugin
/plugin install claude-router@claude-router-marketplace

# Step 3: Restart Claude Code session to activate
```

**Note:** The marketplace must be added in each project where you want to use Claude Router. Once added, updates are automatic.

```bash
# Update manually
/plugin marketplace update claude-router-marketplace

# Uninstall
/plugin uninstall claude-router@claude-router-marketplace
```

### Option 2: One-Command Install

```bash
# Install
curl -sSL https://raw.githubusercontent.com/0xrdan/claude-router/main/install.sh | bash

# Uninstall
curl -sSL https://raw.githubusercontent.com/0xrdan/claude-router/main/uninstall.sh | bash
```

### Option 3: Manual Install

```bash
# Install
git clone https://github.com/0xrdan/claude-router.git
cd claude-router
./install.sh

# Uninstall
./uninstall.sh
```

## Routing Rules

### Fast Route (Haiku) - Simple queries
- Factual questions ("What is X?")
- Code formatting, linting
- Git status, log, diff
- JSON/YAML manipulation
- Regex generation
- Syntax questions

### Standard Route (Sonnet) - Typical coding
- Bug fixes
- Feature implementation
- Code review
- Refactoring
- Test writing

### Deep Route (Opus) - Complex tasks
- Architecture decisions
- Security audits
- Multi-file refactors
- Trade-off analysis
- Performance optimization
- System design

## Example Output

```
[Claude Router] ROUTING DIRECTIVE
Route: deep | Model: Opus | Confidence: 95% | Method: haiku-llm
Signals: architecture, system design, trade-offs

ACTION REQUIRED: Use the Task tool to spawn the "deep-executor" subagent...
```

## Configuration

### Hybrid Classification

By default, Claude Router uses rule-based classification (instant, free). For edge cases with low confidence, it can use Haiku LLM for smarter routing.

To enable LLM fallback, set your API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Or add it to your project's `.env` file.

### Commands

Claude Router provides two slash commands:

**`/route <query>`** - Manually route a specific query:
```
/route What's the syntax for a TypeScript interface?
```

**`/router-stats`** - View your routing statistics and cost savings:
```
/router-stats
```

### Automatic vs Manual Routing

- **Automatic**: The UserPromptSubmit hook classifies every query and injects routing context
- **Manual**: Use `/route` to explicitly route a query with visible classification

## Project Structure

```
claude-router/
├── hooks/
│   └── classify-prompt.py     # Hybrid classifier (auto-routing)
├── commands/
│   ├── route.md               # /route command
│   └── router-stats.md        # /router-stats command
├── agents/
│   ├── fast-executor.md       # Haiku agent
│   ├── standard-executor.md   # Sonnet agent
│   └── deep-executor.md       # Opus agent
└── skills/
    └── route/                 # Auto-invoked routing skill
```

## Why Anthropic Should Care

1. **Validates their model lineup** - Proves Haiku/Sonnet/Opus tiering works in practice
2. **Real usage data** - What % of coding queries actually need Opus?
3. **Adoption driver** - Lower effective cost → more Claude Code usage
4. **Reference implementation** - Could inform native routing features
5. **Community showcase** - Open source tool built *for* their ecosystem

## What Would Make People Use It

1. **Zero-config start** - Works immediately with sensible defaults
2. **Visible savings** - Use `/router-stats` to see your cost savings
3. **Trust through transparency** - Every routing decision is explained
4. **Easy override** - `/route` skill for manual control when needed
5. **Learns from feedback** - Future: adjust routing based on user overrides

## Roadmap

### Completed
- [x] **Phase 1:** Rule-based classification (~0ms, $0)
- [x] **Phase 2:** Hybrid classification (rules + Haiku LLM fallback)
- [x] **Phase 3:** Standalone repository
- [x] **Phase 4:** Usage statistics and savings tracker
  - Routing decisions logged to `~/.claude/router-stats.json`
  - `/router-stats` skill shows savings and route distribution

### Coming Soon
- [ ] **Phase 5:** Context-aware routing
  - Cache classifications for similar queries
  - Factor in number of files open
  - Consider session history and error patterns
  - Adjust based on project complexity profile

- [ ] **Phase 6:** Learning from feedback
  - Track user overrides
  - Adjust future routing based on patterns
  - Per-project routing profiles

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

```bash
git clone https://github.com/0xrdan/claude-router.git
cd claude-router
./install.sh  # Choose option 1 for project install
```

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built for the Claude Code community** | [Report Issues](https://github.com/0xrdan/claude-router/issues) | [Follow @dannymonteiro on LinkedIn](https://linkedin.com/in/dannymonteiro)
