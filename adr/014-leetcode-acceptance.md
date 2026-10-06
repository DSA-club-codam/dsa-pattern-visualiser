# 014 — LeetCode acceptance is recorded by hand

Status: accepted · 2026-10-06

## Context
build.py cannot reach LeetCode. Our tests do not include LeetCode's hidden or very large inputs.

## Decision
Every language is submitted by hand from a dedicated LeetCode account. Accepted languages go into approach.json "accepted"; the code tab shows ✓. The profile link is set once in site.json and shown on the home page and page footers. Single submissions are private, so we link the profile, not submissions.

Update 2026-10-06: the profile link is shown on the main page only (see ADR 023).

## Trade-offs
- Manual step, easy to forget. Pages without ✓ are still tested by our build.

Depends on: 003 · Affects: —
Revisit when: —
