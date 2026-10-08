def gen(rng):
    """Random sorted input with exactly one pair that adds up to target."""
    while True:
        n = rng.randint(2, 12)
        if rng.random() < 0.1:
            pool = [-1000, -999, 0, 999, 1000]  # extreme values
        else:
            pool = list(range(-6, 16))
        numbers = sorted(rng.choice(pool) for _ in range(n))  # repeats are likely
        i, j = sorted(rng.sample(range(n), 2))
        target = numbers[i] + numbers[j]
        if not -1000 <= target <= 1000:
            continue
        count = sum(1 for a in range(n) for b in range(a + 1, n) if numbers[a] + numbers[b] == target)
        if count == 1:  # the statement promises exactly one solution
            return {"numbers": numbers, "target": target}
