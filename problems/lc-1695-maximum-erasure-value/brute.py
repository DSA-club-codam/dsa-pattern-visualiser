def brute(nums):
    best = 0
    for i in range(len(nums)):  # every possible start
        seen = set()  # fresh set for each start
        total = 0
        for j in range(i, len(nums)):  # extend to the right
            T.op()  # @trace
            if nums[j] in seen:  # a repeat: no longer unique
                break
            seen.add(nums[j])
            total += nums[j]
            best = max(best, total)  # nums[i..j] is unique
    return best
