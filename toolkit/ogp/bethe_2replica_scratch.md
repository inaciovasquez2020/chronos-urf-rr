# Scratch: Two-Replica Bethe Functional
## Symbolic Differentiation Target

**Status:** Open — differentiation pending  
**Purpose:** Compute ψ′′(ν₂) to yield κ_Bethe(ρ, Δ)

---

## The Object

The two-replica Bethe functional:

```
Φ_{2-replica}(q)
```

where the overlap parameter is:

```
q = (1/n) Σᵢ σᵢ τᵢ
```

with σ, τ independent replicas drawn under the same Gibbs measure.

---

## Differentiation Target

Curvature is defined by:

```
∂²Φ_{2-replica} / ∂q²  evaluated at q = q*
```

This second derivative is the quantity ψ′′(ν₂) appearing in the OGP hinge module.

---

## What This Unlocks

If curvature is computed explicitly:

```
κ_Bethe(ρ, Δ) := ∂²Φ_{2-replica} / ∂q²  |_{q = q*(ρ,Δ)}
```

Then the LIB barrier immediately yields a quantitative spectral bound:

```
λ₁ ≤ exp( −c(ρ, Δ) · n )
```

This would be the **first fully quantitative LIB barrier result** for local chains under OGP.

---

## Structural Notes

- Φ_{2-replica}(q) is defined on q ∈ [−1, 1] (overlap domain)
- q* is the OGP-relevant saddle point determined by ρ, Δ
- The sign of ψ′′(ν₂) determines whether q* is a local max (OGP holds) or inflection (degenerate case)
- Regularization note: conductance Φ(A) > 0 must be verified away from phase boundary before LIB is applied — see freeze notes

---

## Open

- [ ] Explicit form of Φ_{2-replica}(q) in terms of Bethe free energy
- [ ] Saddle point equation for q*(ρ, Δ)
- [ ] Second derivative computation
- [ ] Sign and magnitude of κ_Bethe(ρ, Δ)
- [ ] Verification against RG closure criterion at η > 0 fixed points

---

## Explicit Bethe Functional

Introduce joint occupation probabilities

p00, p01, p10, p11

with

q = p11

ρ = p10 + p11 = p01 + p11

Vertex term:

F_V = − Σ_{a,b} p_ab log p_ab
      + (p10 + p01 + 2 p11) log λ

Edge term (Bethe approximation):

F_E = log(1 − p11^2)

Two-replica Bethe functional:

Φ₂(q) = F_V + (Δ/2) F_E

*Frozen here. Do not expand until stable modules are confirmed stable under this dependency.*

