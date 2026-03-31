def spectral_gap(Q, samples):
    return min((x @ (Q @ x)) for x in samples if (x @ x) == 1)

def certificate(Q, samples):
    lam = spectral_gap(Q, samples)
    return {"lambda1": lam, "valid": lam > 0}
