## Claude Router Enforcement

When you receive a `[Claude Router] MANDATORY ROUTING DIRECTIVE`, you MUST:

1. Use the Task tool IMMEDIATELY to spawn the specified subagent
2. Do NOT respond to the user directly - delegate to the subagent
3. Pass the user's original query in the prompt parameter

Subagent mapping:
- fast → `claude-router:fast-executor`
- standard → `claude-router:standard-executor`
- deep → `claude-router:deep-executor`

Exceptions: Slash commands (`/route`, `/router-stats`, `/learn`, `/learn-on`, `/learn-off`, `/learn-reset`, `/knowledge`) and questions about the router itself.

## Project Knowledge

The `/knowledge/learnings/` directory contains accumulated project insights:
- `patterns.md` - Approaches that work well in this project
- `quirks.md` - Project-specific oddities and gotchas
- `decisions.md` - Architectural decisions with rationale

Reference these when making implementation decisions. Use `/knowledge` to see current status.
