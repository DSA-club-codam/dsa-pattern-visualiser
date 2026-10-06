# 011 — Pointer names follow the pattern; colours follow the role

Status: accepted · 2026-10-06

## Context
The prototype pages used names from each problem (write / read, l / r). That made the same idea look different on different pages. We considered start / end for pointers moving towards each other, but chose the names readers meet on LeetCode and in interviews.

## Decision
| Pattern | Names |
|---|---|
| Two pointers towards each other | left / right |
| Sliding window | left / right |
| Same direction, linked list | slow / fast |
| Binary search | lo / mid / hi |
The trailing pointer is always blue (--role-back), the leading one orange (--role-front), mid is --role-mid. Code variables use the same names as the labels.

## Trade-offs
- Two pointers and sliding window share left / right; the picture (window band or not) tells them apart.
- Move Zeroes code now says slow / fast instead of write / read.

Depends on: 002 · Affects: —
Revisit when: club members are confused by the shared left / right names.
