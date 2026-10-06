def brute(nums1, m, nums2, n):
    nums1 = nums1[:]  # work on a copy
    for j in range(n):
        nums1[m + j] = nums2[j]  # fill the empty tail with nums2
    for i in range(1, m + n):  # insertion sort on the whole array
        value = nums1[i]
        k = i - 1
        while k >= 0:
            T.op()  # @trace
            if nums1[k] <= value:  # found where value belongs
                break
            nums1[k + 1] = nums1[k]  # shift the bigger value right
            k -= 1
        nums1[k + 1] = value
    return nums1
