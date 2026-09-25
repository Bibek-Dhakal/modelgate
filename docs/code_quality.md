# Code Quality Guidelines

ModelGate strictly enforces code quality to maintain a clean, readable, and predictable codebase. We utilize **Ruff**—an extremely fast Python linter and code formatter written in Rust—replacing older tools like Black, Flake8, and isort.

## Automated Checks (Git Hooks)

Code quality checks run **automatically on every `git commit`** via `pre-commit`. 

If a formatting error is detected, the commit will be blocked. Ruff is configured to auto-fix safe issues, so in most cases, you simply need to restage your files and commit again.

### Environment Setup

To enable automated checks on your local machine:
```bash
# Install dev dependencies (if not already installed)
pip install -e .[dev]

# Install the pre-commit hook into your .git directory
pre-commit install
```

## Manual Execution Commands

You can run the quality tools manually at any time without committing:

### Run on all files
```bash
# Sort imports and format code standard
ruff format .

# Run linter and auto-fix simple issues (e.g. unused imports)
ruff check . --fix
```

### Run pre-commit hooks manually
```bash
# Triggers Ruff formatting, linting, and trailing-whitespace fixes
pre-commit run --all-files
```

## Emergency Bypassing

If you absolutely must skip hooks (e.g., for an emergency hotfix), use the `--no-verify` flag:
```bash
git commit -m "fix: emergency hotfix" --no-verify
```
*Warning: Use this responsibly. CI pipelines will still enforce these checks on Pull Requests, so the code must eventually comply.*