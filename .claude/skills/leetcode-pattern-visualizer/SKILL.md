---
name: leetcode-pattern-visualizer
description: Add or change step-by-step visualisations of LeetCode solutions in this repo (problems/ → build.py → docs/). Use when the user asks to visualise, animate or "show how" a LeetCode problem or pattern works, to add an approach to a problem, to add a design element, or to record an architecture decision for the visualiser.
---

# LeetCode Pattern Visualiser

## Purpose
Each page shows how one LeetCode problem is solved, step by step, so that a beginner (0–1 year of experience) can answer:
1. Which pattern is used here, and which clues in the problem point to it?
2. What does each moving part (pointer, window, stack, map, table cell) do at each step?
3. Why is the answer correct, and why is it faster than brute force?

Audience: Codam DSA Club members preparing for entry-level interviews in the Netherlands. Scope: LeetCode Easy and core Medium. No Hard problems unless the user asks.

## Language
- Talk to the user in the language they write in.
- Everything written into the repo (code, comments, captions, JSON text, ADRs, README, ai-panic) is British English, about B1 level: conversational but professional, short sentences.
- Never use: delve, imagine, superpower, game-changer, it's worth noting, certainly, fascinatingly, in conclusion, or similar filler.

## Read before working
| File | What it is |
|---|---|
| design-system.md | Meaning of every colour role, shape, pointer name and motion rule |
| components.md | The blocks a page is made of and which blocks each pattern uses |
| schemas.md | Exact format of problem.json, approach.json, tests.json, steps, site.json |
| index-spec.md | How the home page groups and links pages |
| notion-guides.md | Public Notion guide link for each pattern |
| ../../../adr/ | Why things are built this way. Do not contradict an accepted ADR without a new ADR |

## Repo map
```
core/            shared engine and design book (tokens.css, viz.css, viz.js, index.*, gallery.html)
problems/<lc-N-slug>/              one folder per problem
    problem.json brute.py gen.py tests.json
    <approach-id>/                 one folder per approach
        approach.json solution.py solution.cpp [solution.c] canvas.js
build.py         tests everything, then writes docs/
docs/            GENERATED — never edit by hand; published by GitHub Pages
adr/             architecture decision records
ai-panic/        unlikely worries, for fun (see below)
site.json        site-wide links
```

## Hard rules
1. Never guess a problem statement, constraint, example or expected output. If you are not sure, ask the user to paste the statement.
2. Never write animation steps by hand. Steps come only from running solution.py through build.py.
3. Never edit docs/. Change sources, run `python3 build.py`.
4. A page is finished only when `python3 build.py` ends with "✓ build ok".
5. Never add a colour, shape or block that is not in core/ and gallery.html. Propose it first (workflow C).
6. No external libraries, CDNs or build tools. Plain static files, relative links only. The one exception is the GoatCounter analytics script that build.py adds to published pages (ADR 024); never add another.
7. One page per problem. Each approach is a tab on that page (ADR 006).
8. canvas.js draws only with VIZ helpers and CSS classes from core. No colour values, no sizes.
9. Git: never commit, push, open or merge a pull request, or change repository settings unless the user asks for that action in this conversation. When asked to publish: run `python3 build.py`, show `git status`, commit sources and docs/ together, then push. CI (.github/workflows/check.yml) must stay green (ADR 019).

## Workflow A — add a problem
1. **Confirm the problem.** Restate it in 2–3 lines with its constraints and examples. If you are not certain of any detail, ask the user to paste the statement. Folder name: `<short>-<id>-<slug>` with the slug from the problem URL, e.g. `lc-283-move-zeroes`; for a source without numbers, `<short>-<slug>` (e.g. `nc-...`). Fill "source" in problem.json (ADR 016).
2. **Pattern ID (in chat).** Pattern, data structure(s), 2–3 signals in the statement, brute force and its complexity, pattern complexity. If several reasonable approaches exist, list them and ask which to build first.
3. **C or not.** C only if the solution needs nothing beyond plain arrays, fixed-size counters (e.g. int count[128]) and loops. Otherwise no solution.c and a one-sentence "noC" reason in approach.json. Say the decision in chat.
4. **Write problem.json** (schemas.md): constraints table (each row: constraint → what it means → what it changes; taken only from the statement), nMax, signature, brute-force summary and ops unit, examples.
   - Examples: the LeetCode examples with their "expected" from the statement, plus your own that trigger the interesting behaviour (the window shrinks, the stack pops, binary search goes both ways).
   - "main" examples: ≤ 10 elements, aim for 15–40 steps. "edge" examples: shorter is fine. Hard limit: 20 elements.
   - Edge cases come from the constraints: smallest n, all equal, none matching, extreme values.
5. **Write brute.py** — the oracle: simplest correct solution, a function `brute(<params>)` that returns the answer (for in-place problems, the final array). Mark the operation counter line `T.op()  # @trace`. It is also shown to readers, so comment it.
6. **Write gen.py** — `gen(rng)` returns random args inside the constraints, small (n ≤ 12) and with many repeats so edge cases appear.
7. **Pattern guide.** If site.json `patternGuides` has no entry for the approach's pattern label, take the link from notion-guides.md (match by meaning: "Two pointers" = "Two Pointers") and add it. Ask the user only if no row matches.
8. **Write tests.json** — extra cases worth keeping that are not shown on the page (extreme values, n = 1).
9. **Write the approach folder** (workflow B, steps 2–5).
10. **Run `python3 build.py`.** Fix whatever it reports. Warnings about step counts: shorten or change the example.
11. **Show the user:** the Pattern ID block, the page path (docs/<folder>.html), and 1–2 sentences on what to watch in the animation. Ask them to review the captions — tests cannot check if a caption is clear.
12. **Remind the user** to submit each language on the LeetCode account and then say which ones were accepted (workflow E).

## Workflow B — add an approach
1. Folder name = approach id = URL anchor: short, lowercase, pattern + data structure, e.g. `sliding-window-hash-map`.
2. **solution.py** — the exact LeetCode signature, with:
   - `# @a:<name>` at the end of every line a step points at (same names in every language)
   - `# @trace` on single lines that only record steps; `# @trace-begin` / `# @trace-end` around blocks
   - `# @hide` on imports
   - `T.step(anchor, phase, caption, state=..., roles=..., vars=...)` at each meaningful moment; `T.op()` once per element visit (for the ops counter)
   - Removing every @trace line must leave a clean, submittable solution. build.py tests both versions.
   - Write it so it could be ported to JavaScript line by line later (ADR 005): no clever Python-only tricks in the logic.
3. **solution.cpp** (always) and **solution.c** (only if allowed): same logic, same anchor names (`// @a:<name>`), `// @hide` on includes and `using namespace std;`. Use long long where overflow is possible, `mid = lo + (hi - lo) / 2`.
4. **approach.json** — name, pattern, ds, complexity, pattern card (signals, pattern, core idea), invariant, phase labels, legend (only roles used on this page; not shown for now but always written, ADR 023), whenToUse, accepted: [].
5. **canvas.js** — an object `({ build(ctx) {...}, render(step, ctx, flash) {...} })`. Pick the canvas from components.md. Map the semantic state from solution.py to VIZ helpers. If two approaches need the same new canvas, move it into core as a helper (with approval).
6. If the approach brings a new pattern label, add its guide link (workflow A, step 7).
7. Run build.py and review as in workflow A.

## Workflow C — a new design element
When a problem needs something core does not have (a tree, a graph, a new role colour):
1. Stop before writing the page.
2. Describe 1–3 options in words (and a quick sketch if useful), using existing tokens where possible.
3. Wait for the user's choice.
4. Add it to core/ (tokens.css for values, viz.css/viz.js for the component), to gallery.html, and to design-system.md / components.md.
5. If it changes a rule, write an ADR (workflow D).
6. Only then build the page.

## Workflow D — architecture decisions (ADR)
Whenever the user and you decide something about how the project works (not a single page's content), draft `adr/NNN-short-title.md` from adr/000-template.md and show it for approval. Rules:
- Only options that were really discussed. Only risks that can really happen in this project.
- Every ADR has "Depends on", "Affects" and a concrete "Revisit when" trigger.
- To change a decision, write a new ADR that supersedes the old one; set the old one's status to "superseded by NNN".

## Workflow E — LeetCode acceptance
When the user says a language was accepted on LeetCode, add it to "accepted" in approach.json (`python`, `cpp`, `c`) and rebuild. The ✓ appears on that language's tab.

## ai-panic/
When you notice yourself worrying about something unlikely ("what if LeetCode renames every slug"), write it as a short, light-hearted file in ai-panic/ instead of adding complexity. One file per worry: what could go wrong, how likely, what we would do. ADRs never cite ai-panic as a reason. The user will check one day which ones came true.

## Pointer names (ADR 011, ADR 021)
| Pattern | Names | Role colour |
|---|---|---|
| Two pointers towards each other | left / right | back / front |
| Sliding window | left / right | back / front |
| Same direction (read/write), linked list | slow / fast | back / front |
| Two arrays, merge (ADR 021) | p1 / p2 / write | front / front / back |
| Binary search | lo / mid / hi | back / mid / front |
Code variable names must match the labels on the canvas.

## Captions
- Each caption says what happened and why, in 1–2 sentences, using the code's variable names.
- Name the decision, not only the action: "nums[mid] = 7 > target, so the target can only be in the left half", not "move hi".
- Every new round of a loop gets its own step on the loop header (`for` / `while` line), so the reader sees the loop start again. A `while` that runs gets a step on its line before the body ("while count[2] = 3 > k: the loop runs"); the step where it stops says so in its caption.
- The last step states the result and one sentence on why it is correct.
- The invariant is the rule the pattern keeps true; put it in approach.json (or per step if it changes).

## Final checklist
- [ ] Statement, constraints and examples confirmed, not guessed
- [ ] Pattern ID shared in chat
- [ ] Python3 + C++17; C only if allowed, else a noC reason
- [ ] `python3 build.py` ends with "✓ build ok"
- [ ] Main examples ≤ 10 elements and 15–40 steps (or the warning is understood)
- [ ] Only existing design elements used, or new ones approved and added to the gallery
- [ ] User asked to review captions and to submit to LeetCode
- [ ] ADR drafted if a project-level decision was made
