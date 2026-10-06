---
name: leetcode-pattern-visualizer
description: Build a step-by-step interactive HTML visualisation of how a specific LeetCode problem is solved, making the algorithmic pattern (two pointers, sliding window, binary search, monotonic stack, BFS/DFS, DP, etc.) visually obvious. Use when the user asks to visualise, animate, or "show how" a LeetCode solution or pattern works.
---

# LeetCode Pattern Visualiser

## Purpose
Turn the solution of one specific LeetCode problem into a visual, step-by-step walkthrough. After watching it, a beginner (0–1 year experience) should be able to answer three questions:
1. Which pattern is used here?
2. What does each moving part (pointer, window, stack, queue, table cell) do at each step?
3. Why does the pattern give the correct answer, and why is it faster than brute force?

Audience: Codam DSA Club members preparing for entry-level interviews in the Netherlands. Scope: LeetCode Easy and core Medium. Do not visualise Hard problems unless the user asks directly.

---

## Input
The user gives one of:
- A problem number and/or title, e.g. "Visualise LC 3 Longest Substring Without Repeating Characters"
- A pasted problem statement
- Their own solution code to visualise

Optional: a specific example input, a language for the code panel (default: Python3), a pattern to highlight if the problem can be solved several ways.

---

## Workflow — follow in order

### Step 1 — Confirm the problem
- If you know the problem well and are confident of its exact statement and constraints, restate it in 2–3 lines.
- If you are not confident (unusual number, recent problem, unclear title), ask the user to paste the statement. Never guess a problem statement.
- If the user supplied their own solution, visualise their code, not yours. If their code has a bug, say so before building anything.

### Step 2 — Identify the pattern
Write a short "Pattern ID" block for the user (in chat, not in the file yet):
- **Pattern:** name
- **Signals in the problem:** the 2–3 clues that point to it (e.g. "contiguous subarray" + "longest/shortest" → sliding window)
- **Brute force:** what it would be and its complexity
- **Pattern solution complexity:** time and space
- If two patterns both work, name both, pick the one more common in interviews, and state why in one sentence.

### Step 3 — Choose the example input
- Small: 6–10 elements for arrays/strings, up to ~12 nodes for trees/graphs, up to 6×6 for grids/DP tables.
- The example must trigger the interesting behaviour of the pattern (e.g. the window must shrink at least once; the stack must pop at least once; binary search must go both left and right).
- Prefer the official LeetCode example if it shows the behaviour; otherwise design your own and say so.

### Step 4 — Generate the trace by running real code
Never write trace steps by hand.
1. Write a reference solution in Python3 in a scratch file.
2. Instrument it: at every meaningful moment, append a step object to a list (schema below).
3. Run it with Bash. Check that the final answer matches the expected output. If it does not, fix the code before continuing.
4. Save the steps as JSON and embed them in the HTML.

Step object schema:
```json
{
  "line": 7,
  "phase": "expand | shrink | compare | push | pop | visit | fill | return",
  "state": { "arr": [], "pointers": {"l": 0, "r": 3}, "window": [0, 3], "stack": [], "queue": [], "map": {}, "table": [], "best": 3 },
  "highlight": { "cells": [3], "roles": {"3": "current"} },
  "caption": "r moves to index 3. 'b' is already in the window, so the window must shrink.",
  "invariant": "The window [l, r] never contains a repeated character."
}
```
Include only the state fields the pattern needs.

What counts as a step: a pointer move, a window expand/shrink, a push/pop, a node visit, a table cell filled, an answer update. Not every loop iteration needs several steps — aim for 15–40 steps in total. If there are more, shorten the input.

### Step 5 — Render the HTML
One self-contained file: inline CSS and JS, no build step, no external dependencies, works offline by opening it in a browser.

Layout, top to bottom:
1. **Header:** problem number, title, pattern name as a coloured badge, time/space complexity.
2. **Pattern card (collapsible):** signals, brute force vs pattern, one-sentence core idea.
3. **Main canvas:** the data structure drawn with the pattern's visual vocabulary (table below).
4. **Side panel:** code with the current line highlighted; auxiliary state (hash map contents, stack, queue, current best answer).
5. **Caption bar:** the step caption (what happened and why) and the invariant in a smaller line beneath.
6. **Controls:** Reset, Prev, Play/Pause, Next, speed slider, step counter "Step 7 / 23". Keyboard: left/right arrows, space for play/pause.
7. **Legend:** every colour and shape used, with its role.

Visual rules:
- One colour per role, the same across the whole file (e.g. left pointer blue, right pointer orange, current element yellow, done/discarded grey, answer green, conflict red). Always show the legend.
- Never rely on colour alone: pointers also get text labels (l, r, mid, slow, fast); discarded cells also get a strike or reduced opacity.
- Animate transitions (pointer slides, window stretches, stack pops) with short CSS transitions, 200–400 ms. No decorative animation.
- Show the index under every array cell.
- The best-so-far answer must always be visible and must flash green when it updates.
- The final step shows the result and a one-line summary of why it is correct.
- Support light and dark mode via prefers-color-scheme.
- Must be readable at 375px width (stack panels vertically).

### Step 6 — Verify
Before handing over:
- Open the file with a headless browser or at minimum parse it (node or python) to check there are no JS errors.
- Confirm step count, the final answer in the last step, and that every step's highlighted code line exists.
- Click-through check: first step, a middle step, last step render without overlap.

### Step 7 — Deliver
- Save to visualisations/lc-<number>-<slug>.html (create the folder if needed).
- In chat: the Pattern ID block from Step 2, the file path, and 1–2 sentences on what to watch for in the animation.
- Optional, only if the user asks: an ASCII version of 3–5 key frames for Notion (no inline backticks in prose; ASCII inside a code block).

---

## Pattern → Visual Vocabulary

| Pattern | What to draw | Key moments to capture as steps |
|---|---|---|
| Two pointers (opposite ends) | Array row, two labelled arrows below cells | Compare, move left, move right, pointers meet |
| Fast & slow pointers | Linked list as boxes with arrows; two labelled markers | Each move; the meeting point; cycle entry |
| Sliding window (variable) | Array row with a translucent bracket over the window; side panel with window contents/counts | Expand, condition broken, shrink, best updated |
| Sliding window (fixed) | Same, bracket of constant width | Add right element, remove left element, compare |
| Binary search | Sorted array; greyed-out discarded halves; lo/mid/hi labels | Compute mid, compare, discard half, termination |
| Prefix sum | Original array above, prefix array below, arrow showing how a range sum = two lookups | Build prefix, answer each query |
| Hash map lookup | Array row + map panel (key → value) | Check complement, hit/miss, insert |
| Monotonic stack | Array row + vertical stack drawn bottom-up | Push, pop (with the reason: "smaller than current"), answer recorded on pop |
| Heap / top-k | Array row + heap drawn as tree and as array | Push, pop root, heap size kept at k |
| Intervals (sort + merge) | Horizontal number line with bars | Sort, compare with last merged, merge or append |
| BFS on grid/graph | Grid or node-link graph; queue panel; colour by distance level | Dequeue, enqueue neighbours, mark visited, level complete |
| DFS / backtracking | Recursion tree growing on the right; current path highlighted | Choose, recurse, hit base case, undo choice |
| Tree traversal | Binary tree; visit order numbers appear on nodes; call stack panel | Enter node, visit, return |
| 1D / 2D DP | Table; arrows from the cells each new cell depends on | Fill each cell with the recurrence written in the caption |

If the problem uses a pattern not in this table, design the vocabulary on the same principle: draw the data, mark each moving part with a labelled shape, and capture every decision as a step.

---

## Captions — writing rules
- Every caption answers "what happened" and "why" in one or two sentences.
- Name the decision, not just the action: "nums[mid] = 7 > target, so the target can only be in the left half" — not "move hi".
- Use the same variable names as the code panel.
- British English, B1 level, conversational but professional.
- No filler words: delve, imagine, superpower, game-changer, it's worth noting, certainly, fascinatingly, in conclusion.

## Code panel rules
- Default language Python3. If the user asks, add a C++17 tab with the same line structure so the highlight still maps correctly.
- Short line-by-line comments.
- Include guards where relevant: empty input check, l + (r - l) // 2 for mid, bounds checks before access.
- The code shown must be the exact code that produced the trace (minus instrumentation lines).

---

## Do not
- Do not invent a problem statement, constraints, or expected output.
- Do not hand-write trace steps.
- Do not add external libraries or CDN links.
- Do not show more than one pattern per file. For a comparison, build two files and say so.
- Do not explain the whole theory of the pattern — one core-idea sentence plus the visual is enough.

---

## Final checklist
- [ ] Problem statement confirmed, not guessed
- [ ] Pattern named with signals, brute force and pattern complexity
- [ ] Example input triggers the interesting behaviour
- [ ] Trace generated by running code; final answer verified
- [ ] 15–40 steps, each with caption + invariant
- [ ] Code line highlight matches each step
- [ ] Legend present, colours consistent, labels not colour-only
- [ ] Works offline, light/dark mode, readable on mobile
- [ ] No JS errors
- [ ] Saved to visualisations/lc-<number>-<slug>.html
