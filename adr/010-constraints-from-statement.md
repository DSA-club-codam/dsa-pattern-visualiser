# 010 — The constraints block uses only the statement

Status: accepted · 2026-10-06

## Context
Constraints are the first hint of the expected complexity, and beginners often skip them. Each page has a collapsed block: constraint → what it means → what it changes, plus a rule-of-thumb table "n → what is fast enough".

## Decision
Constraints, examples and expected outputs come only from the LeetCode statement. If Claude is not sure, it asks the user to paste the statement.

## Why
- A wrong constraint teaches the wrong complexity target.

## Trade-offs
- Sometimes an extra question to the user before starting.

Depends on: — · Affects: 003
Revisit when: —
