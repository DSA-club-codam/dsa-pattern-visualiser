def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(1, 12)
    if rng.random() < 0.1:
        pool = [0, -2147483648, 2147483647]  # extreme values
    else:
        pool = [0, 0, 0, 1, 2, 3, -1, 12]  # many zeros, some negatives
    return {"nums": [rng.choice(pool) for _ in range(n)]}
