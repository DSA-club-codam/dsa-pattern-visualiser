# 007 — The catalogue and home page are generated

Status: accepted · 2026-10-06

## Context
The home page groups problems by pattern, data structure and problem. Keeping a hand-written list in sync with the pages is easy to forget.

## Decision
`build.py` writes `docs/catalogue.js` from problem.json, approach.json and site.json. `docs/index.html` renders from it. It is a `.js` file, not `.json`, because browsers block reading JSON from a page opened as a local file.

## Why
- The home page cannot list a page that does not exist or miss one that does.

## Trade-offs
- Pattern and data-structure names must be spelled the same in every approach.json, or a group splits in two.

Depends on: 001, 006 · Affects: —
Revisit when: groups split because of spelling, then add a fixed list of allowed names to build.py.
