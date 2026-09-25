# Contributing to ModelGate

First off, thank you for considering contributing to ModelGate! It's people like you that make open-source projects thrive.

The following is a set of guidelines for contributing to this project. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Local Development Setup

To get your environment ready for development:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/modelgate.git
   cd modelgate
   ```

2. Install the project with development dependencies:
   ```bash
   pip install -e .[dev]
   ```

3. Install the pre-commit hooks to ensure code quality formatting on every commit:
   ```bash
   pre-commit install
   ```

## Code Quality and Testing

- **Linting & Formatting:** We use `Ruff` for linting and formatting. It will run automatically when you commit (if you installed `pre-commit`). You can also run it manually via `ruff check .` and `ruff format .`.
- **Testing:** We use `pytest` for all unit and integration tests. Before submitting a PR, ensure all tests pass:
  ```bash
  pytest
  ```
- Any new features or bug fixes must include corresponding tests.

## Pull Request Process

1. Create a new branch for your feature or bugfix: `git checkout -b feature-or-fix-name`.
2. Make your changes and commit them following the **Conventional Commits** standard (see below).
3. Push your branch to your fork or the main repository.
4. Open a Pull Request against the `main` branch.
5. Ensure CI checks pass. Once approved, your PR will be merged.

---

## STRICT ENFORCEMENT: Conventional Commits

This project relies on **Automated Versioning and Changelog Generation** using [Release Please](https://github.com/googleapis/release-please). 

Because of this, **ALL commit messages and Pull Request titles MUST strictly follow the [Conventional Commits](https://www.conventionalcommits.org/) format.**

### Format
`<type>(<optional scope>): <description>`

### Allowed Types

| Type | Description | Triggers Release? | Semantic Version Bump |
|------|-------------|-------------------|-----------------------|
| `feat:` | A new feature | **Yes** | Minor (e.g. 1.0.0 -> 1.1.0) |
| `fix:` | A bug fix | **Yes** | Patch (e.g. 1.0.0 -> 1.0.1) |
| `feat!:` or `fix!:` | A breaking API change | **Yes** | Major (e.g. 1.1.0 -> 2.0.0) |
| `docs:` | Documentation only changes | No | None |
| `chore:` | Maintenance, dependency updates, etc. | No | None |
| `test:` | Adding missing tests or correcting tests | No | None |
| `refactor:` | A code change that neither fixes a bug nor adds a feature | No | None |
| `style:` | Changes that do not affect the meaning of the code (formatting) | No | None |

*Example:* `feat(api): add new predict endpoint for bulk features`

## How Releases Work

1. When code is merged into the `main` branch, the `release-please` GitHub Action analyzes the commit history since the last release tag.
2. If it finds commits that warrant a release (e.g., `feat:`, `fix:`), it automatically generates or updates a long-running **Release Pull Request** (usually titled `chore: release x.y.z`).
3. This Release PR will continuously aggregate new unreleased changes as they hit `main`.
4. **To publish a release**, a repository maintainer simply merges the automated Release PR into `main`.
5. Upon merging the Release PR, `release-please` automatically tags the repository (e.g., `v1.1.0`), finalizes the `CHANGELOG.md`, and prepares the repository for the next development cycle.