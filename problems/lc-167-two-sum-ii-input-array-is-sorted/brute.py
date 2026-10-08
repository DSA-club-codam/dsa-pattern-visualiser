def brute(numbers, target):
    n = len(numbers)
    for i in range(n):  # every pair (i, j) with i < j
        for j in range(i + 1, n):
            T.op()  # @trace
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]  # the problem counts from 1
    return []  # never reached: there is always exactly one pair
