---
name: router-analytics
description: Generate HTML analytics dashboard for routing statistics
context: fork
agent: general-purpose
allowed-tools: Read, Write, Bash
---

# Router Analytics Skill

Generate a visual HTML analytics dashboard from your routing statistics.

## What This Does

Reads your routing statistics from `~/.claude/router-stats.json` and generates an interactive HTML dashboard with:
- Route distribution pie chart
- Daily/weekly trends line chart
- Cost savings over time
- Session comparison metrics

## Usage

```
/router-analytics
/router-analytics --output ~/Desktop/router-report.html
```

## Generated Dashboard Includes

### Summary Cards
- Total queries processed
- Total estimated savings vs always-Opus
- Route distribution (fast/standard/deep/orchestrated)
- Average confidence scores

### Charts
- **Pie Chart**: Route distribution breakdown
- **Line Chart**: Daily query trends over last 30 days
- **Bar Chart**: Savings per session

### Tables
- Recent sessions with per-session metrics
- Exception tracking (router_meta queries, slash commands)

## Output

By default, generates `router-analytics.html` in the current directory.

Use `--output <path>` to specify a custom output location.

## Implementation

When this skill runs:
1. Read `~/.claude/router-stats.json`
2. Parse and aggregate statistics
3. Generate HTML with embedded Chart.js visualizations
4. Write to output file
5. Report summary to user

## Requirements

The stats file must exist (run some queries through the router first).
