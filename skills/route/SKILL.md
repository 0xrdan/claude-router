---
name: route
description: Route queries to optimal Claude model (Haiku/Sonnet/Opus) based on complexity. Use when user wants cost-optimized model selection.
---

# Query Router

Routes queries to the most cost-effective Claude model while maintaining quality.

## How It Works

1. Analyze the query from $ARGUMENTS
2. Classify complexity level
3. Spawn the appropriate executor subagent
4. Return the response with routing metadata

## Classification Rules

### fast (use fast-executor -> Haiku)
Indicators:
- Simple factual questions ("What is X?", "How do I Y?")
- Code formatting, linting, prettifying
- Git operations: status, log, diff, add, commit
- JSON/YAML manipulation
- Regex generation
- File lookups and simple reads
- Syntax questions

### standard (use standard-executor -> Sonnet)
Indicators:
- Bug fixes ("fix", "error", "broken", "issue")
- Feature implementation ("add", "implement", "create")
- Code review
- Refactoring ("refactor", "clean up", "improve")
- Test writing
- Documentation updates
- Most typical coding tasks

### deep (use deep-executor -> Opus)
Indicators:
- Architecture decisions ("architect", "design", "system")
- Security audits ("security", "vulnerability", "audit")
- Multi-file refactors ("across", "multiple files", "all components")
- Trade-off analysis ("compare", "pros and cons", "trade-offs")
- Performance optimization analysis
- Complex debugging requiring deep reasoning
- Extended thinking tasks

## Instructions

Given the query in $ARGUMENTS:

1. **Classify** - Determine if it's fast, standard, or deep based on the rules above
2. **Explain** - Briefly state your classification and the key signals
3. **Route** - Use the Task tool to spawn the appropriate subagent:
   - fast -> spawn "fast-executor" subagent
   - standard -> spawn "standard-executor" subagent
   - deep -> spawn "deep-executor" subagent
4. **Return** - Prefix the response with the routing info

## Example Usage

User: `/route What's the syntax for a TypeScript interface?`

Classification: **fast**
Signals: Simple syntax question, factual lookup
Routing to: Haiku (fast-executor)

[Spawns fast-executor with the query]

---

User: `/route Fix the authentication bug in login.ts`

Classification: **standard**
Signals: Bug fix, single file, typical coding task
Routing to: Sonnet (standard-executor)

[Spawns standard-executor with the query]

---

User: `/route Design a scalable caching system for this API`

Classification: **deep**
Signals: Architecture decision, system design, trade-offs
Routing to: Opus (deep-executor)

[Spawns deep-executor with the query]
