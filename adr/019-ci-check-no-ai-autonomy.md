# 019 — Automatic check on GitHub; AI has no autonomy in the repository

Status: accepted · 2026-10-06

## Context
The repository accepts issues and pull requests from anyone. The maintainer reviews and merges by hand and does not want to build every pull request locally. We also discussed connecting Claude to the repository through the Claude GitHub App (@claude in issues and pull requests).

## Options we discussed
- **A** — check pull requests by hand, locally
- **B** — a GitHub Actions workflow that runs `build.py` on every pull request and push to main
- **C** — B plus the Claude GitHub App, so Claude can review or open pull requests

## Decision
B. `.github/workflows/check.yml` installs Python and Chromium, runs `python build.py` (oracle tests, C/C++ checks, browser smoke test) and fails if `docs/` differs from what the sources produce. It has read-only permissions and uses no secrets, so it is safe on pull requests from forks.

No Claude GitHub App. Claude Code is used only locally, by the maintainer, and only commits or pushes when asked (SKILL.md, hard rule 9). GitHub Pages publishes `docs/` from main, so publishing is a normal push.

## Why
- A green check proves the same things on every pull request, without trusting the contributor or the AI.
- The maintainer keeps every decision to merge.

## Trade-offs
- Each check uses about 2–3 minutes of GitHub Actions time.
- No automatic review of explanations or code style: the maintainer still reads every pull request.

Depends on: 001, 003 · Affects: —
Revisit when: pull requests arrive faster than the maintainer can review them.
