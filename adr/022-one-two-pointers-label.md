# 022 — One "Two pointers" label for the whole family

Status: accepted · 2026-10-06

## Context
ADR 018 kept pattern names broad, with one exception: "Two pointers · same direction". With LC 88 (two pointers on two arrays, merging from the end) the home page would get a second two-pointer group, the same problem ADR 018 solved for sliding windows.

## Options we discussed
- **A** — a new group "Two pointers · two arrays" next to "Two pointers · same direction"
- **B** — put LC 88 under "Two pointers · same direction", since all three pointers move right to left
- **C** — one broad label "Two pointers" for every variant

## Decision
C. Pattern names are broad, with no exceptions: "Two pointers", "Sliding window". The variant (same direction, towards each other, two arrays merging from the end, fixed or variable window) is explained in the "Why this pattern?" card, not in the name. LC 283 is relabelled from "Two pointers · same direction" to "Two pointers". Pointer names and colours still follow the variant (ADR 011, ADR 021).

## Why
- One place on the home page for every two-pointer problem.
- The same rule for every pattern, so there is no doubt where a new problem goes.
- The picture and the pointer names already show the variant.

## Trade-offs
- The home page cannot filter two-pointer variants apart.
- Approach ids (URL anchors) such as `two-pointers-same-direction` keep their old names, so old links still work.

Supersedes: 018 · Depends on: 015, 011 · Affects: 021
Revisit when: the club wants to practise two-pointer variants as separate topics.
