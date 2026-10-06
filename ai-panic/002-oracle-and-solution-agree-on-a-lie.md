# The brute force and the clever solution are wrong in exactly the same way

**The fear:** both agree on 200 random inputs, both are wrong, and a page proudly animates a wrong answer.

**How likely:** they are different algorithms, and the brute force is also checked against the LeetCode examples. It would take a remarkable coincidence.

**What we would do:** LeetCode's own judge catches it on submission (ADR 014). Then add the failing input to tests.json and say sorry in the club chat.
