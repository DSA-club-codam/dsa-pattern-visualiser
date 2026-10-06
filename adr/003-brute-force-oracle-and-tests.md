# 003 — Correctness: brute-force oracle, random tests, all languages

Status: accepted · 2026-10-06

## Context
The first skill checked "Python output = expected output", but the expected output could also come from Claude, so the check proved little.

## Options we discussed
- **A** — trust the expected outputs written with the solution
- **B** — compare every solution with an independent brute-force solution on many inputs

## Decision
B. For every problem `build.py` runs, before writing any page:
1. brute force vs the expected answers from the LeetCode statement;
2. every approach (clean Python, without trace lines) vs brute force on the examples, `tests.json` and 200 random inputs from `gen.py`;
3. C++17 and C (if present), compiled with `-Wall -Wextra -Werror`, vs brute force on the same inputs;
4. the traced Python must give the same answer as the clean one.
If anything fails, `docs/` is not touched.

## Why
- Two different algorithms that agree on hundreds of inputs are very unlikely to share a bug.
- Languages cannot silently drift apart.

## Trade-offs
- Our tests are not LeetCode's hidden tests: no huge inputs, so time limits are not checked. Mitigation: manual submission (ADR 014).
- A bug shared by brute force and solution would pass. Mitigation: LeetCode examples check brute force itself.
- Captions cannot be tested automatically; the user reviews them.

Depends on: 001 · Affects: 004, 013, 014
Revisit when: LeetCode rejects a solution that passed our build.
