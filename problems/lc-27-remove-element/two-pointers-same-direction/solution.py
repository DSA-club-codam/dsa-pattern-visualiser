from typing import List  # @hide


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        # @trace-begin
        n = len(nums)

        def snap(slow, fast, roles=None, flash=False):
            return dict(
                state={"arr": nums[:], "slow": slow, "fast": fast},
                roles=roles or {},
                vars=[
                    {"label": "val", "value": val},
                    {"label": "slow", "value": slow, "role": "back"},
                    {"label": "fast", "value": "—" if fast is None else fast, "role": "front"},
                    {"label": "nums[fast]", "value": "—" if fast is None or fast >= n else nums[fast]},
                    {"label": "kept (k)", "value": slow, "flash": flash},
                    {"label": "nums", "value": "[" + ", ".join(map(str, nums)) + "]"},
                ],
            )
        # @trace-end
        slow = 0  # next slot for a value we keep  # @a:init
        T.step("init", "init", f"slow = 0: the next value we keep goes into slot 0. We remove every {val}.", **snap(0, None))  # @trace
        for fast in range(len(nums)):  # fast reads every element once  # @a:loop
            T.op()  # @trace
            T.step("loop", "next", f"Next round of the for loop: fast moves to index {fast}." if fast else "The for loop starts: fast = 0.", **snap(slow, fast))  # @trace
            if nums[fast] != val:  # keep this value  # @a:check
                T.step("check", "compare", f"nums[{fast}] = {nums[fast]} is not {val}, so we keep it. It goes into slot slow = {slow}.", **snap(slow, fast, {fast: "current"}))  # @trace
                # @trace-begin
                if slow == fast:
                    cap = f"slow and fast both point at index {fast}, so nums[{slow}] = nums[{fast}] copies {nums[fast]} onto itself. Nothing has been removed yet."
                else:
                    why = (f"it held a {val}, which we remove anyway" if nums[slow] == val
                           else f"its old value {nums[slow]} was already copied further left")
                    cap = f"Copy: nums[{slow}] = nums[{fast}] = {nums[fast]}. Overwriting slot {slow} is safe: {why}."
                # @trace-end
                nums[slow] = nums[fast]  # copy it forward  # @a:write
                T.step("write", "write", cap, **snap(slow, fast, {slow: "new"}))  # @trace
                slow += 1  # slot filled, move on  # @a:advance
                T.step("advance", "advance", f"Slot {slow - 1} is filled, so slow moves to {slow}. Values kept: {slow}.", **snap(slow, fast, {}, flash=True))  # @trace
            else:  # @trace
                T.step("check", "skip", f"nums[{fast}] = {val}: skip it. slow stays at {slow}: slot {slow} still waits for the next value we keep.", **snap(slow, fast, {fast: "current removed"}))  # @trace
        # @trace-begin
        if n == 0:
            T.step("loop", "stop", "nums is empty, so the for loop does not run at all.", **snap(slow, None))
        else:
            T.step("loop", "stop", f"fast has reached the end (n = {n}), so the for loop stops.", **snap(slow, n))
        removed = n - slow
        if n == 0:
            done = "Return k = 0. There is nothing to remove in an empty array."
        elif slow == 0:
            done = f"Return k = 0. Every element was {val}, so nothing was kept. The judge ignores the whole array."
        elif removed == 0:
            done = f"Return k = {n}. {val} never appears, so every value was copied onto itself. One pass, no extra array."
        else:
            done = (f"Return k = {slow}. Every value that is not {val} was copied into slots 0..{slow - 1}, "
                    f"and {removed} {'copy' if removed == 1 else 'copies'} of {val} {'was' if removed == 1 else 'were'} skipped. The judge ignores slots from {slow} on. One pass, no extra array.")
        T.step("done", "return", done, **snap(slow, None))
        # @trace-end
        return slow  # k = number of values kept  # @a:done
