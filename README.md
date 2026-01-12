# Claude Router

**Intelligent model routing for Claude Code** - Automatically routes queries to the optimal Claude model (Haiku/Sonnet/Opus) based on complexity, reducing costs by up to 80% without sacrificing quality.

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

## Claude Code: Default vs With Router

### Default Behavior (Even with Opus 4.5)

Opus 4.5 is excellent at using tools and spawning subagents - but there's a catch:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DEFAULT CLAUDE CODE (Opus 4.5)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  User: "Refactor the auth system across all files"                          │
│                                                                              │
│  OPUS receives query                                                         │
│    ├─► OPUS spawns Explore agent ──► runs as OPUS ($$$)                     │
│    ├─► OPUS spawns Plan agent ────► runs as OPUS ($$$)                      │
│    ├─► OPUS reads files ──────────► OPUS doing simple reads ($$$)           │
│    └─► OPUS makes edits ──────────► OPUS for each file ($$$)                │
│                                                                              │
│  Problem: Opus is smart enough to delegate, but subagents inherit           │
│           the same expensive model. Simple file reads cost as much          │
│           as architectural analysis.                                         │
│                                                                              │
│  Also: Simple queries like "what is JSON?" still go to Opus.                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### With Claude Router (v2.0)

Claude Router adds **cost-aware routing at every level**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WITH CLAUDE ROUTER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LEVEL 1: Initial Query Routing (before any work starts)                    │
│  ─────────────────────────────────────────────────────────                  │
│  "What is JSON?"  ─────────────────────►  HAIKU      (~$0.01)               │
│  "Fix this typo"  ─────────────────────►  HAIKU      (~$0.01)               │
│  "Run all tests"  ─────────────────────►  SONNET     (~$0.03)               │
│  "Design microservice architecture" ───►  OPUS       (~$0.06)               │
│                                                                              │
│  LEVEL 2: Delegation Within Complex Tasks (v1.2 Orchestrator)               │
│  ─────────────────────────────────────────────────────────────              │
│  User: "Refactor the auth system across all files"                          │
│                                                                              │
│  OPUS ORCHESTRATOR receives query (detected as complex + tool-intensive)    │
│    ├─► Spawns HAIKU to list files ────► cheap file enumeration ($)          │
│    ├─► Spawns HAIKU to read files ────► cheap content gathering ($)         │
│    ├─► OPUS analyzes and plans ───────► expensive reasoning ($$$)           │
│    ├─► Spawns SONNET to edit files ───► balanced implementation ($$)        │
│    └─► OPUS synthesizes & verifies ───► expensive final check ($$$)         │
│                                                                              │
│  Result: Opus does the thinking, cheaper models do the legwork              │
│          Same quality, ~40% less cost on complex tasks                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### The Key Difference

| Aspect | Default Opus 4.5 | Claude Router |
|--------|------------------|---------------|
| Initial routing | Always Opus (or your default) | Right model for the task |
| Subagent model | Inherits parent model | Explicitly cheaper models |
| Simple queries | Opus overkill | Haiku (80% savings) |
| File reads in complex tasks | Opus ($$$) | Haiku ($) |
| Architectural decisions | Opus | Opus (same quality) |
| Cost awareness | None | Built-in at every level |

**TL;DR**: Opus 4.5 is great at *what* to delegate. Claude Router adds *cost-aware* delegation - ensuring cheap work uses cheap models.

## Key Metrics

| Metric | Value |
|--------|-------|
| Classification latency | ~0ms (rule-based) or ~100ms (LLM fallback) |
| Classification cost | $0 (rules) or ~$0.001 (Haiku fallback) |
| Subagent token overhead | ~3.4k tokens (optimized) |
| Cost savings (simple queries) | **~80%** (Haiku vs Opus) |
| Cost savings (mixed workload) | **Est. 50-70%** |
| Additional savings (v1.2 delegation) | **~40%** on complex orchestrated tasks |

## Why This Matters: Three-Fold Savings

Intelligent routing creates a **win-win** for everyone:

### 1. Consumer Savings (API Costs)

LLM pricing has two components, and you save on both:

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Haiku 4.5 | $1 | $5 |
| Sonnet 4.5 | $3 | $15 |
| Opus 4.5 | $5 | $25 |

For a typical query (1K input, 2K output tokens):
- **Opus 4.5 cost:** $0.005 + $0.05 = **$0.055**
- **Haiku 4.5 cost:** $0.001 + $0.01 = **$0.011**
- **Your savings:** ~80%

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

## Installation

Run these commands in any Claude Code session:

```bash
# Step 1: Add the marketplace (one-time, per project)
/plugin marketplace add 0xrdan/claude-router

# Step 2: Install the plugin
/plugin install claude-router@claude-router-marketplace

# Step 3: Restart Claude Code session to activate
```

That's it! The plugin automatically routes queries - no additional configuration needed.

**Note:** The marketplace must be added in each project where you want to use Claude Router. Once added, updates are automatic.

```bash
# Update manually
/plugin marketplace update claude-router-marketplace

# Uninstall
/plugin uninstall claude-router@claude-router-marketplace
```

## Routing Rules

### Fast Route (Haiku) - Simple queries
- Factual questions ("What is X?")
- Code formatting, linting
- Git status, log, diff
- JSON/YAML manipulation
- Regex generation
- Syntax questions

### Standard Route (Sonnet) - Typical coding + Tool-intensive tasks
- Bug fixes and feature implementation
- Code review and refactoring
- Test writing
- **Tool-intensive tasks** (v1.2): Codebase searches, running tests, multi-file edits
- **Orchestration tasks** (v1.2): Multi-step workflows

### Deep Route (Opus) - Complex tasks
- Architecture decisions
- Security audits
- Trade-off analysis
- Performance optimization
- System design

### Opus Orchestrator (v1.2) - Complex + Tool-intensive
When a query is both architecturally complex AND tool-intensive:
- Opus handles strategy and synthesis
- Delegates file reads/searches to Haiku
- Delegates implementations to Sonnet
- ~40% cost savings on complex workflows

## Example Output

**Simple query → Haiku:**
```
[Claude Router] MANDATORY ROUTING DIRECTIVE
Route: fast | Model: Haiku | Confidence: 90% | Method: rules
Signals: what is, json
```

**Tool-intensive query → Sonnet (v1.2):**
```
[Claude Router] MANDATORY ROUTING DIRECTIVE
Route: standard | Model: Sonnet | Confidence: 85% | Method: rules | Tool-intensive: Yes
Signals: find all, across the codebase
```

**Complex + Tool-intensive → Opus Orchestrator (v1.2):**
```
[Claude Router] MANDATORY ROUTING DIRECTIVE
Route: deep | Model: Opus (Orchestrator) | Confidence: 95% | Method: rules | Tool-intensive: Yes | Orchestration: Yes
Signals: architecture, refactor across the entire codebase
```

**Follow-up query with context awareness (v2.0):**
```
[Claude Router] MANDATORY ROUTING DIRECTIVE
Route: deep | Model: Opus | Confidence: 92% | Method: rules | Follow-up: Yes | Context boost: +0.1
Signals: follow-up to previous complex query
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

Claude Router provides slash commands for routing and knowledge management:

**Routing Commands:**

**`/route <model> <query>`** - Override automatic routing and force a specific model:
```
/route opus What's the syntax for a TypeScript interface?
/route haiku Fix the authentication bug
/route sonnet Design a caching system
```
Models: `haiku`/`fast`, `sonnet`/`standard`, `opus`/`deep`

**`/router-stats`** - View your routing statistics and cost savings:
```
/router-stats
```

**Knowledge Commands (v1.4):** `/learn`, `/learn-on`, `/learn-off`, `/knowledge`, `/learn-reset`

See [Knowledge System](#knowledge-system-v14) section for details.

**Context Forking Commands (v2.0):**

**`/orchestrate <task>`** - Execute complex multi-step tasks with forked context:
```
/orchestrate Refactor the authentication system to use JWT tokens
/orchestrate Add comprehensive error handling across all API endpoints
```
Benefits: Clean history (subtasks stay in fork), cost optimized (40-50% cheaper), better focus.

**`/router-analytics`** - Generate interactive HTML analytics dashboard:
```
/router-analytics
/router-analytics --output ~/Desktop/router-report.html
```
Generates charts for route distribution, daily/weekly trends, and cost savings.

**Error Recovery Commands (v2.0):**

**`/retry`** - Retry last query with an escalated model:
```
/retry              # Escalate to next tier
/retry deep         # Force escalation to Opus
/retry standard     # Force escalation to Sonnet
```
Use when: timeout/error, incomplete answer, wrong approach, need more depth.

**Plugin Integration Commands (v2.0):**

**`/router-plugins`** - Manage optional plugin integrations:
```
/router-plugins                     # List all plugins and status
/router-plugins enable <name>       # Enable integration
/router-plugins disable <name>      # Disable integration
```
Supported plugins: hookify, ralph-wiggum, code-review, feature-dev (all optional).

### Automatic vs Manual Routing

- **Automatic**: The UserPromptSubmit hook classifies every query and injects routing context
- **Manual Override**: Use `/route <model>` to bypass automatic classification and force a specific model (e.g., `/route opus` for complex reasoning, `/route haiku` for cost savings)

### CLAUDE.md Enforcement (Optional)

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

## Project Structure

```
claude-router/
├── .claude-plugin/                # Plugin files (marketplace distribution)
│   ├── agents/
│   │   ├── fast-executor.md       # Haiku agent
│   │   ├── standard-executor.md   # Sonnet agent
│   │   ├── deep-executor.md       # Opus agent
│   │   └── opus-orchestrator.md   # Opus orchestrator (v1.2)
│   ├── commands/                  # Slash command definitions
│   │   ├── route.md
│   │   ├── router-stats.md
│   │   ├── learn.md               # (v1.4)
│   │   ├── learn-on.md            # (v1.4)
│   │   ├── learn-off.md           # (v1.4)
│   │   ├── knowledge.md           # (v1.4)
│   │   ├── learn-reset.md         # (v1.4)
│   │   ├── orchestrate.md         # (v2.0)
│   │   ├── router-analytics.md    # (v2.0)
│   │   ├── retry.md               # (v2.0)
│   │   └── router-plugins.md      # (v2.0)
│   ├── hooks/
│   │   └── classify-prompt.py     # Hybrid classifier with multi-turn awareness
│   ├── skills/
│   │   ├── route/                 # Manual routing skill
│   │   ├── router-stats/          # Statistics skill
│   │   ├── learn/                 # Insight extraction (v1.4)
│   │   ├── learn-on/              # Enable continuous learning (v1.4)
│   │   ├── learn-off/             # Disable continuous learning (v1.4)
│   │   ├── knowledge/             # Knowledge base status (v1.4)
│   │   ├── learn-reset/           # Reset knowledge base (v1.4)
│   │   ├── orchestrate/           # Forked orchestration (v2.0)
│   │   ├── router-analytics/      # HTML dashboard (v2.0)
│   │   ├── retry/                 # Error recovery (v2.0)
│   │   └── router-plugins/        # Plugin management (v2.0)
│   └── plugin.json                # Plugin manifest
├── agents/                        # Source agent definitions
├── commands/                      # Source command definitions
├── hooks/                         # Source hook scripts
├── skills/                        # Source skills
└── knowledge/                     # Project knowledge base (v1.4)
    ├── cache/                     # Classification cache
    ├── learnings/                 # Persistent insights
    │   ├── patterns.md            # What works well
    │   ├── quirks.md              # Project oddities
    │   └── decisions.md           # Architectural decisions
    ├── context/                   # Session state
    └── state.json                 # Learning mode & plugin state
```

## Knowledge System (v1.4)

Claude Router includes a **persistent knowledge system** that gives you continuity across sessions and prevents context loss.

### The Intelligence Stack

```
┌─────────────────────────────────────────┐
│  KNOWLEDGE (Memory)                      │
│  Patterns, quirks, decisions             │
│  Survives sessions & compaction          │
└──────────────────┬──────────────────────┘
                   │ informs
┌──────────────────▼──────────────────────┐
│  ROUTING (Decision-Making)               │
│  Classification, caching, model selection│
└──────────────────┬──────────────────────┘
                   │ delegates to
┌──────────────────▼──────────────────────┐
│  AGENTS (Execution)                      │
│  fast, standard, deep, orchestrator      │
└──────────────────┬──────────────────────┘
                   │ use
┌──────────────────▼──────────────────────┐
│  SKILLS (Capabilities)                   │
│  /learn, /knowledge, /route, etc.        │
└─────────────────────────────────────────┘
```

Each layer makes the others smarter. Knowledge isn't standalone memory - it's integrated with routing so the system *acts* on what it learns.

### Why This Matters

**The Problem:** Every Claude Code session starts fresh. When you:
- End a session
- Hit context limits and get auto-compacted
- Come back the next day

...all the understanding Claude built up about your project is gone. You end up re-explaining the same quirks, patterns, and decisions over and over.

**Manual Workaround:** You could manually update `CLAUDE.md` with project notes, but:
- It's tedious to remember to do
- You have to manually extract insights from conversations
- Context often gets lost before you think to save it

**The Knowledge System:** Automatically captures and persists project understanding:

| What It Captures | Example | Why It Helps |
|------------------|---------|--------------|
| **Patterns** | "Error handling wraps async calls in try-catch with custom logger" | Future sessions know the codebase conventions |
| **Quirks** | "Auth service returns 200 even on errors - check response.success" | Avoids re-discovering gotchas |
| **Decisions** | "Chose TypeScript strict mode to catch bugs early" | Preserves rationale for future reference |

### How It Creates Continuity

```
Session 1: Discover auth quirk → /learn saves it
Session 2: Ask about auth → Claude already knows the quirk
Session 3: Debug auth issue → Context preserved from session 1
```

Without knowledge system:
```
Session 1: Discover auth quirk → Session ends, lost
Session 2: Re-discover auth quirk → Session ends, lost
Session 3: Re-discover auth quirk again → Frustrating loop
```

### Knowledge Commands

| Command | What It Does |
|---------|--------------|
| `/learn` | Extract insights from current conversation NOW |
| `/learn-on` | Enable continuous learning (auto-extracts every 10 queries) |
| `/learn-off` | Disable continuous learning |
| `/knowledge` | View knowledge base status and recent learnings |
| `/learn-reset` | Clear all knowledge and start fresh |

### Quick Start

```bash
# After a productive session where you discovered something useful:
/learn

# Or enable continuous learning for long sessions:
/learn-on

# Check what's been learned:
/knowledge
```

### Where It's Stored

Knowledge lives in `knowledge/learnings/` within your project:
- `patterns.md` - Approaches that work well
- `quirks.md` - Project-specific gotchas
- `decisions.md` - Architectural decisions with rationale

**Privacy:** Knowledge is gitignored by default (local only). To share with your team:
1. Edit `knowledge/.gitignore` to allow specific files
2. Commit the knowledge files you want to share

### Advanced: Informed Routing (Opt-in)

The knowledge system can inform routing decisions. If you've learned that "auth is complex in this project," queries about auth can be routed to Opus automatically.

To enable (conservative, off by default):
```bash
# Edit knowledge/state.json and set:
# "informed_routing": true
```

This is conservative by design - it requires strong signals (2+ keyword matches) and uses small confidence adjustments to avoid over-routing to expensive models.

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
4. **Easy override** - `/route <model>` to force any model when needed
5. **Learns from feedback** - Future: adjust routing based on user overrides

## Roadmap

### Completed
- [x] **Phase 1:** Rule-based classification (~0ms, $0)
- [x] **Phase 2:** Hybrid classification (rules + Haiku LLM fallback)
- [x] **Phase 3:** Standalone repository
- [x] **Phase 4:** Usage statistics and plugin distribution
  - `/router-stats` command with multiple value metrics
  - `/route <model>` command for manual model override
  - Plugin marketplace distribution
  - Subscriber benefits (extended limits, longer sessions)
- [x] **Phase 5:** Tool-Aware Routing & Hybrid Delegation (v1.2.0)
  - Tool-intensity pattern detection (file scanning, multi-file edits, test runs)
  - Opus Orchestrator mode for complex multi-step tasks
  - Smart delegation: Opus handles strategy, spawns Haiku/Sonnet for subtasks
  - Escalation paths: Sonnet can recommend Opus for architectural decisions
  - Enhanced cost tracking with delegation metrics (~40% additional savings)

- [x] **Phase 6:** Knowledge System (v1.4.0)
  - Persistent knowledge base that survives session boundaries and context compaction
  - `/learn` command for extracting insights from conversations
  - `/learn-on` / `/learn-off` for continuous learning mode
  - `/knowledge` to view accumulated project intelligence
  - Captures patterns, quirks, and decisions specific to each project

- [x] **Phase 7:** Performance, Context Forking & Multi-Turn Awareness (v2.0.0)
  - **Performance optimizations**: Pre-compiled regex (~10-15% faster), keyword caching, early exit, in-memory LRU cache
  - **Context forking**: `/orchestrate` for clean subtask isolation, `/router-analytics` for dashboard generation
  - **Multi-turn awareness**: Session state tracking, follow-up detection, context-aware confidence boost
  - **Error recovery**: `/retry` command for model escalation when queries fail or need more depth
  - **Plugin integration**: Optional integrations with official plugins (hookify, ralph-wiggum, code-review, feature-dev)
  - **Analytics dashboard**: `/router-analytics` generates interactive HTML charts

### Coming Soon
- **Phase 8:** Hookify Integration (v2.1.0)
  - Dynamic routing rule creation via hookify
  - Dual autonomy: both user and Claude can create rules
  - User: `/hookify "Always route auth questions to deep"`
  - Claude: Auto-suggest rules based on repeated escalation patterns
  - Learning-to-rules conversion (quirks → hookify rules)

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built for the Claude Code community** | [Report Issues](https://github.com/0xrdan/claude-router/issues) | [Follow @dannymonteiro on LinkedIn](https://linkedin.com/in/dannymonteiro)
