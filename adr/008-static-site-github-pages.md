# 008 — Static site, no dependencies, GitHub Pages from docs/

Status: accepted · 2026-10-06

## Decision
Pages are plain HTML, CSS and JavaScript: no frameworks, no CDN, no build tools in the browser. Links are relative, so the site works from a repo sub-path on GitHub Pages and when opened as local files. GitHub Pages serves the `docs/` folder of the main branch.

## Why
- Works offline and on any host.
- Nothing to update or break in a year.

## Trade-offs
- Every UI feature is written by hand in core/viz.js.

Depends on: — · Affects: 002, 007
Revisit when: core/viz.js becomes too large to change safely.
