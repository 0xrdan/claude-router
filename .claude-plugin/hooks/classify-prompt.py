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
# Cross-platform file locking
import platform
if platform.system() == "Windows":
    import msvcrt
    def lock_file(f, exclusive=False):
        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK if exclusive else msvcrt.LK_LOCK, 1)
    def unlock_file(f):
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
else:
    import fcntl
    def lock_file(f, exclusive=False):
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
    def unlock_file(f):
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

# Confidence threshold for LLM fallback
CONFIDENCE_THRESHOLD = 0.7

# Stats file location
STATS_FILE = Path.home() / ".claude" / "router-stats.json"

# Cost estimates per 1M tokens (input/output)
COST_PER_1M = {
    "fast": {"input": 1.0, "output": 5.0},        # Haiku 4.5
    "standard": {"input": 3.0, "output": 15.0},   # Sonnet 4.5
    "deep": {"input": 5.0, "output": 25.0},       # Opus 4.5
}

# Average tokens per query (rough estimate)
AVG_INPUT_TOKENS = 1000
AVG_OUTPUT_TOKENS = 2000

# Exception patterns - queries that will be handled by Opus despite classification
# (router meta-questions, slash commands handled in main())
EXCEPTION_PATTERNS = [
    r'\brouter\b.*\b(stats?|config|setting|work)',
    r'\brouting\b',
    r'claude.?router',
    r'\bexception\b.*\b(track|detect)',
    r'\bclassif(y|ication)\b.*\b(prompt|query)',
]

def is_exception_query(prompt: str) -> tuple[bool, str]:
    """Check if query matches exception patterns that bypass routing."""
    prompt_lower = prompt.lower()
    for pattern in EXCEPTION_PATTERNS:
        if re.search(pattern, prompt_lower):
            return True, "router_meta"
    return False, None

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
    "tool_intensive": [
        # Codebase exploration
        r"\b(find|search|locate) (all|every|each)",
        r"\bacross (the )?(codebase|project|repo)",
        r"\b(all|every) (file|instance|usage|reference)",
        r"\bwhere is .+ (used|called|defined)",
        r"\b(scan|explore|traverse) (the )?(codebase|project)",
        # Multi-file modifications
        r"\b(update|change|modify|rename|replace) .{0,20}(all|every|multiple) files?",
        r"\bglobal (search|replace|rename)",
        r"\brefactor.{0,30}(across|throughout|entire)",
        # Build/test execution
        r"\brun (all |the )?(tests?|specs?|suite)",
        r"\bbuild (the )?(project|app)",
        r"\bnpm (install|build|run)|yarn (install|build)|pip install",
        # Dependency analysis
        r"\b(dependency|import) (tree|graph|analysis)",
        r"\bwhat (depends on|imports|uses)",
    ],
    "orchestration": [
        # Multi-step workflows
        r"\b(step by step|sequentially|in order)\b",
        r"\bfor each (file|component|module)\b",
        r"\bacross the (entire|whole) (codebase|project)",
        # Explicit multi-task
        r"\band (also|then)\b.{0,50}\band (also|then)\b",
        r"\b(multiple|several|many) (tasks?|steps?|operations?)\b",
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


def log_routing_decision(route: str, confidence: float, method: str, signals: list, metadata: dict = None):
    """Log routing decision to stats file with optional metadata tracking."""
    try:
        # Ensure directory exists
        STATS_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Load existing stats or create new (v1.2 schema with exception tracking)
        stats = {
            "version": "1.2",
            "total_queries": 0,
            "routes": {"fast": 0, "standard": 0, "deep": 0, "orchestrated": 0},
            "exceptions": {"router_meta": 0, "slash_commands": 0},
            "tool_intensive_queries": 0,
            "orchestrated_queries": 0,
            "estimated_savings": 0.0,
            "delegation_savings": 0.0,
            "sessions": [],
            "last_updated": None
        }

        if STATS_FILE.exists():
            try:
                with open(STATS_FILE, "r") as f:
                    lock_file(f, exclusive=False)
                    stats = json.load(f)
                    unlock_file(f)
            except (json.JSONDecodeError, IOError):
                pass

        # Ensure v1.2 schema fields exist (migration from v1.0/v1.1)
        stats.setdefault("version", "1.2")
        stats.setdefault("routes", {}).setdefault("orchestrated", 0)
        stats.setdefault("exceptions", {"router_meta": 0, "slash_commands": 0})
        stats.setdefault("tool_intensive_queries", 0)
        stats.setdefault("orchestrated_queries", 0)
        stats.setdefault("delegation_savings", 0.0)

        # Update stats
        stats["total_queries"] += 1
        metadata = metadata or {}

        # Track exceptions (queries that bypass routing due to CLAUDE.md rules)
        exception_type = metadata.get("exception_type")
        if exception_type:
            stats["exceptions"][exception_type] = stats["exceptions"].get(exception_type, 0) + 1

        # Track orchestrated vs regular routes
        if metadata.get("orchestration") and route == "deep":
            stats["routes"]["orchestrated"] += 1
            stats["orchestrated_queries"] += 1
        else:
            stats["routes"][route] += 1

        # Track tool-intensive queries
        if metadata.get("tool_intensive"):
            stats["tool_intensive_queries"] += 1

        # Calculate savings (compared to always using Opus)
        actual_cost = calculate_cost(route)
        opus_cost = calculate_cost("deep")
        savings = opus_cost - actual_cost
        stats["estimated_savings"] += savings

        # Calculate delegation savings for orchestrated queries
        # Assumes 60% delegation (70% Haiku, 30% Sonnet) saves ~40% vs pure Opus
        if metadata.get("orchestration"):
            delegation_saving = opus_cost * 0.4  # ~40% savings through delegation
            stats["delegation_savings"] += delegation_saving

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
            lock_file(f, exclusive=True)
            json.dump(stats, f, indent=2)
            unlock_file(f)

    except Exception:
        # Don't fail the hook if stats logging fails
        pass


def classify_by_rules(prompt: str) -> dict:
    """
    Classify prompt using regex patterns.
    Returns route, confidence, signals, and optional metadata.

    Priority order:
    1. deep patterns (architecture, security, complex analysis)
    2. tool_intensive patterns (route to standard, or deep if combined)
    3. orchestration patterns (route to deep with orchestration flag)
    4. fast patterns (simple queries)
    """
    prompt_lower = prompt.lower()
    deep_signals = []
    tool_signals = []
    orch_signals = []

    # Check for deep patterns first (highest priority)
    for pattern in PATTERNS["deep"]:
        if re.search(pattern, prompt_lower):
            match = re.search(pattern, prompt_lower)
            deep_signals.append(match.group(0) if match else pattern)

    # Check for tool-intensive patterns
    for pattern in PATTERNS.get("tool_intensive", []):
        if re.search(pattern, prompt_lower):
            match = re.search(pattern, prompt_lower)
            tool_signals.append(match.group(0) if match else pattern)

    # Check for orchestration patterns
    for pattern in PATTERNS.get("orchestration", []):
        if re.search(pattern, prompt_lower):
            match = re.search(pattern, prompt_lower)
            orch_signals.append(match.group(0) if match else pattern)

    # Decision matrix: deep + tool_intensive + orchestration
    if deep_signals and (tool_signals or orch_signals):
        # Complex task needing orchestration - route to deep with orchestration flag
        combined = deep_signals + tool_signals + orch_signals
        return {
            "route": "deep",
            "confidence": 0.95,
            "signals": combined[:4],
            "method": "rules",
            "metadata": {"orchestration": True, "tool_intensive": bool(tool_signals)}
        }

    if len(deep_signals) >= 2:
        return {"route": "deep", "confidence": 0.9, "signals": deep_signals[:3], "method": "rules"}

    if deep_signals:  # One deep signal
        return {"route": "deep", "confidence": 0.7, "signals": deep_signals, "method": "rules"}

    # Tool-intensive but not architecturally complex - route to standard
    if tool_signals:
        if len(tool_signals) >= 2:
            return {
                "route": "standard",
                "confidence": 0.85,
                "signals": tool_signals[:3],
                "method": "rules",
                "metadata": {"tool_intensive": True}
            }
        return {
            "route": "standard",
            "confidence": 0.7,
            "signals": tool_signals,
            "method": "rules",
            "metadata": {"tool_intensive": True}
        }

    # Orchestration alone (multi-step workflow) - route to standard
    if orch_signals:
        return {
            "route": "standard",
            "confidence": 0.75,
            "signals": orch_signals[:3],
            "method": "rules",
            "metadata": {"orchestration": True}
        }

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

    # Default to fast with low confidence - cheaper when uncertain
    return {"route": "fast", "confidence": 0.5, "signals": ["no strong patterns"], "method": "rules"}


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
- "standard": Bug fixes, feature implementation, code review, refactoring, test writing, OR tool-intensive tasks (codebase search, running tests, multi-file edits)
- "deep": Architecture decisions, system design, security audits, multi-file refactors, trade-off analysis, complex debugging, OR orchestration tasks (multi-step workflows)

Tool-intensity indicators (favor "standard" or "deep" over "fast"):
- Searching/scanning entire codebase
- Modifying multiple files
- Running tests or builds
- Dependency analysis
- Large-scale refactoring

Return JSON only:
{{"route": "fast|standard|deep", "confidence": 0.0-1.0, "signals": ["signal1", "signal2"], "tool_intensive": true|false}}"""

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
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = input_data.get("prompt", "")

    if not prompt or len(prompt) < 10:
        sys.exit(0)

    # Skip slash commands
    if prompt.strip().startswith("/"):
        sys.exit(0)

    # Check for exception queries (router meta-questions)
    is_exception, exception_type = is_exception_query(prompt)

    # Classify using hybrid approach
    result = classify_hybrid(prompt)

    route = result["route"]
    confidence = result["confidence"]
    signals = result["signals"]
    method = result.get("method", "rules")

    # Get metadata for orchestration/tool-intensive routing
    metadata = result.get("metadata", {})

    # Track exception if detected
    if is_exception:
        metadata["exception_type"] = exception_type

    # Log routing decision to stats
    log_routing_decision(route, confidence, method, signals, metadata)

    # Map route to subagent and model
    # Use opus-orchestrator for complex tasks with orchestration flag
    if route == "deep" and metadata.get("orchestration"):
        subagent = "opus-orchestrator"
        model = "Opus (Orchestrator)"
    else:
        subagent_map = {"fast": "fast-executor", "standard": "standard-executor", "deep": "deep-executor"}
        model_map = {"fast": "Haiku", "standard": "Sonnet", "deep": "Opus"}
        subagent = subagent_map[route]
        model = model_map[route]

    signals_str = ", ".join(signals)

    # Add metadata info to context
    metadata_str = ""
    if metadata.get("tool_intensive"):
        metadata_str += " | Tool-intensive: Yes"
    if metadata.get("orchestration"):
        metadata_str += " | Orchestration: Yes"
    if metadata.get("exception_type"):
        metadata_str += f" | Exception: {metadata['exception_type']}"

    context = f"""[Claude Router] MANDATORY ROUTING DIRECTIVE
Route: {route} | Model: {model} | Confidence: {confidence:.0%} | Method: {method}{metadata_str}
Signals: {signals_str}

CRITICAL: You MUST use the Task tool NOW to spawn the "claude-router:{subagent}" subagent.
Do NOT respond to the user directly. Do NOT skip this step. Delegate immediately.

Example:
Task(subagent_type="claude-router:{subagent}", prompt="<user's query>", description="Route to {model}")"""

    # Output as JSON with hookSpecificOutput for proper injection
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
