# 024 — GoatCounter analytics: the one external script

Status: accepted · 2026-10-06

## Context
The club wants to know which pages members open, so we can see which patterns get used and which pages to improve. ADR 008 says pages load nothing from outside the repo. Counting visits needs a script from an analytics service, so this is the first exception.

## Options we discussed
- **A** — no analytics (keep ADR 008 as it is)
- **B** — GoatCounter, loaded on published pages only

## Decision
B. build.py adds the official GoatCounter script to every problem page and to the main page, but not to the gallery:

`<script data-goatcounter="https://<code>.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>`

The site code lives in site.json ("goatcounter", now "dsa-visualiser"). When it is empty, no script is added. This is the only external script; ADR 008 still holds for everything else.

## Why
- No cookies and no personal data: GoatCounter counts page views without tracking people, so no consent banner is needed.
- The site still works if the script is blocked or offline: it loads async and no page code depends on it.
- One line in site.json turns it off.
- The smoke test serves an empty script instead of the real one, so CI never depends on GoatCounter.

## Trade-offs
- Pages contact a third-party server on every view.
- Counts are rough: ad blockers hide some visits, and local file views are not counted.
- The snippet uses https:// instead of the official protocol-relative //, so it does not break pages opened as local files.

Depends on: 008, 019 · Affects: 008
Revisit when: GoatCounter changes its privacy terms or stops being free for the club, or someone asks for a second external script.
