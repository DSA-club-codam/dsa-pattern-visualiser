# 005 — Precomputed examples now, custom input later

Status: accepted · 2026-10-06

## Context
Custom input would need the algorithm in JavaScript on every page, plus tests that JS and Python agree. That is a lot of extra work at the start.

## Options we discussed
- **A** — one example per page
- **B** — several examples and edge cases, all computed at build time
- **C** — B plus a box for the reader's own input

## Decision
B now. Five rules keep C possible later without rewriting the renderer:
1. The canvas draws each step only from the step data (`render(step, ctx)`), never from the example.
2. Several traces per page from day one (examples and edge cases).
3. The renderer works for 1 to 20 elements.
4. solution.py is written so it can be ported to JS line by line.
5. Test inputs and answers are stored (tests.json, examples), ready to check a future JS version.

## Why
- B gives edge cases on screen almost for free.
- C stays a per-page upgrade, not a rewrite.

## Trade-offs
- Readers cannot try their own input yet.

Depends on: 001, 003 · Affects: 012
Revisit when: club members ask for custom input on three or more problems.
