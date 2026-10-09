class Solution:
    def isPalindrome(self, s: str) -> bool:
        # @trace-begin
        n = len(s)
        matched = []  # positions already compared and equal

        def show(ch):
            return "' '" if ch == " " else f"'{ch}'"

        def snap(left, right, roles=None, done=False):
            return dict(
                state={"arr": list(s), "left": left, "right": right, "matched": matched[:], "done": done},
                roles=roles or {},
                vars=[
                    {"label": "left", "value": left, "role": "back"},
                    {"label": "right", "value": right, "role": "front"},
                    {"label": "s[left]", "value": show(s[left]) if 0 <= left < n else "—"},
                    {"label": "s[right]", "value": show(s[right]) if 0 <= right < n else "—"},
                    {"label": "pairs matched", "value": pairs},
                ],
            )
        rounds = 0
        pairs = 0
        # @trace-end
        left, right = 0, len(s) - 1  # start at both ends  # @a:init
        T.step("init", "init", f"left = 0 and right = {right}: compare the string from both ends at once.", **snap(left, right))  # @trace
        while left < right:  # @a:loop
            # @trace-begin
            rounds += 1
            T.step("loop", "next", (f"while left < right: {left} < {right}, so the loop runs." if rounds == 1
                                    else f"Next round: {left} < {right}, so the loop runs again."), **snap(left, right))
            # @trace-end
            while left < right and not s[left].isalnum():  # skip what does not count  # @a:skipLeftLoop
                T.op()  # @trace
                left += 1  # @a:skipLeft
                T.step("skipLeft", "skip", f"s[{left - 1}] = {show(s[left - 1])} is not a letter or digit, so it does not count. left moves to {left}.", **snap(left, right))  # @trace
            while left < right and not s[right].isalnum():  # @a:skipRightLoop
                T.op()  # @trace
                right -= 1  # @a:skipRight
                T.step("skipRight", "skip", f"s[{right + 1}] = {show(s[right + 1])} is not a letter or digit, so it does not count. right moves to {right}.", **snap(left, right))  # @trace
            T.op()  # @trace
            if s[left].lower() != s[right].lower():  # compare, ignoring case  # @a:compare
                # @trace-begin
                T.step("mismatch", "mismatch", (f"s[{left}] = {show(s[left])} and s[{right}] = {show(s[right])} are different, even in lowercase. "
                                                "A palindrome needs them equal, so the answer is false. No need to look further."),
                       **snap(left, right, {left: "conflict", right: "conflict"}, True))
                # @trace-end
                return False  # @a:mismatch
            # @trace-begin
            if left == right:
                if s[left].isalnum():
                    matched.append(left)
                    cap = f"left and right meet at index {left}: the middle character {show(s[left])} has no partner, and it always equals itself."
                else:
                    cap = (f"left and right meet at index {left} on {show(s[left])}. It is not a letter or digit, "
                           "but a single character always equals itself, so the check passes.")
            else:
                same = "the same" if s[left] == s[right] else "the same in lowercase"
                cap = f"s[{left}] = {show(s[left])} and s[{right}] = {show(s[right])} are {same}. This pair matches."
                matched += [left, right]
                pairs += 1
            T.step("compare", "compare", cap, **snap(left, right))
            # @trace-end
            left += 1  # move both inwards  # @a:move
            right -= 1
            T.step("move", "move", f"Both pointers move inwards: left = {left}, right = {right}.", **snap(left, right))  # @trace
        # @trace-begin
        if rounds == 0:
            stop = f"s has one character, so left = right = 0 and the while loop does not run."
        elif left == right:
            stop = f"left = right = {left}, so the loop stops."
        else:
            stop = f"left = {left} is past right = {right}, so the loop stops."
        if not any(ch.isalnum() for ch in s):
            why = "There are no letters or digits, and an empty string reads the same both ways."
        elif pairs == 0:
            why = "There is only one letter or digit, and it reads the same both ways."
        else:
            why = f"All {pairs} {'pair' if pairs == 1 else 'pairs'} matched, so s reads the same forward and backward."
        done = f"{stop} Return true. {why}"
        T.step("done", "return", done, **snap(left, right, {}, True))
        # @trace-end
        return True  # every pair matched  # @a:done
