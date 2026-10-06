# 012 — Size limits: 10 for presets, 20 for the renderer

Status: accepted · 2026-10-06

## Context
On a 375px phone about 9 cells fit at the smallest size. Long inputs also make long animations (Move Zeroes: 21 steps for 9 elements).

## Decision
- "main" examples: at most 10 elements, aim for 15–40 steps (build.py warns otherwise).
- Renderer: up to 20 elements (build.py fails above that). Above about 9 on a phone, the array scrolls inside its panel.

## Trade-offs
- Some LeetCode examples are longer than 10; they can be shown as "edge" examples or shortened.

Depends on: 005, 009 · Affects: —
Revisit when: real use shows the numbers are wrong. We set them before using them, so they are a first guess.
