# 002 — Shared core instead of a copied template

Status: accepted · 2026-10-06

## Context
The first plan was "copy template.html for every page". The two prototype pages already showed drift: the same pointer role had two token names (--write / --l), and one page was not adapted to phones.

## Options we discussed
- **A** — copy a template into each page
- **B** — one shared core (`core/tokens.css`, `viz.css`, `viz.js`) that every page loads, plus a live gallery page

## Decision
B. The design book has two parts: the description (`.claude/skills/.../design-system.md`, `components.md`) and the implementation (`core/`). Colour and size values exist only in `core/tokens.css`. `docs/gallery.html` shows every element live. A new element is proposed to the user first, then added to core and the gallery, and only then used on a page.

## Why
- A design fix reaches every page at once.
- One source of truth for values, so the description and the code cannot disagree about a hex code.
- The gallery lets a non-frontend person review the design by looking, not by reading CSS.

## Trade-offs
- A change in core can break an older page. Mitigation: build.py rebuilds every page and the smoke test opens each one.
- Pages are no longer single self-contained files; they need the `core/` folder next to them.

Depends on: 001 · Affects: 011, 012
Revisit when: a core change breaks a page that the smoke test did not catch.
