def brute(nums, k):
    best = 0
    for i in range(len(nums)):  # every possible start
        count = {}  # fresh counts for each start
        for j in range(i, len(nums)):  # extend to the right
            T.op()  # @trace
            count[nums[j]] = count.get(nums[j], 0) + 1
            if count[nums[j]] > k:  # this value is now over the limit
                break
            best = max(best, j - i + 1)  # nums[i..j] is good
    return best
