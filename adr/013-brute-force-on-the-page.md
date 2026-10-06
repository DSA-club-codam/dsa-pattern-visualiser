# 013 — Brute force on the page: code and an operation counter, no animation

Status: accepted · 2026-10-06

## Context
Brute force exists anyway as the test oracle (ADR 003). We asked whether to animate it too.

## Options we discussed
- **A** — animate brute force
- **B** — show its code (collapsed) and count operations on the current input
- **C** — do not show it

## Decision
B. The "Why this pattern?" card shows the brute-force summary, its code, and a line such as "On this input: brute force needs 36 element checks, this approach needs 9." Both counts come from `T.op()` calls when tracing.

## Why
- An O(n²) animation is long and draws attention away from the pattern.
- The counter shows in one line why the pattern matters, and it changes with each example.

## Trade-offs
- What counts as "one operation" is chosen per problem (opsUnit); it is a teaching number, not a benchmark.

Depends on: 003 · Affects: —
Revisit when: readers ask to see where brute force repeats work; a static picture would be the next step.
