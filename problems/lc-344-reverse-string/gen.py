def gen(rng):
    """Random printable ASCII characters, including the ones that need escaping."""
    pool = "abcXYZ019 ,.!\"\\'"
    n = rng.randint(1, 14)
    return {"s": [rng.choice(pool) for _ in range(n)]}
