from typing import List  # @hide


class Solution:
    def maximumUniqueSubarray(self, nums: List[int]) -> int:
        count = [0] * 10001  # value -> times it is in the window (values are 1..10^4)  # @a:init
        left = 0  # left edge of the window
        total = 0  # sum of the window nums[left..right]
        largest = 0  # largest window sum so far
        # @trace-begin
        order = list(dict.fromkeys(nums))  # map rows in order of first appearance
        best_win = None

        def snap(right, window, roles=None, dup=None, flash=False):
            return dict(
                state={"arr": nums[:], "left": left, "right": right, "window": window, "total": total,
                       "rows": [{"key": v, "count": count[v]} for v in order],
                       "dup": dup, "largest": largest, "bestWindow": best_win},
                roles=roles or {},
                vars=[
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": "—" if right is None else right, "role": "front"},
                    {"label": "total", "value": "—" if window is None else total},
                    {"label": "largest", "value": largest, "flash": flash},
                ],
            )

        T.step("init", "init", "count is all zeros, left = 0, total = 0, largest = 0. Rule: no value may appear twice in the window.", **snap(None, None))
        # @trace-end
        for right in range(len(nums)):  # right edge, moves every step  # @a:loop
            T.step("loop", "next", f"Next round of the for loop: right moves to index {right}." if right else "The for loop starts: right = 0.", **snap(right, [left, right - 1] if right > left else None))  # @trace
            count[nums[right]] += 1  # add nums[right] to the window  # @a:expand
            total += nums[right]
            T.op()  # @trace
            # @trace-begin
            v = nums[right]
            if count[v] > 1:
                T.step("expand", "expand", f"right = {right}: add {v}, total = {total}. count[{v}] is now 2, "
                       f"so {v} appears twice and the window is no longer unique.",
                       **snap(right, [left, right], {right: "conflict"}, dup=v))
            else:
                T.step("expand", "expand", f"right = {right}: add {v}, total = {total}. count[{v}] = 1, "
                       f"so the window [{left}, {right}] is still unique.", **snap(right, [left, right], {right: "current"}))
            # @trace-end
            while count[nums[right]] > 1:  # only nums[right] can be a repeat  # @a:while
                T.step("while", "check", f"while count[{nums[right]}] = 2 > 1: the loop runs, so the window shrinks from the left until the old {nums[right]} is gone.", **snap(right, [left, right], dup=nums[right]))  # @trace
                count[nums[left]] -= 1  # drop nums[left] from the window  # @a:shrink
                total -= nums[left]
                left += 1
                # @trace-begin
                T.op()
                d, v = nums[left - 1], nums[right]
                if count[v] > 1:
                    T.step("shrink", "shrink", f"Drop nums[{left - 1}] = {d}, total = {total}, left moves to {left}. "
                           f"It is not a {v}, so {v} still appears twice.",
                           **snap(right, [left, right], {left - 1: "removed"}, dup=v))
                else:
                    T.step("shrink", "shrink", f"Drop nums[{left - 1}] = {d}, total = {total}, left moves to {left}. "
                           f"That was the old {v}, so the window [{left}, {right}] is unique again and the while loop stops.",
                           **snap(right, [left, right], {left - 1: "removed"}))
                # @trace-end
            old = largest  # @trace
            largest = max(largest, total)  # unique window: keep the largest sum  # @a:update
            # @trace-begin
            if largest > old:
                best_win = [left, right]
                T.step("update", "update", f"Window [{left}, {right}] has total {total} > old largest {old}, so largest = {largest}.",
                       **snap(right, [left, right], flash=True))
            else:
                T.step("update", "compare", f"Window [{left}, {right}] has total {total}, not more than largest = {largest}. "
                       "largest stays.", **snap(right, [left, right]))
            # @trace-end
        # @trace-begin
        T.step("return", "return", f"Return largest = {largest}, the window [{best_win[0]}, {best_win[1]}]. Every unique window was checked "
               "at its right end, and left only moved right when a repeat forced it, so no unique window with a bigger sum was missed.",
               **snap(None, None))
        # @trace-end
        return largest  # @a:return
