# Routing Rules

Claude Router automatically classifies queries and routes them to the optimal model.

## Fast Route (Haiku) - Simple queries

- Factual questions ("What is X?")
- Code formatting, linting
- Git status, log, diff
- JSON/YAML manipulation
- Regex generation
- Syntax questions

## Standard Route (Sonnet) - Typical coding + Tool-intensive tasks

- Bug fixes and feature implementation
- Code review and refactoring
- Test writing
- **Tool-intensive tasks** (v1.2): Codebase searches, running tests, multi-file edits
- **Orchestration tasks** (v1.2): Multi-step workflows

## Deep Route (Opus) - Complex tasks

- Architecture decisions
- Security audits
- Trade-off analysis
- Performance optimization
- System design

## Opus Orchestrator (v1.2) - Complex + Tool-intensive

When a query is both architecturally complex AND tool-intensive:
- Opus handles strategy and synthesis
- Delegates file reads/searches to Haiku
- Delegates implementations to Sonnet
- ~40% cost savings on complex workflows

---

## Example Output

**Simple query → Haiku:**
```
[Claude Router] MANDATORY ROUTING DIRECTIVE
Route: fast | Model: Haiku | Confidence: 90% | Method: rules
Signals: what is, json
```

**Tool-intensive query → Sonnet (v1.2):**
```
[Claude Router] MANDATORY ROUTING DIRECTIVE
Route: standard | Model: Sonnet | Confidence: 85% | Method: rules | Tool-intensive: Yes
Signals: find all, across the codebase
```

**Complex + Tool-intensive → Opus Orchestrator (v1.2):**
```
[Claude Router] MANDATORY ROUTING DIRECTIVE
Route: deep | Model: Opus (Orchestrator) | Confidence: 95% | Method: rules | Tool-intensive: Yes | Orchestration: Yes
Signals: architecture, refactor across the entire codebase
```

**Follow-up query with context awareness (v2.0):**
```
[Claude Router] MANDATORY ROUTING DIRECTIVE
Route: deep | Model: Opus | Confidence: 92% | Method: rules | Follow-up: Yes | Context boost: +0.1
Signals: follow-up to previous complex query
```

---

## How Classification Works

### Rule-Based Classification (Default)

Claude Router uses pattern matching to classify queries instantly:
- **Zero latency**: No API call needed
- **Zero cost**: All processing happens locally
- **High accuracy**: Patterns tuned for coding workflows

### Hybrid Classification (Optional)

For edge cases with low confidence, Claude Router can use Haiku LLM as a fallback:
- Only triggered when rule confidence < 70%
- Adds ~100ms latency
- Costs ~$0.001 per classification
- Significantly improves accuracy on ambiguous queries

To enable, set your API key:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```
