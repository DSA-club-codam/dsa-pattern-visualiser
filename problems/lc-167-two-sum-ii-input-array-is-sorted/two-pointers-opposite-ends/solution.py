from typing import List  # @hide


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        # @trace-begin
        def snap(left, right, total=None, found=False):
            return dict(
                state={"arr": numbers[:], "left": left, "right": right, "found": found},
                vars=[
                    {"label": "target", "value": target},
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": right, "role": "front"},
                    {"label": "numbers[left]", "value": numbers[left]},
                    {"label": "numbers[right]", "value": numbers[right]},
                    {"label": "total", "value": "—" if total is None else total, "flash": found},
                ],
            )
        rounds = 0
        # @trace-end
        left, right = 0, len(numbers) - 1  # start at both ends  # @a:init
        T.step("init", "init", f"left = 0 and right = {right}: start with the smallest and the largest value. Every pair is still possible.", **snap(left, right))  # @trace
        while left < right:  # @a:loop
            T.op()  # @trace
            # @trace-begin
            rounds += 1
            T.step("loop", "next", (f"while left < right: {left} < {right}, so the loop runs." if rounds == 1
                                    else f"Next round: {left} < {right}, so the loop runs again."), **snap(left, right))
            # @trace-end
            total = numbers[left] + numbers[right]  # @a:sum
            # @trace-begin
            if total == target:
                rel = "equal to"
            else:
                rel = "smaller than" if total < target else "bigger than"
            T.step("sum", "compare", f"total = numbers[{left}] + numbers[{right}] = {numbers[left]} + {numbers[right]} = {total}, {rel} target {target}.",
                   **snap(left, right, total))
            # @trace-end
            if total == target:  # found the pair  # @a:check
                T.step("found", "return", (f"total = target, so return [left + 1, right + 1] = [{left + 1}, {right + 1}] (the problem counts from 1). "  # @trace
                                           "Every value we dropped could not be in any pair, so the one answer was never skipped."), **snap(left, right, total, True))  # @trace
                return [left + 1, right + 1]  # 1-indexed  # @a:found
            if total < target:  # too small: need a bigger left value  # @a:small
                left += 1  # @a:left
                T.step("left", "left", (f"{numbers[left - 1]} is too small even with the largest value left, {numbers[right]}, "  # @trace
                                        f"so it cannot be in any pair. Drop it: left moves to {left}."), **snap(left, right, total))  # @trace
            else:  # too big: need a smaller right value
                right -= 1  # @a:right
                T.step("right", "right", (f"{numbers[right + 1]} is too big even with the smallest value left, {numbers[left]}, "  # @trace
                                          f"so it cannot be in any pair. Drop it: right moves to {right}."), **snap(left, right, total))  # @trace
        return []  # never reached: there is always exactly one pair
