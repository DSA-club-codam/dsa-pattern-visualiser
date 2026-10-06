# 017 — Page layout: animation and code on the left, state and controls on the right

Status: accepted · 2026-10-06

## Context
In the first layout everything was stacked: animation, variables, caption, controls, code. On a laptop, opening the code pushed the animation off screen, so you could follow either the animation or the code, not both. A longer caption also moved the controls, so the Next button jumped between clicks. We tried a second layout as a draft (`?layout=stage`) next to the old one before choosing.

## Options we discussed
- **A** — keep everything stacked
- **B** — variables to the right of the animation, code under the animation, caption and controls on the right

## Decision
B, with this order on the right: variables (and maps), controls, caption. The code box scrolls inside itself and keeps the highlighted line visible. Below 900px the page stacks into one column. Array indices sit above the cells, pointers below them (there was no technical reason for indices below; it came from the prototypes).

## Why
- On a 1366×768 laptop, the animation, the highlighted code line and the caption are visible at the same time.
- Controls above the caption keep the Next button in one place.

## Trade-offs
- The animation column is narrower (about 630px on a laptop). 20 cells still fit at the smallest cell size; more would scroll inside the panel.
- Long code lines scroll sideways inside the code box.

Depends on: 009, 012 · Affects: —
Revisit when: a canvas (tree, graph, grid) needs more width than the left column gives.
