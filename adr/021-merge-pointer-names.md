# 021 — Pointer names for merging two arrays

Status: accepted · 2026-10-06

## Context
LC 88 Merge Sorted Array needs three pointers: one reads nums1, one reads nums2, and one writes into nums1. ADR 011 has no names for this case.

## Options we discussed
- **p1 / p2 / write** — p1 and p2 as in the LeetCode editorial; write says what the third pointer does
- **i / j / k** — short and common in tutorials, but the names do not say who reads and who writes
- **read1 / read2 / write** — most explicit, but longer and not what readers see on LeetCode

## Decision
Merging two arrays uses p1 / p2 / write. write uses --role-back, like slow in Move Zeroes: it is the writer. p1 and p2 use --role-front, like fast: they are the readers. They sit in different rows, so the labels tell them apart. This extends the table in ADR 011:

| Pattern | Names |
|---|---|
| Two pointers on two arrays (merge) | p1 / p2 / write |

## Why
- Readers who check the LeetCode editorial see the same names.
- The colours keep one meaning across pages: blue writes, orange reads.
- When merging from the end, write trails behind p1, so "trailing pointer = blue" from ADR 011 still holds.

## Trade-offs
- Two pointers share the orange role on one canvas. Only the label and the row tell p1 and p2 apart.

Depends on: 011 · Affects: —
Revisit when: a merge of three or more arrays (or a linked-list merge such as LC 21) needs names that p1 / p2 do not cover.
