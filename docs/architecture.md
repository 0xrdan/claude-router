# Project Architecture

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
├── docs/                          # Documentation
└── knowledge/                     # Project knowledge base (v1.4)
    ├── cache/                     # Classification cache
    ├── learnings/                 # Persistent insights
    │   ├── patterns.md            # What works well
    │   ├── quirks.md              # Project oddities
    │   └── decisions.md           # Architectural decisions
    ├── context/                   # Session state
    └── state.json                 # Learning mode & plugin state
```

---

## Core Components

### UserPromptSubmit Hook (`hooks/classify-prompt.py`)

The heart of Claude Router. This hook:
1. Intercepts every user query before Claude processes it
2. Classifies the query using rule-based patterns (+ optional Haiku LLM fallback)
3. Injects a routing directive that triggers the appropriate subagent

**Key features (v2.0):**
- Pre-compiled regex patterns for speed
- In-memory LRU cache for repeated queries
- Session state tracking for multi-turn awareness
- Follow-up query detection
- Plugin detection system

### Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `fast-executor` | Haiku | Simple queries, lookups, formatting |
| `standard-executor` | Sonnet | Typical coding tasks, tool-intensive work |
| `deep-executor` | Opus | Complex architecture, security, trade-offs |
| `opus-orchestrator` | Opus | Complex multi-step tasks with delegation |

### Skills

Skills implement the actual functionality behind slash commands:

| Skill | Command | Description |
|-------|---------|-------------|
| `route` | `/route` | Manual model override |
| `router-stats` | `/router-stats` | Usage statistics |
| `learn` | `/learn` | Extract insights |
| `knowledge` | `/knowledge` | View knowledge base |
| `orchestrate` | `/orchestrate` | Forked task execution |
| `router-analytics` | `/router-analytics` | HTML dashboard |
| `retry` | `/retry` | Error recovery |
| `router-plugins` | `/router-plugins` | Plugin management |

---

## Data Flow

```
User Query
    │
    ▼
┌─────────────────────────────────┐
│  UserPromptSubmit Hook          │
│  (classify-prompt.py)           │
├─────────────────────────────────┤
│  1. Check in-memory cache       │
│  2. Check file cache            │
│  3. Rule-based classification   │
│  4. LLM fallback (if needed)    │
│  5. Session state update        │
│  6. Inject routing directive    │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  Claude Code (Main)             │
│  Sees: [Claude Router] MANDATORY│
│  ROUTING DIRECTIVE              │
├─────────────────────────────────┤
│  Spawns appropriate subagent    │
│  via Task tool                  │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  Subagent (Haiku/Sonnet/Opus)   │
│  Executes the actual task       │
└─────────────────────────────────┘
    │
    ▼
Response to User
```

---

## State Files

### `~/.claude/router-stats.json`
Global routing statistics across all projects.

### `~/.claude/router-session.json`
Session state for multi-turn context awareness.

### `knowledge/state.json`
Per-project learning mode and plugin configuration.

### `knowledge/cache/classifications.md`
Per-project classification cache.
