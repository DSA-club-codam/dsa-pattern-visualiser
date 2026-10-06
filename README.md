# DSA Club · Pattern Visualiser

**Open the site: https://dsa-club-codam.github.io/dsa-pattern-visualiser/**

Step-by-step animations of coding-interview problems, grouped by algorithmic pattern. Made for the Data Structures & Algorithms club at Codam.

Each problem page shows:
- which clues in the problem statement point to the pattern
- what every pointer and data structure does at each step, next to the line of code that runs
- the constraints and what they tell you about the complexity you need
- why the pattern beats brute force, with an operation count on the same input
- the solution in Python3 and C++17, and in C where it fits the problem

Every solution is checked against a brute-force answer and across languages before a page is published.

Pattern theory lives in the club's guides on Notion: [Pattern guides](https://cosmic-ray-317.notion.site/2c5b90a8e089805cb323c5733701f9cf?v=2c5b90a8e089806f831a000c62ebfca1).

## Contributing
Ideas, corrections and pull requests are welcome. Open an issue to suggest a problem, report an unclear explanation or a bug. For pull requests, read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## Repo
| Path | What |
|---|---|
| `problems/` | sources: one folder per problem, one subfolder per approach |
| `core/` | shared page engine and design system |
| `build.py` | tests every solution, then builds the site |
| `docs/` | the published site (generated, do not edit) |
| `adr/` | why the project is built this way |
| `.claude/skills/` | instructions Claude Code follows when it adds a problem |
| `ai-panic/` | worries that did not deserve code |
