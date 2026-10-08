def brute(nums, val):
    nums = nums[:]  # work on a copy
    n = len(nums)  # length of the part that still counts
    i = 0
    while i < n:
        T.op()  # @trace
        if nums[i] == val:  # found val: close the hole
            for j in range(i + 1, n):  # shift everything after it one step left
                T.op()  # @trace
                nums[j - 1] = nums[j]
            n -= 1  # one element fewer; check index i again, a new value is there now
        else:
            i += 1
    return sorted(nums[:n])  # the judge sorts the first k elements, so we do too
