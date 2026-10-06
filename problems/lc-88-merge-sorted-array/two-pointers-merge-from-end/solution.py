from typing import List  # @hide


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        # @trace-begin
        last = m + n - 1

        def show(v):
            return "[" + ", ".join(map(str, v)) + "]"

        def snap(p1, p2, write, placed, r1=None, r2=None, flash=False):
            return dict(
                state={"arr1": nums1[:], "arr2": nums2[:], "m": m, "p1": p1, "p2": p2, "write": write,
                       "placed": placed, "r1": r1 or {}, "r2": r2 or {}},
                vars=[
                    {"label": "write", "value": write, "role": "back"},
                    {"label": "p1", "value": p1, "role": "front"},
                    {"label": "p2", "value": p2, "role": "front"},
                    {"label": "nums1[p1]", "value": nums1[p1] if p1 >= 0 else "—"},
                    {"label": "nums2[p2]", "value": nums2[p2] if p2 >= 0 else "—"},
                    {"label": "slots placed", "value": last - placed + 1 if placed <= last else 0, "flash": flash},
                    {"label": "nums1", "value": show(nums1)},
                ],
            )

        def slots(a, b):
            return "slot %d is" % a if a == b else "slots %d..%d are" % (a, b)

        if m == 0:
            start = "p1 = -1: nums1 has no real values, only placeholders. "
        else:
            start = f"p1 = {m - 1}: the last real value of nums1. "
        if n == 0:
            start += "p2 = -1: nums2 is empty. "
        else:
            start += f"p2 = {n - 1}: the last value of nums2. "
        start += f"write = {last}: the last slot. The free slots are at the back, so we fill nums1 from the back."
        # @trace-end
        p1 = m - 1  # last real value in nums1  # @a:init
        p2 = n - 1  # last value in nums2
        write = m + n - 1  # last slot of nums1: fill from the back
        T.step("init", "init", start, **snap(p1, p2, write, last + 1))  # @trace
        while p2 >= 0:  # nums2 still has values to place  # @a:loop
            T.op()  # @trace
            T.step("loop", "next", (f"Next round: p2 = {p2} ≥ 0, so nums2 still has {p2 + 1} value{'' if p2 == 0 else 's'} to place." if write < last else f"The while loop starts: p2 = {p2} ≥ 0, so nums2 has values to place."), **snap(p1, p2, write, write + 1))  # @trace
            if p1 >= 0 and nums1[p1] > nums2[p2]:  # the larger value is in nums1  # @a:compare
                a = nums1[p1]  # @trace
                T.step("compare", "compare", f"nums1[p1] = {a} > nums2[p2] = {nums2[p2]}: {a} is the largest value left, so it goes into slot write = {write}.", **snap(p1, p2, write, write + 1, {p1: "current"}))  # @trace
                nums1[write] = nums1[p1]  # move it to the back  # @a:take1
                T.step("take1", "take", f"nums1[{write}] = {a}. Slot {write} is final. Once p1 moves left, slot {p1} is free: its old {a} will be overwritten later.", **snap(p1, p2, write, write, {write: "new"}, flash=True))  # @trace
                p1 -= 1
            else:
                # @trace-begin
                b = nums2[p2]
                if p1 < 0:
                    cap = f"p1 = -1: nums1 has no values left, so the next value always comes from nums2. Take nums2[p2] = {b} for slot write = {write}."
                elif nums1[p1] == b:
                    cap = f"nums1[p1] = {nums1[p1]} is not larger than nums2[p2] = {b}, so take {b} from nums2. They are equal, so either choice gives a sorted result."
                else:
                    cap = f"nums1[p1] = {nums1[p1]} < nums2[p2] = {b}: {b} is the largest value left, so it goes into slot write = {write}."
                T.step("compare", "compare", cap, **snap(p1, p2, write, write + 1, {}, {p2: "current"}))
                # @trace-end
                nums1[write] = nums2[p2]  # the larger value is in nums2, or nums1 is used up  # @a:take2
                T.step("take2", "take", f"nums1[{write}] = {b}, copied from nums2[{p2}]. Slot {write} is final.", **snap(p1, p2, write, write, {write: "new"}, flash=True))  # @trace
                p2 -= 1
            write -= 1  # @a:advance
            T.step("advance", "advance", f"p1 = {p1}, p2 = {p2}, and write moves to {write}. {slots(write + 1, last).capitalize()} final.", **snap(p1, p2, write, write + 1))  # @trace
        # @trace-begin
        if n == 0:
            stop = "p2 = -1 from the start: nums2 is empty, so the while loop never runs."
        else:
            stop = "p2 = -1: every value of nums2 is placed, so the while loop stops."
        if p1 >= 0:
            stop += f" nums1[0..{p1}] were never moved: they are the smallest values, already sorted and in the right place."
        T.step("loop", "stop", stop, **snap(p1, p2, write, write + 1))
        # @trace-end
        # p2 < 0: nums1[0..p1] were already in place  # @a:done
        # @trace-begin
        T.step("done", "return", f"Done: nums1 = {show(nums1)}. Each slot from the back got the largest value left, so the result is sorted. "
               "write = p1 + p2 + 1 always sits to the right of p1, so no value in nums1 was overwritten before it was copied. One pass, no extra array.",
               **snap(p1, p2, write, 0))
        # @trace-end
