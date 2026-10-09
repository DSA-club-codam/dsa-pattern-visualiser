from typing import List  # @hide


class Solution:
    def reverseString(self, s: List[str]) -> None:
        # @trace-begin
        ids = list(range(len(s)))  # identity of each cell, so swaps slide on screen
        n = len(s)

        def show(ch):
            return "' '" if ch == " " else f"'{ch}'"

        def snap(left, right, roles=None, done=False):
            return dict(
                state={"arr": s[:], "ids": ids[:], "left": left, "right": right, "done": done},
                roles=roles or {},
                vars=[
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": right, "role": "front"},
                    {"label": "s[left]", "value": show(s[left]) if 0 <= left < n else "—"},
                    {"label": "s[right]", "value": show(s[right]) if 0 <= right < n else "—"},
                    {"label": "swaps", "value": swaps},
                ],
            )
        swaps = 0
        # @trace-end
        left, right = 0, len(s) - 1  # start at both ends  # @a:init
        T.step("init", "init", f"left = 0 and right = {right}: the first and the last character must trade places.", **snap(left, right))  # @trace
        while left < right:  # @a:loop
            T.op()  # @trace
            T.step("loop", "next", (f"while left < right: {left} < {right}, so the loop runs." if swaps == 0  # @trace
                                    else f"Next round: {left} < {right}, so the loop runs again."), **snap(left, right))  # @trace
            # @trace-begin
            cap = (f"Swap s[{left}] = {show(s[left])} and s[{right}] = {show(s[right])}. "
                   f"Each one is now where it belongs in the reversed string.")
            # @trace-end
            s[left], s[right] = s[right], s[left]  # @a:swap
            ids[left], ids[right] = ids[right], ids[left]  # @trace
            swaps += 1  # @trace
            T.step("swap", "swap", cap, **snap(left, right, {left: "swap", right: "swap"}))  # @trace
            left += 1  # move both inwards  # @a:move
            right -= 1
            T.step("move", "move", f"Both pointers move inwards: left = {left}, right = {right}.", **snap(left, right))  # @trace
        # loop ends: left and right met or crossed  # @a:done
        # @trace-begin
        if n == 1:
            done = "s has one character, so left = right = 0 and the loop does not run. One character is its own reverse."
        elif left == right:
            done = (f"left = right = {left}, so the loop stops. The middle character {show(s[left])} stays where it is. "
                    f"Done after {swaps} {'swap' if swaps == 1 else 'swaps'}: n / 2 rounded down = {n // 2}, with O(1) extra memory.")
        else:
            done = (f"left = {left} is past right = {right}, so the loop stops. Every character has been swapped once. "
                    f"Done after {swaps} {'swap' if swaps == 1 else 'swaps'}: n / 2 = {n // 2}, with O(1) extra memory.")
        T.step("done", "return", done, **snap(left, right, {}, True))
        # @trace-end
