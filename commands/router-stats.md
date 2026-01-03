---
name: router-stats
description: Display Claude Router usage statistics and cost savings (global across all projects)
---

# /router-stats Command

Display usage statistics and estimated cost savings from Claude Router.

**Note:** Stats are global - they track routing across all your projects.

## Usage

```
/router-stats
```

## Instructions

1. Read the stats file at `~/.claude/router-stats.json`
2. If the file doesn't exist, inform the user that no stats are available yet
3. Calculate percentages for route distribution
4. Calculate **optimization rate**: percentage of queries routed to Haiku or Sonnet instead of Opus
5. Format and display the statistics

## Data Format

The stats file contains:
```json
{
  "version": "1.0",
  "total_queries": 100,
  "routes": {"fast": 30, "standard": 60, "deep": 10},
  "estimated_savings": 12.50,
  "sessions": [
    {
      "date": "2026-01-03",
      "queries": 25,
      "routes": {"fast": 8, "standard": 15, "deep": 2},
      "savings": 3.20
    }
  ],
  "last_updated": "2026-01-03T15:30:00"
}
```

## Output Format

Present the stats like this:

```
Claude Router Statistics (Global)
==================================

All Time
--------
Total Queries Routed: 100
Optimization Rate: 90% (queries routed to cheaper models)

Route Distribution:
  Fast (Haiku):      30 (30%)
  Standard (Sonnet): 60 (60%)
  Deep (Opus):       10 (10%)

Value Metrics:
  Estimated Savings: $12.50 (vs always using Opus)
  Avg Cost per Query: $0.04 (vs $0.165 with Opus)

Today
-----
Queries: 25
Savings: $3.20
Routes: Fast 8 | Standard 15 | Deep 2
```

## Metrics Explained

- **Optimization Rate**: Percentage of queries routed to Haiku or Sonnet instead of Opus
- **Estimated Savings**: Total cost saved compared to always using Opus
- **Avg Cost per Query**: Your actual average cost vs what Opus would cost

## Cost Reference

Model pricing per 1M tokens (input/output):
- Haiku: $0.25 / $1.25
- Sonnet: $3 / $15
- Opus: $15 / $75

Average query estimated at 1K input + 2K output tokens (~$0.165 with Opus).
