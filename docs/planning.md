# Claude Router Plugin for Claude Code

Planning document for a Claude Code plugin that intelligently routes queries to the optimal Claude model based on complexity.

## What Makes This Novel

This project fills a gap that no existing tool addresses:

| What Exists | What Claude Router Does |
|-------------|-------------------------|
| Multi-provider routers (OpenRouter, etc.) | **Intra-Claude optimization** (Haiku/Sonnet/Opus) |
| Manual `/model` switching | **Automatic routing** via UserPromptSubmit hook |
| Generic LLM complexity scoring | **Coding-task specific** pattern recognition |
| External API wrapper approach | **Native Claude Code integration** using subagents |

### Why This Matters

1. **First of its kind** - No existing tool optimizes routing *within* the Claude model family for coding workflows
2. **Native integration** - Uses Claude Code's own subagent system, not external wrappers
3. **Zero-overhead classification** - Rule-based patterns mean instant, free routing decisions
4. **Significant cost savings** - 98% reduction on simple queries (Haiku vs Opus)

### Key Metrics (Phase 1)

| Metric | Value |
|--------|-------|
| Classification latency | ~0ms (rule-based) |
| Classification cost | $0 (no API call) |
| Subagent token overhead | 3.4k tokens (optimized from 11.9k) |
| Cost savings (simple queries) | ~98% (Haiku vs Opus) |
| Cost savings (mixed workload) | Est. 50-70% |

### Technical Achievements

1. **Discovered the right architecture** - Researched hooks, MCP, and subagents to find the only viable approach
2. **Solved the hook integration** - UserPromptSubmit hook injects routing context that triggers subagent spawning
3. **Optimized token overhead** - Minimal agent definitions reduced overhead by 70%
4. **Built hybrid classification design** - Rule-based for speed, LLM fallback for accuracy

## Concept

Route queries to the most cost-effective Claude model while maintaining quality:

| Route | Model | Use Case | Cost (per 1M tokens) |
|-------|-------|----------|---------------------|
| fast | Haiku | Simple questions, lookups, formatting | $0.25 / $1.25 |
| standard | Sonnet | Most coding tasks, analysis | $3 / $15 |
| deep | Opus | Complex architecture, multi-step reasoning | $15 / $75 |

**Goal:** Reduce costs by 50-70% by avoiding Opus for queries that don't need it.

## What Exists Today

| Solution | Limitation |
|----------|------------|
| Claude Code `--model` flag | Manual selection, user must know which model fits |
| Default to Sonnet | Overpays for simple tasks, underpowered for complex ones |
| Always use Opus | 5x cost for same results on routine queries |
| Generic LLM routers | Multi-provider focus, not optimized for Claude model family |

**Gap:** No tool specifically optimizes routing *within* the Claude model family for coding workflows.

## Why This Would Be Valuable

### For Users
1. **Automatic cost optimization** - Don't think about which model, just ask
2. **No quality sacrifice** - Complex queries still get Opus
3. **Transparency** - See exactly why a model was chosen
4. **Learning** - Understand what makes a query "complex"

### For Anthropic (Why They'd Care)
1. **Validates their model lineup** - Proves Haiku/Sonnet/Opus tiering works in practice
2. **Real usage data** - What % of coding queries actually need Opus?
3. **Adoption driver** - Lower effective cost → more Claude Code usage
4. **Reference implementation** - Could inform native routing features
5. **Community showcase** - Open source tool built *for* their ecosystem

### Differentiation from ai-orchestrator
| ai-orchestrator | Claude Router |
|-----------------|---------------|
| Multi-provider (Claude, GPT, Gemini) | Claude-only (Haiku, Sonnet, Opus) |
| General LLM routing | Coding-task optimized |
| Fallback = different provider | Fallback = different Claude tier |
| Generic complexity signals | Claude Code workflow signals |

## What Would Make People Actually Use It

1. **Zero-config start** - Works immediately with sensible defaults
2. **Visible savings** - Show "You saved $X this session" prominently
3. **Trust through transparency** - Explain every routing decision
4. **Easy override** - `/opus` or `/haiku` to force when needed
5. **Learns from feedback** - If user overrides, adjust future routing
6. **Publishable stats** - "I saved 73% on Claude Code this month" screenshots

## Unique Features (Not in ai-orchestrator)

### 1. Coding-Specific Signals
```typescript
// Detect coding patterns that influence routing
const codingSignals = {
  // Fast (Haiku)
  singleFileEdit: /edit (this|the) file/i,
  simpleGitOp: /git (status|log|diff|add|commit)/i,
  formatRequest: /(format|lint|prettify)/i,

  // Standard (Sonnet)
  bugFix: /(fix|bug|error|issue|broken)/i,
  addFeature: /add (a|the)? ?\w+ (to|for|in)/i,
  refactor: /(refactor|clean up|improve)/i,

  // Deep (Opus)
  architecture: /(architect|design|system|scalab)/i,
  multiFile: /(across|multiple|all) (files|components)/i,
  tradeoffs: /(trade-?off|compare|pros? (and|&) cons?)/i,
  security: /(security|vulnerabil|audit|penetration)/i,
};
```

### 2. Context-Aware Routing
```typescript
// Factor in conversation context, not just the query
interface ContextSignals {
  filesOpen: number;        // Many files → likely complex
  recentToolCalls: string[]; // Pattern of tool usage
  sessionDuration: number;  // Long session → may need Opus stamina
  errorCount: number;       // Many errors → escalate to Opus
}
```

### 3. Feedback Loop
```typescript
// Learn from user overrides
interface RoutingFeedback {
  query: string;
  suggestedRoute: Route;
  userOverride?: Route;
  wasHelpful: boolean;  // Did they need to re-ask?
}

// Over time: "Queries like X should go to Opus, not Sonnet"
```

### 4. Team/Project Profiles
```typescript
// Different projects have different complexity profiles
interface ProjectProfile {
  name: string;
  defaultRoute: Route;
  routeWeights: {
    fast: number;      // e.g., 0.2 for a complex codebase
    standard: number;  // e.g., 0.5
    deep: number;      // e.g., 0.3
  };
}
```

## Architecture

### Current Implementation (Phase 1)

```
┌─────────────────────────────────────────────────────────┐
│                     Claude Code Session                  │
│                                                          │
│  User submits any query                                  │
│           │                                              │
│           ▼                                              │
│  ┌─────────────────────────────────────────────────┐    │
│  │         UserPromptSubmit Hook                    │    │
│  │         (classify-prompt.py)                     │    │
│  │                                                  │    │
│  │  • Rule-based pattern matching                   │    │
│  │  • Instant classification (0ms)                  │    │
│  │  • Zero API cost                                 │    │
│  │  • Injects routing context                       │    │
│  └─────────────────────────────────────────────────┘    │
│           │                                              │
│           ▼                                              │
│  ┌─────────────────────────────────────────────────┐    │
│  │         Main Model (sees routing context)        │    │
│  │                                                  │    │
│  │  "[Claude Router] Route: fast | Model: Haiku"    │    │
│  │  "Spawn the fast-executor subagent..."           │    │
│  └─────────────────────────────────────────────────┘    │
│           │                                              │
│           ▼                                              │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Subagents                           │    │
│  │                                                  │    │
│  │  ┌─────────┐  ┌───────────┐  ┌─────────┐        │    │
│  │  │  fast   │  │ standard  │  │  deep   │        │    │
│  │  │ (Haiku) │  │ (Sonnet)  │  │ (Opus)  │        │    │
│  │  │ 3.4k tk │  │           │  │         │        │    │
│  │  └─────────┘  └───────────┘  └─────────┘        │    │
│  │                                                  │    │
│  └─────────────────────────────────────────────────┘    │
│           │                                              │
│           ▼                                              │
│  Response returned to user                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Planned: Hybrid Classification (Phase 2)

```
┌─────────────────────────────────────────────────────────┐
│                     Classification Flow                  │
│                                                          │
│  User query                                              │
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────────┐                                   │
│  │  Rule-based      │──── High confidence ────▶ Route   │
│  │  (~0ms, $0)      │     (≥70%)                        │
│  └────────┬─────────┘                                   │
│           │                                              │
│           │ Low confidence (<70%)                        │
│           ▼                                              │
│  ┌──────────────────┐                                   │
│  │  Haiku LLM       │──── Classification ────▶ Route    │
│  │  (~100ms, $0.001)│                                   │
│  └──────────────────┘                                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Routing Signals

### Fast Route (Haiku)
- Simple factual questions ("What is X?")
- Code formatting/linting requests
- Short file reads
- Git status/diff summaries
- Regex generation
- JSON/YAML manipulation

### Standard Route (Sonnet)
- Most coding tasks
- Bug fixes
- Feature implementation
- Code review
- Refactoring
- Test writing

### Deep Route (Opus)
- Architecture decisions
- Complex multi-file refactors
- Security audits
- Performance optimization analysis
- "Compare", "analyze trade-offs", "design system for"
- Extended thinking required

## Implementation Options

### ~~Option 1: MCP Server~~ ❌ Not Viable

MCP tools cannot influence model selection. Would require separate API calls, doubling costs and breaking the natural conversation flow.

### ~~Option 2: Claude Code Hook~~ ❌ Not Viable

Hooks cannot change which model handles responses. Model selection is CLI/config only.

### Option 3: Custom Skill + Subagents ✅ Recommended

Create a `/route` skill that:
1. Classifies the query (rule-based + optional Haiku LLM)
2. Spawns the appropriate subagent with the right model
3. Returns the response with routing metadata

```
/route How do I implement authentication?
# → Classifies as "standard"
# → Spawns sonnet subagent
# → Returns response with "[Routed to Sonnet]"
```

**Pros:**
- Native Claude Code integration
- Leverages existing subagent infrastructure
- No external dependencies
- Easy to install (just a skill file)

**Cons:**
- Requires user to invoke `/route` explicitly
- Could add `/route` hook on UserPromptSubmit to suggest routing

### Option 4: Wrapper CLI ⚠️ Alternative

Still viable but less integrated. Consider only if subagent approach has limitations.

## Recommended Approach

**Custom Skill + Subagents** because:
1. Uses native Claude Code features (subagents with model selection)
2. Zero external dependencies
3. Easy distribution (single skill file or small package)
4. Can evolve: add UserPromptSubmit hook to auto-suggest routing

## Components to Build

### 1. Skill File: `/route`

The main entry point - a Claude Code skill that handles classification and routing:

```markdown
---
name: route
description: Route query to optimal Claude model based on complexity
allowed_tools: Task
---
You are a query router. Classify the user's query and spawn the appropriate subagent.

Query: $ARGUMENTS

## Classification Rules

**fast** (spawn fast-executor with Haiku):
- Simple factual questions
- Code formatting, linting
- Git status, log, diff
- JSON/YAML manipulation
- Regex generation

**standard** (spawn standard-executor with Sonnet):
- Bug fixes
- Feature implementation
- Code review
- Refactoring
- Test writing

**deep** (spawn deep-executor with Opus):
- Architecture decisions
- Security audits
- Multi-file refactors
- Trade-off analysis
- Complex reasoning

## Output Format

1. State your classification: "Classification: [fast|standard|deep]"
2. List signals that influenced the decision
3. Spawn the appropriate subagent with the query
4. Return the response prefixed with "[Routed to <Model>]"
```

### 2. Subagent Files

Three subagents with different model assignments:

**`fast-executor.md`**
```markdown
---
name: fast-executor
model: haiku
---
You handle simple, quick tasks efficiently.
```

**`standard-executor.md`**
```markdown
---
name: standard-executor
model: sonnet
---
You handle typical coding tasks with good balance of speed and quality.
```

**`deep-executor.md`**
```markdown
---
name: deep-executor
model: opus
---
You handle complex tasks requiring deep reasoning and analysis.
```

### 3. Cost Tracker (Phase 2)

```typescript
interface RoutingLog {
  timestamp: string;
  query: string;
  route: 'fast' | 'standard' | 'deep';
  signals: string[];
}

// Stored in ~/.claude/router-stats.json
interface RouterStats {
  logs: RoutingLog[];
  summary: {
    fast: number;
    standard: number;
    deep: number;
  };
}
```

## User Experience

### Transparent Mode (Recommended)
```
User: How do I add a button to this component?
[Router: standard → Sonnet]
Claude: Here's how to add a button...

User: Design a scalable authentication system for this app
[Router: deep → Opus]
Claude: Let me think through this architecture...
```

### Verbose Mode
```
User: How do I add a button?
[Router] Classified as: standard (confidence: 0.89)
[Router] Signals: single-file change, UI component, straightforward
[Router] Routing to: claude-sonnet-4
[Router] Estimated cost: $0.003 (vs $0.015 with Opus)
Claude: Here's how to add a button...
```

### Stats Command
```
/router-stats

Claude Router Statistics
────────────────────────
Total queries: 47
  Fast (Haiku):    12 (26%)
  Standard (Sonnet): 31 (66%)
  Deep (Opus):      4 (8%)

Cost Analysis
  Actual cost:     $0.42
  All-Opus cost:   $1.89
  Savings:         $1.47 (78%)
```

## Development Phases

### Phase 1: Minimal Viable Product ✅ COMPLETE

**What We Built:**

Instead of a manual `/route` skill, we implemented **automatic routing via UserPromptSubmit hook**:

```
User query → Hook classifies (instant, free) → Context injected → Subagent spawns
```

**Deliverables (Complete):**
- [x] `UserPromptSubmit` hook with rule-based classifier
- [x] Three optimized subagents (fast/standard/deep)
- [x] Automatic routing on every prompt
- [x] Routing context displayed to user

**Files Created:**
```
.claude/
├── settings.json              # Hook configuration
├── hooks/
│   ├── classify-prompt.py     # Rule-based classifier
│   └── venv/                  # Python dependencies
├── agents/
│   ├── fast-executor/AGENT.md    # Haiku
│   ├── standard-executor/AGENT.md # Sonnet
│   └── deep-executor/AGENT.md    # Opus
└── skills/
    └── route/SKILL.md         # Manual /route skill (backup)
```

**Key Findings:**
- Rule-based classification: ~0ms, zero cost
- Subagent token overhead: ~3.4k tokens (optimized from 11.9k)
- Even with overhead, Haiku routing saves ~98% vs Opus for simple queries

**Classification Patterns Implemented:**
```python
PATTERNS = {
    "fast": [
        r"^what (is|are|does) ",
        r"^how (do|does|to) ",
        r"\b(format|lint|prettify)\b",
        r"\bgit (status|log|diff|add|commit)\b",
        r"\b(json|yaml)\b",
        r"\bregex\b",
        r"\bsyntax\b",
    ],
    "deep": [
        r"\b(architect|architecture|design pattern)\b",
        r"\bscalable?\b",
        r"\b(security|vulnerab|audit)\b",
        r"\b(across|multiple|all) (files?|components?)\b",
        r"\b(trade-?off|compare|pros? (and|&) cons?)\b",
        r"\b(complex|intricate|sophisticated)\b",
    ],
}
# Default: standard (Sonnet)
```

### Phase 2: Hybrid Classification ✅ COMPLETE

Combines rule-based speed with LLM accuracy for edge cases:

**How It Works:**
```python
def classify_hybrid(prompt):
    # 1. Try rule-based first (instant, free)
    result = classify_by_rules(prompt)

    # 2. If low confidence (<70%), use Haiku LLM (~$0.001)
    if result["confidence"] < 0.7:
        llm_result = classify_by_haiku(prompt)
        if llm_result:
            return llm_result

    return result
```

**Benefits Realized:**
- Clear patterns: Rule-based (0ms, $0)
- Ambiguous queries: Haiku LLM (~100ms, ~$0.001)
- Best of both worlds

**Example:**
```
Query: "Design a rate limiting system with Redis for our API endpoints"

Before (rules only): standard (50% confidence) ❌
After (hybrid):      deep (95% confidence via haiku-llm) ✅
```

**Deliverables (Complete):**
- [x] Hybrid classifier with 70% confidence threshold
- [x] API key from environment or server/.env
- [x] Method shown in output (rules vs haiku-llm)
- [x] Authoritative routing directive (ACTION REQUIRED)
- [x] All three routes tested and working

### Phase 3: Standalone Repository (Next)

Extract to dedicated repo for portfolio visibility and community distribution:

**Repo Structure:**
```
claude-router/
├── README.md              # Hero doc - problem, install, demo, metrics
├── LICENSE                # MIT
├── install.sh             # One-command setup script
├── .claude/
│   ├── settings.json      # Hook configuration
│   ├── hooks/
│   │   └── classify-prompt.py
│   └── agents/
│       ├── fast-executor/AGENT.md
│       ├── standard-executor/AGENT.md
│       └── deep-executor/AGENT.md
└── docs/
    ├── planning.md        # This detailed planning doc
    └── CONTRIBUTING.md    # How to contribute
```

**README Sections:**
- Problem statement (the gap in the market)
- One-command install: `curl -sSL .../install.sh | bash`
- Demo GIF showing routing in action
- Key metrics table (98% savings, 0ms latency, 3.4k tokens)
- How it works (architecture diagram)
- Configuration options
- Roadmap / contributing

**Deliverables:**
- [ ] Create GitHub repo (`claude-router` or `claude-code-router`)
- [ ] One-command install script
- [ ] Compelling README with demo
- [ ] GitHub release with proper versioning
- [ ] Share on relevant communities (Claude Discord, HN, Reddit)
- [ ] Blog post / demo video for visibility

### Phase 4: Stats Tracking (First Feature PR)

Add after standalone repo is live - demonstrates active development:

**Features:**
- [ ] Persist routing decisions to `~/.claude/router-stats.json`
- [ ] `/router-stats` skill to show savings
- [ ] Session stats: "You saved $X this session"
- [ ] Cumulative stats: "Total savings this month: $XX (73%)"

**Why This Matters:**
- "You saved 73% on Claude Code" screenshots drive adoption
- Shows the repo is actively maintained
- Concrete value prop for README

## Technical Research Findings (January 2026)

### Hooks: Cannot Switch Models ❌

Claude Code hooks can:
- ✅ Add context to prompts (`additionalContext`)
- ✅ Block/allow/modify tool calls (`updatedInput`)
- ✅ Inject system messages
- ❌ **Cannot change which model handles the response**

From documentation: "Model selection is controlled via configuration files and CLI flags, not hooks."

### MCP Tools: Wrong Architecture ❌

MCP tools are data/tool providers, not model controllers:
- ❌ Cannot change the active model in a Claude Code session
- ⚠️ Could make separate API calls, but this is problematic:
  - Double API costs (main model + routed model)
  - Response comes back as tool output, not model replacement
  - Breaks MCP design principles
  - Loses context awareness

### Subagents: Native Solution ✅

Claude Code has built-in model routing via **subagents**:

```markdown
---
name: fast-task
model: haiku
---
You're optimized for fast, lightweight tasks.
```

Subagents can specify `model: haiku`, `model: sonnet`, `model: opus`, or `inherit`.

This is the correct architecture: **Custom Skill → Classifier → Appropriate Subagent**

### What Exists in the Market

| Solution | What It Does | Gap |
|----------|--------------|-----|
| Manual `/model` switching | User decides | Requires knowing which model fits |
| `opusplan` mode | Opus for planning → Sonnet for execution | Binary, not query-by-query |
| claude-code-router | Routes to *other providers* (OpenRouter, DeepSeek) | Multi-provider, not intra-Claude |
| VS Code Copilot auto-select | Routes between GPT/Claude/etc | Copilot-only, not Claude Code |

**Gap confirmed:** No automatic intra-Claude routing for coding workflows exists.

## Open Questions

- [x] Does Claude Code's hook system allow model selection? **No**
- [x] Can MCP tools influence which model handles the response? **No (wrong architecture)**
- [ ] Should we cache classifications for similar queries?
- [x] How to handle streaming responses across models? **Subagents handle this natively**
- [ ] Should context window size influence routing? (large context → Opus?)
- [x] What's the latency overhead of Haiku classification? **~0ms for rule-based; ~100ms for LLM**
- [x] How accurate is rule-based vs LLM classification for coding queries? **Rule-based works well for clear patterns; LLM needed for edge cases (hybrid approach)**
- [x] What's the subagent token overhead? **~3.4k tokens with minimal agent definitions**
- [ ] How to access Claude API for hybrid classification? (OAuth tokens don't work as API keys)
- [ ] Should the router respect user's current model preference?

## Related

- [ai-orchestrator](https://github.com/0xrdan/ai-orchestrator) - Base routing logic (multi-provider)
- [mcp-rag-server](https://github.com/0xrdan/mcp-rag-server) - MCP server reference
- [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents.md) - Native model routing
- [Claude Code Model Config](https://code.claude.com/docs/en/model-config.md) - Model selection options

---

## Changelog

### January 3, 2026 - Phase 2 Complete
- Implemented hybrid classification (rules + Haiku LLM fallback)
- Added authoritative routing directive ("ACTION REQUIRED")
- Fixed routing enforcement - subagents now spawn correctly
- Tested all three routes successfully in single session
- API key reads from environment or server/.env

### January 3, 2026 - Phase 1 Complete
- Implemented UserPromptSubmit hook with rule-based classifier
- Created three optimized subagents (fast/standard/deep)
- Reduced token overhead from 11.9k to 3.4k through minimal agent definitions
- Validated routing works: queries correctly classified and routed
- Documented hybrid approach for Phase 2

### January 2, 2026 - Research Complete
- Confirmed hooks cannot switch models directly
- Confirmed MCP is wrong architecture for this use case
- Discovered subagents as the native solution
- Validated market gap exists (no intra-Claude router)

---

*Last updated: January 3, 2026*
*Status: Phase 2 Complete - Hybrid classification working*
*Next: Phase 3 (standalone repo) → Phase 4 (stats tracking as first feature PR)*
