def brute(s):
    n = len(s)
    copy = []  # extra array: O(n) memory
    for i in range(n - 1, -1, -1):  # read s backwards
        T.op()  # @trace
        copy.append(s[i])
    for i in range(n):  # write the copy back into s
        T.op()  # @trace
        s[i] = copy[i]
    return s
