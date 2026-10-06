# 001 — Sources are separate from built pages

Status: accepted · 2026-10-06

## Context
The first two pages (LC 283, LC 2958) were single HTML files written by Claude. Code, steps and text lived only inside the HTML. If the step format changed, the pages could not be regenerated.

## Options we discussed
- **A** — keep one hand-generated HTML file per problem
- **B** — keep sources (solutions, tests, text) in `problems/`, and let a script assemble `docs/`

## Decision
B. Claude writes sources in `problems/`. `build.py` tests them and assembles every page. `docs/` is never edited by hand.

## Why
- Every page can be rebuilt when the core or the step format changes.
- The same input always gives the same page (the script is deterministic; the AI only writes the creative parts).
- Tests run in one place before anything is published.

## Trade-offs
- One more step: run `python3 build.py` after every change.
- Metadata is JSON, not YAML or TOML, so no packages are needed (Python on macOS may be older than 3.11). JSON is less pleasant for long text.

Depends on: — · Affects: 002, 003, 007
Revisit when: the build takes longer than about a minute, or a second person finds the workflow too hard to follow.
