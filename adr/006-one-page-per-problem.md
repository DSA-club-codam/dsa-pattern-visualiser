# 006 — One page per problem; approaches are tabs

Status: accepted · 2026-10-06

## Context
Some problems have several good approaches (different pattern or data structure). We first planned one page per approach, then considered tabs on one page.

## Options we discussed
- **A** — one page per approach, linked with "Other approaches"
- **B** — one page per problem, each approach a tab

## Decision
B. The address of a tab is the page plus `#<approach-id>` (the folder name), e.g. `lc-2958-....html#sliding-window-hash-map`. Opening that link opens the tab; switching tabs updates the address. A "Compare approaches" table appears when there are two or more.

## Why
- Comparing approaches on the same input is easier on one page.
- Links stay stable. Moving from A to B later would have broken links already pasted into Notion.

## Trade-offs
- Pages with several approaches are larger (a few kilobytes).
- The tab switcher is built but only appears with 2+ approaches; it has not been used on a real problem yet.

Depends on: 001 · Affects: 007
Revisit when: a page has so many approaches that it becomes slow or hard to read.
