---
name: route
description: Manually route a query to the optimal Claude model (Haiku/Sonnet/Opus)
---

# /route Command

Manually route a query to the most cost-effective Claude model.

## Usage

```
/route <your query here>
```

## How It Works

1. Analyze the query from $ARGUMENTS
2. Classify complexity level (fast/standard/deep)
3. Spawn the appropriate executor subagent
4. Return the response with routing metadata

## Classification Rules

### fast (Haiku)
- Simple factual questions ("What is X?")
- Code formatting, linting
- Git operations: status, log, diff
- JSON/YAML manipulation
- Regex generation
- Syntax questions

### standard (Sonnet)
- Bug fixes
- Feature implementation
- Code review
- Refactoring
- Test writing
- Most typical coding tasks

### deep (Opus)
- Architecture decisions
- Security audits
- Multi-file refactors
- Trade-off analysis
- Performance optimization
- Complex debugging

## Instructions

Given the query in $ARGUMENTS:

1. **Classify** - Determine if it's fast, standard, or deep
2. **Explain** - State your classification and key signals
3. **Route** - Use the Task tool to spawn the appropriate subagent:
   - fast -> spawn "fast-executor" subagent
   - standard -> spawn "standard-executor" subagent
   - deep -> spawn "deep-executor" subagent
4. **Return** - Prefix the response with routing info

## Examples

```
/route What's the syntax for a TypeScript interface?
```
-> Routes to Haiku (fast)

```
/route Fix the authentication bug in login.ts
```
-> Routes to Sonnet (standard)

```
/route Design a scalable caching system for this API
```
-> Routes to Opus (deep)
