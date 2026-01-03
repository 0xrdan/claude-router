# Contributing to Claude Router

Thank you for your interest in contributing to Claude Router! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/claude-router.git
   cd claude-router
   ```
3. Install locally:
   ```bash
   ./install.sh  # Choose option 1 for project install
   ```

## Development Setup

The project structure is straightforward:

```
.claude/
├── hooks/
│   └── classify-prompt.py    # Main classifier logic
├── agents/
│   ├── fast-executor/        # Haiku agent
│   ├── standard-executor/    # Sonnet agent
│   └── deep-executor/        # Opus agent
└── skills/
    └── route/                # Manual /route skill
```

### Testing Changes

To test your changes:

1. Make edits to the classifier or agents
2. Start a new Claude Code session
3. Try various queries and verify routing behavior

### Testing the Classifier Directly

```bash
echo '{"prompt": "What is the syntax for a Python list?"}' | python3 .claude/hooks/classify-prompt.py
```

## Areas for Contribution

### High Priority

1. **Improved Classification Patterns**
   - Add new regex patterns for better accuracy
   - Fix false positives/negatives
   - Add language-specific patterns

2. **Usage Statistics (Phase 4)**
   - Track routing decisions to `~/.claude/router-stats.json`
   - Create `/router-stats` skill to display savings
   - Show "You saved $X this session" summaries

3. **Context-Aware Routing (Phase 5)**
   - Factor in number of files open
   - Consider session history
   - Adjust based on error patterns

### Good First Issues

- Add more classification patterns for specific coding tasks
- Improve error messages and logging
- Add configuration options (e.g., disable LLM fallback)
- Documentation improvements

## Code Style

- Python code should follow PEP 8
- Keep the classifier lightweight (it runs on every prompt)
- Prefer rule-based patterns over LLM calls for common cases
- Test with edge cases before submitting

## Pull Request Process

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Add: description of your change"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Open a Pull Request with:
   - Clear description of the change
   - Any testing you've done
   - Screenshots if applicable

## Commit Message Format

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

Example: `feat: Add Python-specific routing patterns`

## Questions?

Open an issue with the `question` label, or reach out in the discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
