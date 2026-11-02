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

## Bounded linear rank-width separation (2026-11-02)

**Independent of the overlap scanner and its selected-cycle proxy.** Define the graph family `G_n` for every `n ≥ 7` exactly as above, and use the vertex order `0,1,...,n-1`.

For every prefix `S_t = {0,...,t-1}`, the only vertices in `S_t` that can have neighbors in its complement belong to `{0,1,t-2,t-1} ∩ S_t`: an edge connects only cyclic offsets one and two. Thus the binary adjacency submatrix across any prefix cut has at most four nonzero rows, and its rank over F₂ is at most four. Therefore the **linear rank-width** satisfies `lrw(G_n) ≤ 4` and hence `rw(G_n) ≤ 4` for all `n ≥ 7`.

Separately, each triangle `(i,i+1,i+2)` is contained in a radius-one ball, and the `n` triangle vectors are F₂-independent by their distinct length-two edges. Hence `COR_R(G_n) ≥ n` for all `R ≥ 1`. Rotations preserve the graph and send any vertex to any other, so all rooted neighborhoods are isomorphic and the graph is FO^k_R-homogeneous for every `k,R`.

**Separation:** arbitrary growth in the repository-defined local-cycle-span rank can coexist with bounded linear rank-width and complete rooted-vertex homogeneity. It does **not** follow that high COR rank forces FO^k_R type diversity; this conclusion holds without invoking the overlap scanner, a WL implementation, or an unproved CFI correspondence.

**Independent finite sanity check:** direct F₂ elimination on triangle edge vectors and prefix-cut adjacency rows at `n = 7,8,10,16,32,64` produced triangle ranks `7,8,10,16,32,64` and maximum prefix cut-ranks `3,4,4,4,4,4`, respectively. These finite checks support—but do not replace—the general combinatorial argument.

**Scope:** This graph-theoretic separation neither proves a universal URF rigidity statement nor addresses the independent Chronos GfE quadratic-action and spectral-closure obligations.
