# 016 — Problems are not tied to LeetCode

Status: accepted · 2026-10-06

## Context
The first schema had "number" and "slug" and built a LeetCode URL from them. Problems from NeetCode or other sites may come later.

## Decision
problem.json has `"source": { "site", "id", "url" }` (and an optional "short" prefix). The page says "Open on <site>", the label is "<short> <id>" (e.g. "LC 283") or nothing when there is no id. Folders are named `<short>-<id>-<slug>` or `<short>-<slug>`. Random tests are seeded from the folder name, not from a number.

## Trade-offs
- "accepted" in approach.json means accepted on that source's judge; a site without a judge simply has none.

Depends on: 001 · Affects: 014
Revisit when: a source needs more than a link (for example, its own way to run tests).
