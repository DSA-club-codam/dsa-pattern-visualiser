def gen(rng):
    """Random input inside the constraints, small enough to compare with brute force."""
    total = rng.randint(1, 12)
    m = rng.randint(0, total)
    n = total - m
    if rng.random() < 0.1:
        pool = [-10**9, 0, 10**9]  # extreme values
    else:
        pool = [-2, 0, 1, 2, 2, 3, 5]  # repeats, negatives and real zeros
    a = sorted(rng.choice(pool) for _ in range(m))
    b = sorted(rng.choice(pool) for _ in range(n))
    return {"nums1": a + [0] * n, "m": m, "nums2": b, "n": n}
