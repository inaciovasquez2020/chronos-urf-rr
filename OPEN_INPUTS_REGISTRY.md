# Open Inputs Registry
**Repository Status: CONDITIONAL**

This file is the single authoritative registry of theorem-level inputs that must be proved before the non-factorization conclusion can be discharged.

Assembly surfaces and dependency routing are complete. Theorem-level closure is not complete. Only the three items below remain as terminal mathematical inputs.

---

## (R1) Long-Chord Exclusion Lemma
**Status: OPEN**

```text
∀ i ∈ {1,2},  ∀ w ∈ W^triv,    e_i ∉ supp(w)
Role: Excludes both long-chord edges from every trivial witness word.
Sub-steps:
(R1a) For every trivial 2-face (\tau \in \Phi_2^{\mathrm{triv}}), neither long chord occurs in (\partial \tau).
(R1b) Linear combinations of trivial face boundaries cannot create either long chord by cancellation.
(R1c) The maximal-separation geometry forbids any trivial witness boundary from traversing a diameter-spanning long chord.
Downstream:
(R1) ⟹ dim(W^tw / W^triv) = 2
## (R2) Diameter-Separation Filling Obstruction
**Status: OPEN**
u ≠ v,  ∂S = c_u − c_v   ⟹   diam(supp S) > L
Role: Forces distinct nonzero fiber classes to remain globally separated.
Sub-steps:
(R2a) Every (L)-bounded filling localizes to a single rooted region.
(R2b) Supports near distinct fibers cannot be joined by an (L)-bounded 2-chain.
(R2c) Any (L)-bounded filling of (c_u-c_v) would force a forbidden identification of distinct local twisted classes.
(R2d) Geometric separation implies algebraic injectivity of the fiber-to-global map.
Downstream:
(R2) ⟹ cross-fiber injectivity
(R2) + (R1) + sigma-package assembly ⟹ dim(Z₁ / W^glob) ≥ 2|U|
## (R3) Uniform Local-Type Capacity Lemma
**Status: OPEN**
Q factors through bounded (r,k,Δ)-local type
  ⟹  dim_{F₂}(Z₁ / W^glob) ≤ C(r,k,Δ)
Role: Supplies the bounded-capacity side of the final contradiction.
Sub-steps:
(R3a) Model bounded local-type factorization by a finite local state space.
(R3b) Prove that factorization through that finite state space yields uniformly bounded image dimension.
(R3c) Bridge equality of local type data to equality of quotient data.
(R3d) Extract the uniform dimension bound (\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})\le C(r,k,\Delta)).
Downstream:
(R3) + (dim(Z₁/W^glob) ≥ 2|U|) + (|U| → ∞) ⟹ non-factorization
Closure Dependency (read-only)
(R1) ──► dim(W^tw/W^triv) = 2
(R2) ──► cross-fiber injectivity
(R2) + (R1) + sigma-package assembly ──► dim(Z₁/W^glob) ≥ 2|U|
(R3) + (dim(Z₁/W^glob) ≥ 2|U|) + (|U| → ∞) ──► NON-FACTORIZATION
Assembly surfaces are organized.
Theorem-level closure remains blocked exactly at (R1), (R2), (R3).
Last audited: see AUDIT_TEST.py
