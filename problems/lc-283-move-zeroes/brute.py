def brute(nums):
    nums = nums[:]  # work on a copy
    n = len(nums)
    for i in range(n):  # n passes, like bubble sort
        for j in range(n - 1 - i):
            T.op()  # @trace
            if nums[j] == 0 and nums[j + 1] != 0:  # a zero sits before a non-zero
                nums[j], nums[j + 1] = nums[j + 1], nums[j]  # move the non-zero one step left
    return nums
