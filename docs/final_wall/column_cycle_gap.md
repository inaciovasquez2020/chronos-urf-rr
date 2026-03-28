# Remaining irreducible gap

Need to prove:
isOverlapCycle(A, γ) -> forall j, Even (sum_{i in γ} 1_{A i j != 0})

Current definitions only encode overlap connectivity, not per-column parity balance.

Required new ingredient:
A constructive overlap-cycle generator whose row incidences are column-balanced by design.
