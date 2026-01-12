# Changelog

All notable changes to Claude Router will be documented in this file.

## [2.0.2] - 2026-01-12

### Changed
- **Marketplace migration**: Moved from `claude-router-marketplace` to centralized `0xrdan/claude-plugins`
- Added `/migrate-marketplace` command (temporary) to help users migrate
- Added daily deprecation warning for users on old marketplace
- Old marketplace will be removed in a future update

**Note:** This is a distribution change only. The plugin repo (`0xrdan/claude-router`) remains the same. Your settings and stats are preserved.

---

## [2.0.1] - 2026-01-12

### Fixed
- Renamed `ralph-wiggum` to `ralph-loop` across all references to match the official plugin name in the marketplace

---

## [2.0.0] - 2026-01-11

### Major Release - Performance, Context Forking, Multi-Turn Awareness

**Why this version is better:**

v2.0.0 is a comprehensive upgrade that makes Claude Router faster, smarter, and more integrated with the Claude Code ecosystem.

### Performance Optimizations (Phase 1)

- **Pre-compiled regex patterns**: All classification patterns now pre-compiled at module load (~10-15% faster)
- **Keyword caching**: mtime-based caching for learning keywords (avoids re-parsing files)
- **Early exit optimization**: Pattern matching short-circuits when sufficient signals found
- **In-memory cache**: LRU cache (50 entries) eliminates file I/O for repeated queries

### Context Forking Integration (Phase 2)

New skills that use Claude Code's context forking for clean subtask isolation:

| Command | Description |
|---------|-------------|
| `/orchestrate` | Execute complex multi-step tasks in forked context |
| `/router-analytics` | Generate HTML analytics dashboard in isolated context |
| `/learn --deep` | Thorough analysis with forked Explore agent |

Context forking keeps intermediate work isolated from your main conversation.

### Multi-Turn Context Awareness (Phase 3)

- **Session state tracking**: Remembers last route for 30 minutes
- **Follow-up detection**: Recognizes "and also", "what about", "yes, do that" patterns
- **Context boost**: Follow-ups to complex queries get confidence boost toward same route

### Error Recovery (Phase 4)

| Command | Description |
|---------|-------------|
| `/retry` | Retry last query with escalated model |
| `/retry deep` | Force escalation to Opus |

Agents now include escalation guidance when they encounter tasks beyond their capability.

### Analytics Dashboard (Phase 5)

- `/router-analytics` generates interactive HTML dashboards with:
  - Route distribution pie chart
  - Daily/weekly trends
  - Cost savings over time
  - Session comparison metrics

### Plugin Integration System

Optional integrations with official Claude Code plugins:

| Plugin | Integration |
|--------|-------------|
| hookify | Pattern-based behavior rules |
| ralph-loop | Iterative development loops |
| code-review | Multi-agent PR review |
| feature-dev | 7-phase feature development |

New command: `/router-plugins` to list and toggle integrations.

All plugins are **optional** - Claude Router works fully without them.

### Technical Details

- Knowledge state schema bumped to v2.0
- New session state file: `~/.claude/router-session.json`
- New plugin_integrations field in state.json
- 4 new skills, 4 new commands
- Updated agent definitions with escalation guidance

### Looking Ahead: v2.1.0

The plugin integration system in v2.0.0 sets the foundation for deeper integrations:

**Planned: Hookify Integration**
- Dynamic routing rule creation via hookify
- Dual autonomy: both user and Claude can create rules
- User: `/hookify "Always route auth questions to deep"`
- Claude: Auto-suggest rules based on repeated escalation patterns
- Learning-to-rules conversion (quirks → hookify rules)

**Documentation updates needed:**
- README update with new commands
- Individual command documentation review

---

## [1.4.0] - 2026-01-08

### Added - Knowledge System (Phase 6)

**Why this version is better:**

The previous versions made Claude Code smarter about routing queries to the right model. But every session started fresh - Claude had no memory of what it learned about your project. You'd discover a quirk in the auth system, session ends, and next time you're back to square one.

v1.4.0 introduces a **persistent knowledge system** that creates continuity across sessions.

**The Core Problem:**

```
Session 1: Discover auth quirk after 30 minutes of debugging
Session ends → Context lost

Session 2: Same auth quirk bites you again
Session ends → Context lost again

Session 3: "Why does this keep happening?"
```

**The Solution:**

```
Session 1: Discover auth quirk → /learn saves it
Session 2: Ask about auth → Claude already knows the quirk
Session 3: Continuity preserved, no re-discovery needed
```

### New Commands

| Command | Description |
|---------|-------------|
| `/learn` | Extract insights from current conversation (one-shot) |
| `/learn-on` | Enable continuous learning mode (auto-extracts every 10 queries) |
| `/learn-off` | Disable continuous learning mode |
| `/knowledge` | View knowledge base status and recent learnings |
| `/learn-reset` | Clear all knowledge and start fresh |

### What Gets Captured

The knowledge system captures three types of insights:

1. **Patterns** (`knowledge/learnings/patterns.md`)
   - Approaches that work well in your codebase
   - Example: "Error handling wraps async calls in try-catch with custom logger"

2. **Quirks** (`knowledge/learnings/quirks.md`)
   - Project-specific gotchas and non-standard behaviors
   - Example: "Auth service returns 200 even on errors - check response.success"

3. **Decisions** (`knowledge/learnings/decisions.md`)
   - Architectural choices with rationale
   - Example: "Chose Redis over in-memory cache for session storage because..."

### How It's Different from Manual CLAUDE.md Updates

| Manual Approach | Knowledge System |
|-----------------|------------------|
| Remember to update CLAUDE.md | Automatic extraction on `/learn` |
| Extract insights yourself | Claude analyzes conversation for you |
| Context often lost before you save | Continuous mode captures as you go |
| Single file, gets cluttered | Organized by type (patterns/quirks/decisions) |
| Hard to share selectively | Gitignored by default, opt-in sharing |

### Technical Features

**Classification Caching:**
- Similar queries are cached to avoid re-classification
- Fingerprint-based matching (not exact match)
- LRU eviction at 100 entries, 30-day TTL
- Cache hits shown in routing output

**Informed Routing (Opt-in):**
- Knowledge can influence routing decisions
- If quirks.md says "auth is complex," auth queries boost toward Opus
- Conservative by design: requires 2+ keyword matches, +0.1 confidence max
- Disabled by default, enable via `knowledge/state.json`

**Privacy:**
- Knowledge gitignored by default (local only)
- Edit `knowledge/.gitignore` to share with team
- Human-readable markdown files

### Directory Structure

```
knowledge/
├── cache/
│   └── classifications.md    # Query→route cache
├── learnings/
│   ├── patterns.md           # What works well
│   ├── quirks.md             # Project gotchas
│   └── decisions.md          # Architectural rationale
├── context/
│   └── session.md            # Session state
├── state.json                # Learning mode config
└── .gitignore                # Privacy (gitignored by default)
```

### Configuration

`knowledge/state.json` controls behavior:

```json
{
  "learning_mode": false,        // true when /learn-on active
  "informed_routing": false,     // Enable knowledge-informed routing
  "informed_routing_boost": 0.1, // Max confidence adjustment
  "extraction_threshold_queries": 10
}
```

---

## [1.3.0] - 2026-01-07

### Added
- Exception tracking for router transparency
- Stats now show when queries are classified but handled by Opus due to exceptions (router meta-questions)

---

## [1.2.0] - 2026-01-06

### Added - Tool-Aware Routing & Hybrid Delegation (Phase 5)

**Why this version is better:**

The previous version (1.1.1) routed queries based solely on *semantic complexity* - it looked at keywords like "architecture" or "security" to decide which model to use. This missed an important factor: **tool intensity**.

A query like "find all usages of getUserById across the codebase" seems simple semantically, but actually requires extensive tool use (grep, glob, file reads). v1.1.1 would route this to Haiku, which would struggle or fail.

**What's new:**

1. **Tool-Intensity Detection** - New pattern category detects queries that will need heavy tool use:
   - Codebase-wide searches ("find all", "search across")
   - Multi-file modifications ("update all files", "global rename")
   - Build/test execution ("run all tests", "build the project")
   - Dependency analysis ("what depends on", "import tree")

2. **Opus Orchestrator** - New agent for complex multi-step tasks that:
   - Decomposes tasks into subtasks
   - Delegates simple subtasks to Haiku/Sonnet (saves ~40% cost)
   - Handles complex decisions and synthesis itself
   - Coordinates multi-file changes

3. **Smart Delegation** - All executors can now delegate:
   - Opus/Sonnet can spawn Haiku for file reads, searches
   - Sonnet can escalate to Opus for architectural decisions

4. **Enhanced Cost Tracking** - New metrics in `/router-stats`:
   - Tool-intensive query count
   - Orchestrated query count
   - Delegation savings (separate from routing savings)

### Routing Changes

| Query Type | v1.1.1 | v1.2.0 |
|------------|--------|--------|
| "find all files that import X" | fast (Haiku) - often failed | standard (Sonnet) |
| "run all tests" | fast (Haiku) | standard (Sonnet) |
| "refactor auth system across codebase" | deep (Opus) | deep (Opus Orchestrator) with delegation |
| "what is JSON" | fast (Haiku) | fast (Haiku) - unchanged |

### Technical Details

- Stats schema bumped to v1.1 (backwards compatible)
- New `tool_intensive` and `orchestration` pattern categories
- New `opus-orchestrator` agent registered in plugin.json
- LLM classification prompt updated to consider tool intensity

---

## [1.1.1] - 2026-01-05

### Fixed
- Added Windows compatibility for file locking (replaced Unix-only `fcntl` with cross-platform solution)

---

## [1.1.0] - 2026-01-04

### Added
- Hybrid classification (rules + Haiku LLM fallback for low-confidence cases)
- `/router-stats` command for usage statistics
- `/route <model>` command for manual model override
- Plugin marketplace distribution

---

## [1.0.0] - 2026-01-03

### Added
- Initial release
- Rule-based classification with pattern matching
- Three-tier routing: fast (Haiku), standard (Sonnet), deep (Opus)
- Cost savings tracking
