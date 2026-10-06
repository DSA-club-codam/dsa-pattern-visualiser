# 015 — Home page is a plain table; gallery and ADRs are not linked

Status: accepted · 2026-10-06

## Context
The first home page had cards, group-by buttons, filters and complexity chips. Looking at it in a browser, it felt like too much for what readers need: find a problem and open it.

## Options we discussed
- **A** — cards grouped by pattern / data structure / problem, with filters
- **B** — one simple table: # · problem · difficulty · pattern · data structure · guide

## Decision
B. One row per problem; a problem with several approaches shows one line per approach in the pattern, data-structure and guide columns, each pattern linking to its tab. Columns sort on click. No complexity on the home page. The design gallery and the ADRs are not linked from published pages: they are for reviewers and stay in the repo (the gallery is still built into docs/).

## Why
- Faster to scan, nothing to learn.
- Sorting by pattern gives the grouping without extra controls.

## Trade-offs
- No filters. With many problems, sorting may not be enough.

Depends on: 007 · Affects: —
Revisit when: the table has more than about 50 rows and people ask for filters.
