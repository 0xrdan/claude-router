# Contributing to Claude Router

Thank you for your interest in contributing to Claude Router! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/claude-router.git
   cd claude-router
   ```
3. Make your changes to files in the repository
4. Test your changes (see Testing below)

## Development Setup

The project structure is straightforward:

```
claude-router/
├── hooks/
│   └── classify-prompt.py    # Main classifier logic
├── agents/
│   ├── fast-executor.md      # Haiku agent
│   ├── standard-executor.md  # Sonnet agent
│   └── deep-executor.md      # Opus agent
├── skills/
│   ├── route/                # Manual /route skill
│   └── router-stats/         # Stats display skill
└── .claude-plugin/           # Marketplace plugin files
```

### Testing Changes

To test your changes:

1. Make edits to the classifier or agents
2. Start a new Claude Code session
3. Try various queries and verify routing behavior

### Testing the Classifier Directly

```bash
echo '{"prompt": "What is the syntax for a Python list?"}' | python3 hooks/classify-prompt.py
```

## Areas for Contribution

### High Priority

1. **Improved Classification Patterns**
   - Add new regex patterns for better accuracy
   - Fix false positives/negatives
   - Add language-specific patterns

2. **Context-Aware Routing (Phase 5)**
   - Factor in number of files open
   - Consider session history
   - Adjust based on error patterns

3. **Learning from Feedback (Phase 6)**
   - Track user overrides
   - Adjust future routing based on patterns
   - Per-project routing profiles

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

**Important:** All changes must go through pull requests. Never push directly to `main`.

### Workflow

1. **Sync with main:**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

   Branch naming conventions:
   - `feature/` - New features (e.g., `feature/phase-5-context-routing`)
   - `fix/` - Bug fixes (e.g., `fix/classification-edge-case`)
   - `docs/` - Documentation (e.g., `docs/improve-readme`)

3. **Make your changes and commit:**
   ```bash
   git add .
   git commit -m "feat: description of your change"
   ```

4. **Push and create PR:**
   ```bash
   git push -u origin feature/your-feature-name
   gh pr create --title "Your PR title" --body "Description"
   ```

5. **After PR is merged:**
   ```bash
   git checkout main
   git pull origin main
   git branch -d feature/your-feature-name  # Delete local branch
   ```

### PR Requirements

- Clear description of the change
- Reference related issues (if any)
- Testing you've done
- Screenshots if applicable
- Update relevant documentation (README, planning docs)

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
