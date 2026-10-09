def brute(s):
    cleaned = []  # extra copy: O(n) space
    for ch in s:
        T.op()  # @trace
        if ch.isalnum():  # keep letters and digits only
            cleaned.append(ch.lower())
    return cleaned == cleaned[::-1]  # same forward and backward?
