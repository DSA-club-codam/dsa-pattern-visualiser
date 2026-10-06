# 018 — Pattern names stay broad

Status: superseded by 022 · 2026-10-06

## Context
The first sliding-window problem was labelled "Sliding window (variable)". With a fixed-window problem later, the home page would show two sliding-window patterns, and it would be unclear where to put a problem.

## Decision
One name per pattern family on the home page and in the badge: "Sliding window", not fixed / variable. The variant is explained in the "Why this pattern?" card. "Two pointers · same direction" stays as it is: the direction changes how the pointers are drawn and named (ADR 011).

## Trade-offs
- The home page cannot filter fixed and variable windows apart.

Depends on: 015 · Affects: —
Revisit when: the club wants to practise fixed and variable windows as separate topics.
