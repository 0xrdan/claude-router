#!/usr/bin/env python3
"""
Claude Router - UserPromptSubmit Hook
Classifies prompts using hybrid approach:
1. Rule-based patterns (instant, free)
2. Haiku LLM fallback for low-confidence cases (~$0.001)

Part of claude-router: https://github.com/0xrdan/claude-router
"""
import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime
import fcntl

# Confidence threshold for LLM fallback
CONFIDENCE_THRESHOLD = 0.7

# Stats file location
STATS_FILE = Path.home() / ".claude" / "router-stats.json"

# Cost estimates per 1M tokens (input/output)
COST_PER_1M = {
    "fast": {"input": 0.25, "output": 1.25},      # Haiku
    "standard": {"input": 3.0, "output": 15.0},   # Sonnet
    "deep": {"input": 15.0, "output": 75.0},      # Opus
}

# Average tokens per query (rough estimate)
AVG_INPUT_TOKENS = 1000
AVG_OUTPUT_TOKENS = 2000

# Classification patterns
PATTERNS = {
    "fast": [
        # Simple questions
        r"^what (is|are|does) ",
        r"^how (do|does|to) ",
        r"^(show|list|get) .{0,30}$",
        # Formatting
        r"\b(format|lint|prettify|beautify)\b",
        # Git simple ops
        r"\bgit (status|log|diff|add|commit|push|pull)\b",
        # JSON/YAML
        r"\b(json|yaml|yml)\b.{0,20}$",
        # Regex
        r"\bregex\b",
        # Syntax questions
        r"\bsyntax (for|of)\b",
        r"^(what|how).{0,50}\?$",
    ],
    "deep": [
        # Architecture
        r"\b(architect|architecture|design pattern|system design)\b",
        r"\bscalable?\b",
        # Security
        r"\b(security|vulnerab|audit|penetration|exploit)\b",
        # Multi-file
        r"\b(across|multiple|all) (files?|components?|modules?)\b",
        r"\brefactor.{0,20}(codebase|project|entire)\b",
        # Trade-offs
        r"\b(trade-?off|compare|pros? (and|&) cons?)\b",
        r"\b(analyze|evaluate|assess).{0,30}(option|approach|strateg)\b",
        # Complex
        r"\b(complex|intricate|sophisticated)\b",
        r"\boptimiz(e|ation).{0,20}(performance|speed|memory)\b",
        # Planning
        r"\b(multi-?phase|extraction|standalone repo|migration)\b",
    ],
}


def get_api_key():
    """Get API key from environment or common locations."""
    # Try environment first
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        return api_key

    # Try common .env locations
    search_paths = [
        Path.cwd() / ".env",                           # Current directory
        Path.cwd() / "server" / ".env",                # Server subdirectory
        Path.home() / ".anthropic" / "api_key",        # Anthropic config
        Path.home() / ".config" / "anthropic" / "key", # XDG config
    ]

    for env_path in search_paths:
        try:
            with open(env_path, "r") as f:
                content = f.read()
                # Handle both KEY=value and plain value formats
                for line in content.split("\n"):
                    if line.startswith("ANTHROPIC_API_KEY="):
                        return line.strip().split("=", 1)[1].strip('"\'')
                # If file is just the key (no assignment)
                if content.strip().startswith("sk-ant-"):
                    return content.strip()
        except (FileNotFoundError, PermissionError):
            continue

    return None


def calculate_cost(route: str, input_tokens: int = AVG_INPUT_TOKENS, output_tokens: int = AVG_OUTPUT_TOKENS) -> float:
    """Calculate estimated cost for a route."""
    costs = COST_PER_1M[route]
    input_cost = (input_tokens / 1_000_000) * costs["input"]
    output_cost = (output_tokens / 1_000_000) * costs["output"]
    return input_cost + output_cost


def log_routing_decision(route: str, confidence: float, method: str, signals: list):
    """Log routing decision to stats file."""
    try:
        # Ensure directory exists
        STATS_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Load existing stats or create new
        stats = {
            "version": "1.0",
            "total_queries": 0,
            "routes": {"fast": 0, "standard": 0, "deep": 0},
            "estimated_savings": 0.0,
            "sessions": [],
            "last_updated": None
        }

        if STATS_FILE.exists():
            try:
                with open(STATS_FILE, "r") as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                    stats = json.load(f)
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            except (json.JSONDecodeError, IOError):
                pass

        # Update stats
        stats["total_queries"] += 1
        stats["routes"][route] += 1

        # Calculate savings (compared to always using Opus)
        actual_cost = calculate_cost(route)
        opus_cost = calculate_cost("deep")
        savings = opus_cost - actual_cost
        stats["estimated_savings"] += savings

        # Get or create today's session
        today = datetime.now().strftime("%Y-%m-%d")
        session = None
        for s in stats.get("sessions", []):
            if s["date"] == today:
                session = s
                break

        if not session:
            session = {
                "date": today,
                "queries": 0,
                "routes": {"fast": 0, "standard": 0, "deep": 0},
                "savings": 0.0
            }
            stats.setdefault("sessions", []).append(session)

        session["queries"] += 1
        session["routes"][route] += 1
        session["savings"] += savings

        # Keep only last 30 days of sessions
        stats["sessions"] = sorted(stats["sessions"], key=lambda x: x["date"], reverse=True)[:30]

        stats["last_updated"] = datetime.now().isoformat()

        # Write stats atomically
        with open(STATS_FILE, "w") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            json.dump(stats, f, indent=2)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    except Exception:
        # Don't fail the hook if stats logging fails
        pass


def classify_by_rules(prompt: str) -> dict:
    """
    Classify prompt using regex patterns.
    Returns route, confidence, and signals.
    """
    prompt_lower = prompt.lower()
    signals = []

    # Check for deep patterns first (higher priority)
    for pattern in PATTERNS["deep"]:
        if re.search(pattern, prompt_lower):
            match = re.search(pattern, prompt_lower)
            signals.append(match.group(0) if match else pattern)
            if len(signals) >= 2:
                return {"route": "deep", "confidence": 0.9, "signals": signals[:3], "method": "rules"}

    if signals:  # One deep signal
        return {"route": "deep", "confidence": 0.7, "signals": signals, "method": "rules"}

    # Check for fast patterns
    fast_signals = []
    for pattern in PATTERNS["fast"]:
        if re.search(pattern, prompt_lower):
            match = re.search(pattern, prompt_lower)
            fast_signals.append(match.group(0) if match else pattern)
            if len(fast_signals) >= 2:
                return {"route": "fast", "confidence": 0.9, "signals": fast_signals[:3], "method": "rules"}

    if fast_signals:  # One fast signal
        return {"route": "fast", "confidence": 0.7, "signals": fast_signals, "method": "rules"}

    # Default to standard with low confidence (triggers LLM fallback)
    return {"route": "standard", "confidence": 0.5, "signals": ["no strong patterns"], "method": "rules"}


def classify_by_llm(prompt: str, api_key: str) -> dict:
    """
    Classify prompt using Haiku LLM.
    Used as fallback for low-confidence rule-based results.
    """
    try:
        from anthropic import Anthropic
    except ImportError:
        return None

    client = Anthropic(api_key=api_key)

    classification_prompt = f"""Classify this coding query into exactly one route. Return ONLY valid JSON, no other text.

Query: "{prompt}"

Routes:
- "fast": Simple factual questions, syntax lookups, formatting, git status, JSON/YAML manipulation
- "standard": Bug fixes, feature implementation, code review, refactoring, test writing
- "deep": Architecture decisions, system design, security audits, multi-file refactors, trade-off analysis, complex debugging

Return JSON only:
{{"route": "fast|standard|deep", "confidence": 0.0-1.0, "signals": ["signal1", "signal2"]}}"""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            messages=[{"role": "user", "content": classification_prompt}]
        )

        response_text = message.content[0].text.strip()

        # Handle potential markdown code blocks
        if "```" in response_text:
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:].strip()

        result = json.loads(response_text)
        result["method"] = "haiku-llm"
        return result

    except Exception as e:
        # Log error but don't fail
        print(f"LLM classification error: {e}", file=sys.stderr)
        return None


def classify_hybrid(prompt: str) -> dict:
    """
    Hybrid classification: rules first, LLM fallback for low confidence.
    """
    # Step 1: Rule-based classification (instant, free)
    result = classify_by_rules(prompt)

    # Step 2: If low confidence and API key available, use LLM
    if result["confidence"] < CONFIDENCE_THRESHOLD:
        api_key = get_api_key()
        if api_key:
            llm_result = classify_by_llm(prompt, api_key)
            if llm_result:
                return llm_result

    return result


def main():
    """Main hook handler."""
    try:
        # Redirect stderr to suppress any warnings
        sys.stderr = open(os.devnull, 'w')

        try:
            input_data = json.load(sys.stdin)
        except json.JSONDecodeError:
            sys.exit(0)

        prompt = input_data.get("prompt", "")

        if not prompt or len(prompt) < 10:
            sys.exit(0)

        # Skip slash commands
        if prompt.strip().startswith("/"):
            sys.exit(0)

        # Classify using hybrid approach
        result = classify_hybrid(prompt)

        route = result["route"]
        confidence = result["confidence"]
        signals = result["signals"]
        method = result.get("method", "rules")

        # Log routing decision to stats (don't let this fail the hook)
        try:
            log_routing_decision(route, confidence, method, signals)
        except Exception:
            pass

        # Map route to subagent and model
        subagent_map = {"fast": "fast-executor", "standard": "standard-executor", "deep": "deep-executor"}
        model_map = {"fast": "Haiku", "standard": "Sonnet", "deep": "Opus"}

        subagent = subagent_map[route]
        model = model_map[route]
        signals_str = ", ".join(signals)

        context = f"""[Claude Router] ROUTING DIRECTIVE
Route: {route} | Model: {model} | Confidence: {confidence:.0%} | Method: {method}
Signals: {signals_str}

ACTION REQUIRED: Use the Task tool to spawn the "{subagent}" subagent with the user's query.
Do not handle this query directly - delegate to the subagent for cost-optimized execution."""

        # Output JSON with hookSpecificOutput for transcript visibility
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    except Exception:
        # Any error: exit silently
        sys.exit(0)


if __name__ == "__main__":
    main()
