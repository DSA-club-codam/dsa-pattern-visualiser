# 004 — Python3 and C++17 always, C only for simple array problems

Status: accepted · 2026-10-06

## Context
The club works in Python; Codam students write C and C++. C has no standard hash map, heap or dynamic array, so many solutions in C would mostly show data-structure code, not the pattern.

## Options we discussed
- **A** — Python only
- **B** — Python + C++ + C for everything
- **C** — Python + C++ always; C only when the natural solution uses plain arrays, fixed-size counters and loops

## Decision
C. When there is no C version, approach.json has a one-sentence "noC" reason, shown in the code drawer.

## Why
- Every page is useful to both Python and C++ readers.
- C appears where it shows the same idea clearly (two pointers, sliding window with a small alphabet, binary search, prefix sums).

## Trade-offs
- Up to three implementations per approach to maintain. Tests catch wrong answers, not differences in style.

Depends on: 003 · Affects: —
Revisit when: club members ask for C on problems that need a map, or nobody uses the C tab.
