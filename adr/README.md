# Architecture decision records

Why the visualiser is built the way it is. One file per decision. To change a decision, write a new ADR and mark the old one "superseded by NNN". Template: 000-template.md.

| # | Decision |
|---|---|
| 001 | Sources are separate from built pages |
| 002 | Shared core instead of a copied template |
| 003 | Correctness: brute-force oracle, random tests, all languages |
| 004 | Python3 and C++17 always, C only for simple array problems |
| 005 | Precomputed examples now, custom input later |
| 006 | One page per problem; approaches are tabs |
| 007 | The catalogue and home page are generated |
| 008 | Static site, no dependencies, GitHub Pages from docs/ |
| 009 | Pages work on phones |
| 010 | The constraints block uses only the statement |
| 011 | Pointer names follow the pattern; colours follow the role |
| 012 | Size limits: 10 for presets, 20 for the renderer |
| 013 | Brute force on the page: code and an operation counter, no animation |
| 014 | LeetCode acceptance is recorded by hand |
| 015 | Home page is a plain table; gallery and ADRs are not linked |
| 016 | Problems are not tied to LeetCode |
| 017 | Page layout: animation and code on the left, state and controls on the right |
| 018 | Pattern names stay broad |
