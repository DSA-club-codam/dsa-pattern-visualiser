def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        pool = [1, 9999, 10000]  # extreme values
    else:
        pool = list(range(1, rng.randint(2, 8)))  # few distinct values → many repeats
    return {"nums": [rng.choice(pool) for _ in range(n)]}
