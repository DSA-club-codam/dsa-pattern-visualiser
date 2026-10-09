def gen(rng):
    """Random printable ASCII string; about half are palindromes after cleaning."""
    alnum = "abcAB019"
    other = " ,.:!'?-"
    n = rng.randint(1, 14)
    if rng.random() < 0.5:
        half = [rng.choice(alnum) for _ in range(n // 2)]
        mid = [rng.choice(alnum)] if n % 2 else []
        core = half + mid + half[::-1]
        core = [ch.upper() if rng.random() < 0.3 else ch for ch in core]  # mixed case must still match
        out = []
        for ch in core:  # sprinkle punctuation and spaces in between
            if rng.random() < 0.3:
                out.append(rng.choice(other))
            out.append(ch)
        s = "".join(out)[:14] or "a"
    else:
        s = "".join(rng.choice(alnum + other) for _ in range(n))
    return {"s": s}
