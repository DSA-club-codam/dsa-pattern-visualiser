# 025 — Custom judge: sorted first k elements

Status: accepted · 2026-10-09

## Context
LC 27 Remove Element returns k and changes nums in place. LeetCode's custom judge checks k, sorts nums[0..k-1] and compares it with the expected array. The rest of nums and the order inside the first k do not matter. build.py could compare only a plain return value or the whole in-place array, so a correct solution that leaves a different tail or order would fail.

## Options we discussed
- **A** — a `"judge"` field in the signature that names how answers are compared; the first one is `"sortedPrefix"`
- **B** — force one fixed order and tail in brute.py, so the plain comparison works

## Decision
`signature.judge = "sortedPrefix"` (with `returns: "int"` and `inPlace`): the answer is `sorted(inPlace[:k])`. build.py applies it to Python, and the C / C++ drivers print the same sorted prefix. A k outside 0..n prints `{"badK": k}` and fails the test. brute.py returns the sorted kept values, which is also what the statement's expected arrays look like.

## Why
- It copies LeetCode's own rule, so every solution that LeetCode accepts also passes here.
- Option B would reject valid solutions (for example swapping val to the end).
- Other problems use the same judge (LC 26, LC 80), so the field will be reused.

## Trade-offs
- The page's stored "output" is the sorted prefix, not the raw array. The page does not show it today.
- Every new judge needs code in three places: call_solution and both drivers.

Depends on: 003, 004 · Affects: 005
Revisit when: a problem needs a judge that is not "sorted first k" (for example "any valid answer").
