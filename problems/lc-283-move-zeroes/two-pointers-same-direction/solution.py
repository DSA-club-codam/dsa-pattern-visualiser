from typing import List  # @hide


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        # @trace-begin
        ids = list(range(len(nums)))  # identity of each cell, so swaps slide on screen
        n = len(nums)

        def snap(slow, fast, roles=None, flash=False):
            return dict(
                state={"arr": nums[:], "ids": ids[:], "slow": slow, "fast": fast},
                roles=roles or {},
                vars=[
                    {"label": "slow", "value": slow, "role": "back"},
                    {"label": "fast", "value": "—" if fast is None else fast, "role": "front"},
                    {"label": "nums[fast]", "value": "—" if fast is None else nums[fast]},
                    {"label": "non-zeros placed", "value": slow, "flash": flash},
                    {"label": "nums", "value": "[" + ", ".join(map(str, nums)) + "]"},
                ],
            )

        def zeros_text(z):
            return "no zeros" if z == 0 else ("1 zero is" if z == 1 else "%d zeros are" % z)
        # @trace-end
        slow = 0  # next free slot for a non-zero  # @a:init
        T.step("init", "init", "slow = 0: the next non-zero we find goes into slot 0. Nothing has been placed yet.", **snap(0, None))  # @trace
        for fast in range(len(nums)):  # fast visits every element once  # @a:loop
            T.op()  # @trace
            T.step("loop", "next", f"Next round of the for loop: fast moves to index {fast}." if fast else "The for loop starts: fast = 0.", **snap(slow, fast))  # @trace
            if nums[fast] != 0:  # found a non-zero  # @a:check
                T.step("check", "compare", f"nums[{fast}] = {nums[fast]} is not zero, so it belongs in the next free slot, slow = {slow}.", **snap(slow, fast, {fast: "current"}))  # @trace
                # @trace-begin
                if slow == fast:
                    cap = f"slow and fast both point at index {fast}, so the swap changes nothing: {nums[fast]} is already in the right place."
                else:
                    cap = (f"Swap nums[{slow}] = 0 with nums[{fast}] = {nums[fast]}. The {nums[fast]} moves left into slot {slow}; "
                           f"the 0 moves right to index {fast}. The order of the non-zeros does not change.")
                # @trace-end
                nums[slow], nums[fast] = nums[fast], nums[slow]  # send it left  # @a:swap
                ids[slow], ids[fast] = ids[fast], ids[slow]  # @trace
                T.step("swap", "swap", cap, **snap(slow, fast, {slow: "swap", fast: "swap"}))  # @trace
                slow += 1  # slot filled, move on  # @a:advance
                T.step("advance", "advance", f"Slot {slow - 1} is filled, so slow moves to {slow}. Non-zeros placed: {slow}.", **snap(slow, fast, {}, flash=True))  # @trace
            else:  # @trace
                T.step("check", "skip", f"nums[{fast}] = 0. Skip it: slow stays at {slow}, so this zero waits to be swapped out.", **snap(slow, fast, {fast: "current"}))  # @trace
        # loop ends: every zero now sits after the last non-zero  # @a:done
        # @trace-begin
        if slow == 0:
            done = f"Done: {nums}. There are no non-zeros, so nothing moved. One pass, no extra array."
        elif slow == n:
            done = f"Done: {nums}. Every element is non-zero, so each one was swapped with itself and stayed in place. One pass, no extra array."
        else:
            done = (f"Done: {nums}. Every non-zero was swapped into slots 0..{slow - 1} in the order fast met it, "
                    f"so the order is kept, and {zeros_text(n - slow)} left at the end. One pass, no extra array.")
        T.step("done", "return", done, **snap(slow, None))
        # @trace-end
