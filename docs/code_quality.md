# Code Quality Guidelines

This project uses modern ecosystem standards for formatting and linting. Automated checks are enforced via `pre-commit`.

## Automated Checks Trigger

Code quality checks run **automatically on `git commit`** via `pre-commit` hooks.

## Environment Setup

To enable automated checks on your local machine:
```bash
# Install dev dependencies (if not already installed)
pip install -e .[dev]

# Install the pre-commit hook
pre-commit install
```

## Manual Execution Commands

You can run `ruff` manually at any time without committing:

### Run on all files
```bash
# Format code
ruff format .

# Run linter and auto-fix simple issues
ruff check . --fix
```

### Run pre-commit on all files manually
```bash
pre-commit run --all-files
```

## Emergency Bypassing

If you absolutely must skip hooks (e.g., for an emergency hotfix), use the `--no-verify` flag:
```bash
git commit -m "fix: emergency hotfix" --no-verify
```
*Warning: Use this responsibly. CI pipelines will still enforce these checks.*