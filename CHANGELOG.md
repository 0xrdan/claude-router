# Changelog

All notable changes to Claude Router will be documented in this file.

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
