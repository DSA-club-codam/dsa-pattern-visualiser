# Contributing

Thank you for helping. Every change is reviewed by the club lead before it is merged.

## Issues
Open an issue to:
- suggest a problem or a pattern to visualise
- report an explanation that is unclear or wrong
- report a bug (please say which page, which example and which step)

## Pull requests

### The one rule
`docs/` is generated. Never edit it by hand. Change the sources (`problems/`, `core/`, `site.json`) and rebuild.

### Build locally
You need Python 3.8+ and a C/C++ compiler (macOS: `xcode-select --install`). No packages.
```
python3 build.py
```
Then open `docs/index.html` in a browser. Commit both your sources and the rebuilt `docs/`.

`build.py` refuses to write the site if anything fails:
1. every solution is compared with a brute-force solution on the examples, `tests.json` and 200 random inputs
2. C++ and C are compiled with all warnings as errors and checked on the same inputs
3. the animation steps are recorded by running the real Python solution
4. pages are assembled
5. pages are opened in a headless browser, if [Playwright](https://playwright.dev/python/) is installed (optional: `pip3 install playwright && python3 -m playwright install chromium`). Without it, only the JavaScript syntax is checked.

### Automatic check
Every pull request runs the same `build.py` on GitHub (Actions → "Check"). It also fails when `docs/` does not match the sources, so always commit the rebuilt `docs/`. A pull request is only merged when the check is green.

### Adding a problem
The format of every file is in `.claude/skills/leetcode-pattern-visualizer/schemas.md`, and the step-by-step process in `SKILL.md` next to it. If you use Claude Code in this repo, it picks up that skill automatically.

In short, a problem folder has `problem.json`, `brute.py`, `gen.py`, `tests.json`, and one folder per approach with `approach.json`, `solution.py`, `solution.cpp`, optionally `solution.c`, and `canvas.js`.

### Before changing how things work
Read `adr/`. If your change goes against an accepted decision, open an issue first.

### Writing style
British English, simple and short sentences (about B1 level). No filler words such as "delve", "imagine", "it's worth noting".
