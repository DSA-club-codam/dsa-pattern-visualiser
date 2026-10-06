# 009 — Pages work on phones

Status: accepted · 2026-10-06

## Context
The first LC 283 page adapted to small screens; the LC 2958 page did not. The project is also a portfolio piece and may be opened on a phone during an interview or a club session.

## Decision
Every page works at 375px wide with no sideways page scroll. Panels stack; array cells shrink; a long array scrolls inside its own panel. The smoke test checks this on every build.

## Trade-offs
- Some layout code for small screens in core.

Depends on: 002 · Affects: 012
Revisit when: —
