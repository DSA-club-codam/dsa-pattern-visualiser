# Components — page blocks

`VIZ.mount(PAGE)` in core/viz.js builds every block below from data. A page never re-implements them. Only the canvas (block 7) is written per approach, in canvas.js, using the helpers listed here.

## Page order
| # | Block | Shown | Data |
|---|---|---|---|
| 1 | Header: "LC N · Title", difficulty, Open on <site> ↗ | always | problem.source |
| 2 | Meta: pattern badge, data-structure badges, time · space, Big-O ↗ | always (changes with the tab) | approach |
| 3 | Approach tabs | only with 2+ approaches | approaches |
| 4 | Compare approaches (collapsed table) | only with 2+ approaches | approach.time/space/whenToUse |
| 5 | Constraints — what they tell you (collapsed): table + "n → fast enough" rule of thumb with the matching row highlighted | always | problem.constraints, problem.nMax |
| 6 | Why this pattern? (collapsed): signals, brute force, pattern, core idea, ops counter "on this input", brute-force code (collapsed) | always | approach.card, problem.bruteForce, example.ops |
| 7 | Examples / Edge cases buttons | always | problem.examples (kind main / edge) |
| 8 | Canvas | always | canvas.js |
| 9 | Side panels: Variables (always) + extra panels from canvas.js | always | step.vars |
| 10 | Caption: phase tag, caption, invariant | always | step |
| 11 | Controls: Reset, Prev, Play/Pause, Next, speed, "Step n / N"; keys ← → Space Home | always | — |
| 12 | Code drawer (collapsed "Show code"): tabs Python3 · C++17 · C, ✓ if accepted, current line highlighted via anchors, "Copy" button (copies the open tab's code without line numbers), "No C version: …" note. Line numbers are drawn by CSS (`.ln::before { content: attr(data-n) }`), so selecting and copying never includes them | always | approach.code |
| 13 | Legend (collapsed, at the bottom) | always | approach.legend |
| 14 | Footer: All visualisations, Notion guides, Big-O, LeetCode profile (if set) | always | site.json |

## Layout (ADR 017)
- From 900px: left column = canvas, code drawer under it; right column = side panels, controls, caption. Controls sit above the caption so the Next button stays in place. The code box scrolls inside itself (max 60% of the screen height) and keeps the highlighted line in view.
- Below 900px: one column — canvas, side panels, controls, caption, code.
- Inside the array row, top to bottom: band labels, swap arc, indices, cells, pointers, best bar.

## Links to a tab
`lc-2958-....html#sliding-window-hash-map` opens that approach. Switching tabs updates the address, so a copied URL points at the open approach. An unknown anchor opens the first approach.

## Canvas helpers (core/viz.js)
| Helper | Draws | Typical patterns |
|---|---|---|
| `new VIZ.ArrayRow(host, values, {roles, bar})` + `.update({arr, ids, cls, tags, bands, arc, pointers, bar})` | one array with indices, pointers (back/front/mid rows), bands (window/best/gap) with labels, swap arc, best bar; cells keyed by identity so swaps slide | two pointers, sliding window, binary search, prefix sum, Kadane, 1D DP |
| `VIZ.vars(host, vars, flash)` | variables list; flashes values marked flash | every page (automatic) |
| `VIZ.countMap(host, rows, limit, title)` | value → count with slots, over-limit row in red | frequency limits, anagram windows |
| `VIZ.kvMap(host, rows, title)` | key → value table, rows marked hit / new | Two Sum style lookups |
| `VIZ.stack(host, items, title)` | vertical stack, top marked | monotonic stack, parentheses, iterative DFS |
| `VIZ.queue(host, items, title)` | horizontal queue, front → back | BFS |
| `<h3>` inside the canvas | a title above each row when the canvas has several ArrayRows (same style as side-panel titles) | merge, prefix sum |
| `ctx.extraPanel()` | adds one more side panel for the canvas to draw into | anything with a map/stack/queue |

## Not built yet (workflow C before first use)
| Canvas | For |
|---|---|
| Grid | BFS/DFS on a grid, 2D DP |
| LinkedList | fast & slow pointers, reversal |
| Tree | traversals, BST |
| Graph | BFS/DFS on graphs, topological sort |
| NumberLine | intervals |
| RecursionTree | backtracking |
Rule: build it inside canvas.js the first time if it is truly one-off; the second time a canvas type is needed, move it into core as a helper.

## Pattern → blocks
| Pattern | Canvas | Extra panels | Steps to capture |
|---|---|---|---|
| Two pointers (towards each other) | ArrayRow | — | compare, move left, move right, meet |
| Two pointers (same direction) | ArrayRow + arc | — | check, skip, swap/write, advance |
| Two pointers (two arrays, merge) | two ArrayRows, each under an `<h3>` title | — | compare, copy the larger/smaller, move reader and write, stop |
| Fast & slow (linked list) | LinkedList | — | each move, meeting point, cycle entry |
| Sliding window — variable size (pattern label: "Sliding window") | ArrayRow + window band + bar | countMap or kvMap | expand, conflict, shrink, best updated |
| Sliding window — fixed size (pattern label: "Sliding window") | ArrayRow + window band | — | add right, remove left, compare |
| Binary search | ArrayRow (out cells) + lo/mid/hi | — | compute mid, compare, discard half, stop |
| Prefix sum | two ArrayRows | — | build prefix, answer query |
| Hash map lookup | ArrayRow | kvMap | check complement, hit/miss, insert |
| Monotonic stack | ArrayRow | stack | push, pop with reason, answer on pop |
| Intervals | NumberLine | — | sort, compare with last, merge or append |
| BFS | Grid or Graph | queue | dequeue, enqueue neighbours, level done |
| DFS / backtracking | RecursionTree | stack | choose, recurse, base case, undo |
| 1D DP | ArrayRow | — | fill cell with the recurrence |
| 2D DP | Grid | — | fill cell, dependency arrows |
