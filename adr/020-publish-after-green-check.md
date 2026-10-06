# 020 — The site is published by GitHub Actions, only after a green check

Status: accepted · 2026-10-06 · changes the publishing part of 008

## Context
GitHub Pages can publish in two ways: straight from a folder on a branch, or from a GitHub Actions workflow. Publishing from the branch would put `docs/` online even when the check (ADR 019) is red.

## Decision
Pages source is "GitHub Actions". The "Check" workflow builds and tests on every push to main; a second job publishes `docs/` only if that build is green. Pull requests are checked but never published. "GitHub Actions" here is GitHub's own automation; no AI is involved.

## Why
- A broken build never reaches the live site.
- One workflow does both, so there is nothing else to configure.

## Trade-offs
- Publishing takes a few minutes after a push (the whole check runs first).
- If GitHub Actions is down, the site cannot be updated until it is back.

Depends on: 008, 019 · Affects: —
Revisit when: publishing gets too slow for how often the site changes.
