# 023 — No legend on problem pages for now

Status: accepted · 2026-10-06

## Context
Every problem page had a collapsed "Legend" panel at the bottom. Pointers are labelled, captions name what happens, and design-system.md never lets colour carry meaning alone, so the legend repeats what the page already says. We were tidying the page layout (no footer, a "← Main page" link, a pattern-guide link in the meta row) and asked whether the legend earns its place.

## Options we discussed
- **A** — keep the legend panel as it is
- **B** — remove the panel, but keep "legend" in approach.json and keep writing it for new problems
- **C** — remove the panel and the data

## Decision
B. Problem pages do not show a legend. approach.json keeps its "legend" list, build.py still requires it, and every new approach still writes it. VIZ.legend stays in core and in the gallery, so the panel can come back with a few lines in viz.js.

## Why
- YAGNI: nobody has asked what a colour means yet.
- Labels, captions and non-colour signals already explain each mark.
- Keeping the data costs a few lines per approach and makes the way back cheap.

## Trade-offs
- A reader who wants a key for a colour has to read the caption or the labels.
- The legend data is written but not seen, so mistakes in it can go unnoticed until it is shown again.

Depends on: 002, 017 · Affects: —
Revisit when: club members ask what a colour or mark means.
