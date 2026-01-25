def permutation_p_value(D: np.ndarray, trials: int = 1000) -> float:
    C = covariance(D)
    s = np.linalg.svd(C, compute_uv=False)
    stat = s[1] if s.size > 1 else 0.0

    count = 0
    for _ in range(trials):
        P = np.random.permutation(D)
        Cp = covariance(P)
        sp = np.linalg.svd(Cp, compute_uv=False)
        stat_p = sp[1] if sp.size > 1 else 0.0
        if stat_p <= stat:
            count += 1
    return count / trials

