# Schemas — every file build.py reads

schemaVersion: 1. All files are plain JSON (no comments, no trailing commas). Python 3.8+ and no packages, so no YAML/TOML.

## problems/<lc-N-slug>/problem.json
```json
{
  "schemaVersion": 1,
  "title": "Move Zeroes",
  "source": { "site": "LeetCode", "id": "283", "url": "https://leetcode.com/problems/move-zeroes/" },
      // site: shown as "Open on <site>"; id: optional (shown as "LC 283"); short: optional prefix,
      // defaults LeetCode → LC, NeetCode → NC
  "difficulty": "Easy",                  // Easy | Medium | Hard
  "nMax": 10000,                         // largest n from the constraints; highlights the rule-of-thumb row
  "signature": {
    "python": "moveZeroes", "cpp": "moveZeroes", "c": "moveZeroes",
    "params": [{ "name": "nums", "type": "int[]" }],   // int | long | int[] | long[] | string
    "returns": "void",                                  // void | int | long | bool | int[]
    "inPlace": "nums",                                  // required when returns = void
    "judge": "sortedPrefix"                             // optional (ADR 025): returns int k; the answer is
                                                        // sorted(inPlace[:k]), like LeetCode's custom judge
  },
  "constraints": [{ "text": "1 ≤ nums.length ≤ 10⁴", "meaning": "...", "impact": "..." }],
  "bruteForce": { "summary": "...", "opsUnit": "element checks" },
  "examples": [
    { "id": "lc1", "label": "LeetCode Example 1: [0,1,0,3,12]", "kind": "main",
      "args": { "nums": [0, 1, 0, 3, 12] }, "expected": [1, 3, 12, 0, 0] }
  ]
}
```
- `examples` are tested AND animated. `expected` only when it comes from the statement.
- `kind`: `main` (≤ 10 elements, 15–40 steps) or `edge`.
- More param or return types: extend `make_driver()` in build.py first.

## problems/<…>/brute.py
`def brute(<params in signature order>)` → answer (in-place problems: the final array; judge "sortedPrefix": the sorted first k elements). One `T.op()  # @trace` per basic operation. Shown on the page (minus @trace lines).

## problems/<…>/gen.py
`def gen(rng)` → dict of args inside the constraints. `rng` is `random.Random` with a fixed seed, so runs repeat.

## problems/<…>/tests.json (optional)
`[{ "name": "...", "args": {...}, "expected": ... }]` — tested, not animated. `expected` optional (brute force is the answer when missing).

## problems/<…>/<approach-id>/approach.json
```json
{
  "order": 1,                                  // tab order
  "name": "Sliding window + hash map",         // tab label
  "pattern": "Sliding window (variable)",      // groups the home page; keep names consistent
  "ds": ["Hash map"],
  "time": "O(n)", "space": "O(n)",
  "whenToUse": "...",                          // compare table
  "noC": "...",                                // required when there is no solution.c
  "card": { "signals": "...", "pattern": "...", "coreIdea": "..." },
  "invariant": "...",
  "phases": { "expand": "expand", "update": "best ↑" },   // phase → tag text
  "legend": [{ "swatch": "ptr-back", "text": "left: left edge of the window" }],
  "accepted": ["python", "cpp"]                // languages accepted on LeetCode
}
```

## Source markers
| Marker | Python | C / C++ | Effect |
|---|---|---|---|
| anchor | `# @a:name` | `// @a:name` | the line a step with anchor "name" highlights |
| hide | `# @hide` | `// @hide` | runs, never shown (imports, includes) |
| trace line | `# @trace` | — | runs only when tracing, never shown |
| trace block | `# @trace-begin` … `# @trace-end` | — | same, for several lines |
Markers must be the last thing on the line. A display comment goes before the marker: `slow = 0  # next free slot  # @a:init`.

## Step (what T.step records)
```json
{
  "anchor": "expand",                 // must exist in every language
  "phase": "expand",                  // free text; approach.phases maps it to a tag
  "caption": "right = 3: add 1. ...",
  "invariant": "...",                 // optional; overrides approach.invariant
  "state": { ... },                   // semantic state; canvas.js reads it
  "roles": { "3": "current" },        // position → role
  "vars": [{ "label": "left", "value": 0, "role": "back", "flash": false }]
}
```
State is a full snapshot (not a diff), so any step can be shown on its own (Prev, jump, future custom input).

## canvas.js
```js
({
  build(ctx) { /* create helpers once per example: ctx.canvas, ctx.extraPanel(), ctx.example.args */ },
  render(step, ctx, flash) { /* pure: draw this step only from step + ctx */ },
})
```
`ctx` = { canvas, aux, approach, example, problem, extraPanel() }. build.py wraps it as `VIZ.canvas.register("<problem>/<approach>", …)`.

## site.json
```json
{
  "title": "...", "intro": "...",
  "notionPatterns": "https://...",          // general pattern guides page
  "patternGuides": { "Sliding window (variable)": "https://..." },  // optional per-pattern links
  "bigO": "https://www.bigocalc.com/",
  "leetcodeProfile": "",                    // empty = hidden
  "repoUrl": "",                            // empty = "Source on GitHub" link hidden
  "goatcounter": "",                        // GoatCounter site code (ADR 024); empty = no analytics script
  "articles": [{ "title": "...", "url": "https://dev.to/...", "tags": ["Sliding window (variable)"] }]
}
```
