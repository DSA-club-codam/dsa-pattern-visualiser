# DSA Club · Pattern Visualiser

Step-by-step animations of LeetCode solutions, grouped by algorithmic pattern, for the Data Structures & Algorithms club at Codam.

Each page shows one problem: which clues in the statement point to the pattern, what every pointer and data structure does at each step, and why the pattern beats brute force. Code is in Python3 and C++17, and in C where it makes sense.

## How it works
```
problems/<problem>/            sources: statement data, brute force, tests, solutions
        │
        ▼
python3 build.py               1. every solution vs a brute-force oracle (examples + 200 random inputs)
        │                      2. C++ and C compiled and checked on the same inputs
        │                      3. traced Python records the animation steps
        │                      4. pages, home page and catalogue assembled
        ▼                      5. headless-browser smoke test (if Playwright is installed)
docs/                          the published site (GitHub Pages)
```
A page is only written when every check passes. Animation steps are never written by hand: they come from running the real solution.

## Build
Needs Python 3.8+, a C++17 compiler and a C compiler (on macOS: `xcode-select --install`). No packages.
```
python3 build.py
open docs/index.html
```
Optional full browser check: `pip3 install playwright && python3 -m playwright install chromium`.

## Repo
| Path | What |
|---|---|
| `problems/` | one folder per problem, one subfolder per approach |
| `core/` | shared engine and design system; live preview in `docs/gallery.html` |
| `build.py` | tests and builds everything |
| `docs/` | generated site — do not edit |
| `adr/` | why it is built this way |
| `.claude/skills/leetcode-pattern-visualizer/` | instructions Claude Code follows to add problems |
| `ai-panic/` | worries that did not deserve code |

## How it was made
Built with Claude Code. The AI writes solutions, captions and page code following the skill in `.claude/skills/`. Correctness does not depend on trusting the AI: `build.py` checks every solution against an independent brute force and across languages before anything is published, and each solution is also submitted to LeetCode. Design and architecture decisions were made together and are recorded in `adr/`.

## Publish
GitHub → Settings → Pages → Deploy from a branch → `main`, folder `/docs`.
