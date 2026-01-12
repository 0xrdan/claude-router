---
name: route
description: Manually route a query to the optimal Claude model (Haiku/Sonnet/Opus)
---

# /route Command

Manually route a query to the most cost-effective Claude model.

## Usage

```
/route <query>                    # Auto-classify by complexity
/route <model> <query>            # Force specific model
```

Models: `haiku`/`fast`, `sonnet`/`standard`, `opus`/`deep`

## How It Works

1. Check if first word of $ARGUMENTS is a model name (case-insensitive)
2. **If model specified**: Use that model. No classification. No override.
3. **If no model**: Classify complexity and route accordingly
4. Spawn the appropriate executor subagent
5. Return the response with routing metadata

**CRITICAL: When user specifies a model, honor it unconditionally.**

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

Given $ARGUMENTS:

1. **Check for explicit model** - Is first word haiku/fast/sonnet/standard/opus/deep (case-insensitive)?
   - **YES**: Extract model, rest is query. **USE THAT MODEL. DO NOT CLASSIFY.**
   - **NO**: Entire argument is query, proceed to classification
2. **Classify** (only if no explicit model) - Determine if it's fast, standard, or deep
3. **Route** - Use the Task tool to spawn the appropriate subagent:
   - haiku/fast -> spawn "fast-executor" subagent
   - sonnet/standard -> spawn "standard-executor" subagent
   - opus/deep -> spawn "deep-executor" subagent
4. **Return** - Prefix the response with routing info

**DO NOT override explicit model choices. The user's selection is final.**

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
