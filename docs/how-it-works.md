# How Claude Router Works

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

---

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
