# TODO: Formal Closure Checklist (Oblivion → Chronos)

## A. Combinatorial bound: independent s-local cycles

Target:
FO^k_R-homogeneous(G) ⇒ dim span{s-local cycles} ≤ C(k,Δ,R)

Deliverables:
1. Precise definition of s-local cycles as edge-sets in Z_1(G;F2).
2. Cover/packing lemma on R-balls in bounded-degree graphs.
3. Overlap-induced dependency lemma with explicit rank bound.

## B. Explicit constant C(k,Δ,R)

Target:
C(k,Δ,R) computed from:
- ball size bound B(Δ,R)
- cycle space bound on the template ball
- FO^k_R type count bound T(k,B)

Deliverables:
1. Formal bound B(Δ,R) = 1+Δ+…+Δ^R.
2. Template cycle basis size ≤ E(B*)−V(B*)+1 ≤ O(Δ^R).
3. Type-count bound: |Types_{k,R}| ≤ T(k,B).

## C. Random lifts / expanders achieve COR_R(G)=Ω(n)

Target:
For base cyclic H, random n-lift G_n satisfies COR_R(G_n) ≥ c(H,R)·n w.h.p.

Deliverables:
1. Define a concrete family of lifted cycles from a base cycle in H.
2. Show Ω(n) of these cycles are independent in Im(Φ_R).
3. Provide experiment corroboration with scripts.

## D. EF Spoiler ⇒ explicit FO^k formula

Target:
Given a Spoiler win on (G,u),(G,v) in k-pebble r-local game,
produce φ(x) ∈ FO^k_R with G ⊨ φ(u) and G ⊭ φ(v).

Deliverables:
1. Encode bounded-length cycle detection within radius R.
2. Define cycle-signature predicate as FO^k conjunction/disjunction of bounded witnesses.
3. Extract φ(x) from the winning strategy tree.

## E. Lean formalization

Targets:
1. radiusBall / dist: use Mathlib graph distance (Finite graph setting).
2. cycle model: represent cycles as edge-sets (Finset (Sym2 V)) with even-degree constraint.
3. Z_1 space: F2-vector space structure for edge-sets modulo boundaries.
4. COR_R: dim of span of images of local cycle spaces.
5. signature bound: finiteness + cardinality bounds.

