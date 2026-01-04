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
