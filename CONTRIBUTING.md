# Contributing to ViralMint

Thanks for your interest in contributing! ViralMint is an open-source project under the AGPL-3.0 license. We welcome bug reports, feature requests, documentation improvements, and code contributions.

## Ground rules

- **Open an issue first** for non-trivial changes. Aligning on direction up front saves rework.
- **Keep PRs focused.** One logical change per PR makes review faster and easier to revert if needed.
- **Be respectful.** Assume good intent. We're all volunteers here.

## Development setup

```bash
git clone https://github.com/<your-fork>/ViralMint.git
cd ViralMint
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY or OPENAI_API_KEY to .env
python run.py
```

System dependencies: Python 3.11+, Node 18+, FFmpeg, ImageMagick.

## Code style

### Python (backend)

- Follow PEP 8. Use `black` and `ruff` if you have them installed.
- Type hints encouraged on public functions.
- Async-first: prefer `async def` for any I/O code path.
- Docstrings for non-obvious functions; skip them for self-explanatory ones.

### JavaScript/JSX (frontend)

- 2-space indentation, double quotes (matches existing files).
- Prefer functional components and hooks over class components.
- MUI's `sx` prop is the styling default; avoid introducing a new styling system without discussion.

## Commit & PR

- Use clear, imperative commit messages: `Add Pexels rate-limit handling`, not `pexels stuff`.
- Reference the issue number in the PR description when applicable.
- Include a short test plan in the PR body.

## License headers

All Python source files must start with the SPDX/copyright header:

```python
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
```

By contributing, you agree that your contributions are licensed under AGPL-3.0.

## Tests

```bash
pytest tests/
```

If you change behavior covered by tests, update them. If you add behavior, add a test where reasonable.

## Reporting bugs

Use GitHub Issues. A useful bug report includes:

- What you expected to happen
- What actually happened (full error / stack trace)
- Minimal repro steps
- OS, Python version, ViralMint version (commit hash)

## Reporting security issues

**Do not file public issues for security vulnerabilities.** See [SECURITY.md](SECURITY.md) for the disclosure process.
