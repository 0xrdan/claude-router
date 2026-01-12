# Knowledge System (v1.4)

Claude Router includes a **persistent knowledge system** that gives you continuity across sessions and prevents context loss.

## The Intelligence Stack

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

---

## Why This Matters

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

---

## How It Creates Continuity

**With knowledge system:**
```
Session 1: Discover auth quirk → /learn saves it
Session 2: Ask about auth → Claude already knows the quirk
Session 3: Debug auth issue → Context preserved from session 1
```

**Without knowledge system:**
```
Session 1: Discover auth quirk → Session ends, lost
Session 2: Re-discover auth quirk → Session ends, lost
Session 3: Re-discover auth quirk again → Frustrating loop
```

---

## Knowledge Commands

| Command | What It Does |
|---------|--------------|
| `/learn` | Extract insights from current conversation NOW |
| `/learn-on` | Enable continuous learning (auto-extracts every 10 queries) |
| `/learn-off` | Disable continuous learning |
| `/knowledge` | View knowledge base status and recent learnings |
| `/learn-reset` | Clear all knowledge and start fresh |

---

## Quick Start

```bash
# After a productive session where you discovered something useful:
/learn

# Or enable continuous learning for long sessions:
/learn-on

# Check what's been learned:
/knowledge
```

---

## Where It's Stored

Knowledge lives in `knowledge/learnings/` within your project:
- `patterns.md` - Approaches that work well
- `quirks.md` - Project-specific gotchas
- `decisions.md` - Architectural decisions with rationale

**Privacy:** Knowledge is gitignored by default (local only). To share with your team:
1. Edit `knowledge/.gitignore` to allow specific files
2. Commit the knowledge files you want to share

---

## Advanced: Informed Routing (Opt-in)

The knowledge system can inform routing decisions. If you've learned that "auth is complex in this project," queries about auth can be routed to Opus automatically.

To enable (conservative, off by default):
```bash
# Edit knowledge/state.json and set:
# "informed_routing": true
```

This is conservative by design - it requires strong signals (2+ keyword matches) and uses small confidence adjustments to avoid over-routing to expensive models.

---

## Configuration

`knowledge/state.json` controls behavior:

```json
{
  "learning_mode": false,
  "informed_routing": false,
  "informed_routing_boost": 0.1,
  "extraction_threshold_queries": 10
}
```

| Setting | Description | Default |
|---------|-------------|---------|
| `learning_mode` | Auto-extract insights periodically | `false` |
| `informed_routing` | Let knowledge influence routing | `false` |
| `informed_routing_boost` | Max confidence adjustment | `0.1` |
| `extraction_threshold_queries` | Queries between auto-extractions | `10` |
