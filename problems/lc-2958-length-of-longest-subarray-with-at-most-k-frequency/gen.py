def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        pool = [1, 10**9, 999999999]  # extreme values
    else:
        pool = list(range(1, rng.randint(2, 5)))  # few distinct values → many repeats
    nums = [rng.choice(pool) for _ in range(n)]
    return {"nums": nums, "k": rng.randint(1, n)}
