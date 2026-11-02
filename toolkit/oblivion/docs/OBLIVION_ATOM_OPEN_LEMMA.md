# Oblivion Atom (Open Lemma)

Fix k, Δ ∈ ℕ. There exist R = R(k,Δ) and T = T(k,Δ) such that for every finite graph G with max degree ≤ Δ,
if COR_R(G) ≥ T then G is not FO^k_R-homogeneous.

Equivalent formulations to target:
(1) Cycle-support rigidity
(2) Hypergraph-gadget rigidity
(3) FO^k configuration pumping on bounded-degree graphs
(4) Cycle packing ⇒ local type divergence

## Counterexample to the nonvacuous cycle-rank implication (2026-11-02)

**Status: counterexample for every radius R ≥ 1 under the repository's formal definitions.** The displayed existential statement above is **not** a proven rigidity theorem; it also permits the vacuous choice R = 0 unless that case is excluded.

The repository defines COR_R(G) as the F₂-dimension of the span of all cycles contained in radius-R balls and defines FO^k_R-homogeneity as equality of rooted vertex neighborhood types (see `docs/oblivion_atom/formal_definitions.md`).

For every integer n ≥ 7, define G_n on ℤ/nℤ by joining i to i ± 1 and i ± 2 modulo n. Every G_n is 4-regular and vertex-transitive, hence FO^k_R-homogeneous for **all** k and R: rotations carry any root to any other root and induce isomorphisms of their rooted balls.

For each i modulo n, the triangle T_i = (i, i+1, i+2) lies in a radius-1 ball. Its edge {i,i+2} occurs in no other listed T_j (n ≥ 7), so the n triangle vectors are linearly independent over F₂. Consecutive T_i overlap in an edge. It follows that

    COR_R(G_n) ≥ n                    for every R ≥ 1.

Thus for fixed k, Δ = 4, **any positive R** and finite threshold T are defeated by choosing n > max(7,T), despite full rooted-vertex homogeneity. A rank threshold by itself cannot force local logical type diversity.

**Quantifier boundary:** If R = 0 is permitted, ordinary simple-graph radius-0 balls contain no cycles, so COR_0(G) = 0. Choosing T > 0 makes the original existential implication true but vacuous. This example refutes the intended *nonvacuous* assertion, not the literal statement with an unrestricted R = 0.

**Measurement boundary:** COR_R is the full local-cycle-span rank. The existing command-line overlap scanner is a proxy that selects an overlap-connected subset and currently has an unseeded empty selection. Its reported rank is not a substitute for the mathematical definition. The independently verified connected family above is sufficient for the counterexample.

**Restricted CFI observation result (not universal):** A separately checked degree-two parity gadget has even and odd twists with component structures C₁₈ ⊔ C₁₈ and C₃₆, while *unlabeled rooted radius-2 ball-type-only* observations are identical. Its rank-zero factorization applies **only** to that deliberately restricted oracle. It does not establish general CFI indistinguishability under k-WL, FO^k, arbitrary labeled observations, or universal URF rigidity.

**Evidence:** isolated reproducibility script `toolkit/oblivion/proofs/oblivion_bounded_reduction_certificate.py`. The checks are Python experiments and are not a Lean proof of a universal statement. No theorem status should be upgraded.

**Required repair:** either define a genuinely different structural invariant or impose explicit restrictions excluding vertex-transitive families such as these; merely raising T cannot resolve this counterexample.
