def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    n = rng.randint(0, 12)
    pool = [0, 1, 2, 3, 50]
    nums = [rng.choice(pool) for _ in range(n)]
    if rng.random() < 0.15:
        val = rng.choice([51, 100])  # bigger than any value: nothing to remove
    else:
        val = rng.choice(pool)  # usually appears, often more than once
    return {"nums": nums, "val": val}
