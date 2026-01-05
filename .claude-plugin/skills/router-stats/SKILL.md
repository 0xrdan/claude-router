---
name: router-stats
description: Display Claude Router usage statistics and cost savings
user_invokable: true
---

# Router Stats

Display usage statistics and estimated cost savings from Claude Router.

## Instructions

Read the stats file at `~/.claude/router-stats.json` and present the data in a clear, formatted way.

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
╔═══════════════════════════════════════════════════╗
║           Claude Router Statistics                 ║
╚═══════════════════════════════════════════════════╝

📊 All Time
───────────────────────────────────────────────────
Total Queries Routed: 100

Route Distribution:
  Fast (Haiku):     30 (30%)  ████████░░░░░░░░░░░░
  Standard (Sonnet): 60 (60%)  ████████████████░░░░
  Deep (Opus):      10 (10%)  ████░░░░░░░░░░░░░░░░

💰 Estimated Savings: $12.50
   (compared to always using Opus)

📅 Today (2026-01-03)
───────────────────────────────────────────────────
Queries: 25
Savings: $3.20

Route Distribution:
  Fast: 8 | Standard: 15 | Deep: 2
```

## Steps

1. Use the Read tool to read `~/.claude/router-stats.json`
2. If the file doesn't exist, inform the user that no stats are available yet
3. Calculate percentages for route distribution
4. Format and display the statistics
5. Include the savings comparison explanation

## Notes

- Savings are calculated assuming Opus would have been used for all queries
- Cost estimates use: Haiku 4.5 $1/$5, Sonnet 4.5 $3/$15, Opus 4.5 $5/$25 per 1M tokens
- Average query estimated at 1K input + 2K output tokens
