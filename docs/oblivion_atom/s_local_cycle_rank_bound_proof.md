# s-Local Cycle Rank Bound (Proof Skeleton)

Let G have max degree ≤ Δ.

Let s := O(Δ^R).

Define L_s(G) := span of all cycles contained in some B_R(v).

Claim:

dim L_s(G) ≤ O(Δ^(2R)).

Skeleton:

1. Each B_R(v) has at most B := 1+Δ+...+Δ^R vertices and at most O(Δ^R) edges.
2. Thus dim Z_1(B_R(v)) ≤ O(Δ^R).
3. Consider the cover of E(G) by ball-edges E(B_R(v)).
4. Choose a maximal set of vertices V0 such that B_{R-1}(v) are disjoint.
   Then |V0| ≤ O(|V|/Δ^(R-1)).
5. Any s-local cycle is supported in the union of O(1) balls centered near some v∈V0.
6. Therefore the total independent contribution is bounded by |V0|·O(Δ^R) = O(|V|·Δ).
7. Under FO^k_R-homogeneity, only T(k,B) distinct cycle-support patterns exist, collapsing the bound to O(1).
