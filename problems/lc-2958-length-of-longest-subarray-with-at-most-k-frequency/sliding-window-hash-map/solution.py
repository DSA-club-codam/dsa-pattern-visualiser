from collections import defaultdict  # @hide
from typing import List  # @hide


class Solution:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        count = defaultdict(int)  # value -> times it is in the window  # @a:init
        left = 0  # left edge of the window
        longest = 0  # length of the longest good window so far
        # @trace-begin
        order = list(dict.fromkeys(nums))  # map rows in order of first appearance
        best_win = None
        length = None  # only exists after it is computed in this round, as in C++

        def snap(right, window, roles=None, over=None, flash=False):
            return dict(
                state={"arr": nums[:], "k": k, "left": left, "right": right, "window": window,
                       "rows": [{"key": v, "count": count.get(v, 0)} for v in order],
                       "over": over, "length": length, "longest": longest, "bestWindow": best_win},
                roles=roles or {},
                vars=[
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "length", "value": "—" if length is None else length},
                    {"label": "longest", "value": longest, "flash": flash},
                ],
            )

        T.step("init", "init", f"count is empty, left = 0, longest = 0. k = {k}: no value may appear more than {k} "
               f"time{'s' if k != 1 else ''} in the window.", **snap(None, None))
        # @trace-end
        for right in range(len(nums)):  # right edge, moves every step  # @a:loop
            length = None  # @trace
            T.step("loop", "next", f"Next round of the for loop: right moves to index {right}." if right else "The for loop starts: right = 0.", **snap(right, [left, right - 1] if right > left else None))  # @trace
            count[nums[right]] += 1  # add nums[right] to the window  # @a:expand
            T.op()  # @trace
            # @trace-begin
            v = nums[right]
            if count[v] > k:
                T.step("expand", "expand", f"right = {right}: add {v}. count[{v}] is now {count[v]} > k = {k}, "
                       "so the window is no longer good.",
                       **snap(right, [left, right], {right: "conflict"}, over=v))
            else:
                T.step("expand", "expand", f"right = {right}: add {v}. count[{v}] = {count[v]} ≤ k = {k}, "
                       f"so the window [{left}, {right}] is still good.", **snap(right, [left, right], {right: "current"}))
            # @trace-end
            while count[nums[right]] > k:  # only nums[right] can be over the limit  # @a:while
                T.step("while", "check", f"while count[{nums[right]}] = {count[nums[right]]} > k = {k}: the loop runs, so the window shrinks from the left.", **snap(right, [left, right], over=nums[right]))  # @trace
                count[nums[left]] -= 1  # drop nums[left] from the window  # @a:shrink
                left += 1
                # @trace-begin
                T.op()
                d, v = nums[left - 1], nums[right]
                if count[v] > k:
                    T.step("shrink", "shrink", f"Drop nums[{left - 1}] = {d}, left moves to {left}. It is not a {v}, "
                           f"so count[{v}] is still {count[v]} > k.",
                           **snap(right, [left, right], {left - 1: "removed"}, over=v))
                else:
                    T.step("shrink", "shrink", f"Drop nums[{left - 1}] = {d}, left moves to {left}. count[{v}] = {count[v]} ≤ k, "
                           f"so the window [{left}, {right}] is good again and the while loop stops.", **snap(right, [left, right], {left - 1: "removed"}))
                # @trace-end
            old = longest  # @trace
            length = right - left + 1  # length of the good window [left, right]
            longest = max(longest, length)  # keep the longest  # @a:update
            # @trace-begin
            if longest > old:
                best_win = [left, right]
                T.step("update", "update", f"Window [{left}, {right}] has length {right - left + 1} > old longest, so longest = {longest}.",
                       **snap(right, [left, right], flash=True))
            else:
                T.step("update", "compare", f"Window [{left}, {right}] has length {right - left + 1}, not longer than longest = {longest}. "
                       "longest stays.", **snap(right, [left, right]))
            # @trace-end
        # @trace-begin
        length = None  # out of scope after the loop, as in C++
        T.step("return", "return", f"Return longest = {longest}, the window [{best_win[0]}, {best_win[1]}]. Every good window was checked "
               "at its right end, and left only moved right when it had to, so no longer good window was missed.",
               **snap(None, None))
        # @trace-end
        return longest  # @a:return
