# Cycle–Overlap Rank Rigidity

## Definition (Bounded-Radius Cycle Incidence Matrix)

Let G=(V,E) be a finite graph and R∈ℕ.

Let

C_R(G) = { C ⊆ E : C is a simple cycle and C ⊆ B_R(v) for some v∈V }.

Define the matrix

M_R(G) ∈ {0,1}^{|C_R(G)| × |E|}

by

(M_R(G))_{C,e} =
1 if e ∈ C  
0 otherwise.

Define

rank_F2(M_R(G)).

## Lemma (Orbit Compression)

If G is FO^k_R-homogeneous and deg(G) ≤ Δ then the number of radius-R rooted neighborhood types is bounded by

T(k,Δ,R).

Hence rows of M_R(G) collapse into finitely many cycle-orbit types.

## Rank Compression

Define quotient matrix

M̃_R

with rows indexed by cycle-orbit types and columns by edge-orbit types.

Then

rank_F2(M_R(G)) = rank_F2(M̃_R).

Thus

FO^k_R-homogeneity ⇒ rank_F2(M_R(G)) ≤ T(k,Δ,R).

## Cycle Packing Lemma

If G contains m edge-disjoint cycles inside radius-R neighborhoods then

rank_F2(M_R(G)) ≥ m.

## Expander Cycle Packing

Bounded-degree expanders contain Ω(|V|) short cycles.

Thus

rank_F2(M_R(G)) ≥ c|V|.

## Cycle–Overlap Rank Rigidity

For fixed k,Δ there exist constants R,T such that

FO^k_R-homogeneous(G) ⇒ rank_F2(M_R(G)) ≤ T.

But expanders satisfy

rank_F2(M_R(G)) ≥ c|V|.

For sufficiently large graphs this yields a contradiction.

Therefore

large cycle-overlap rank ⇒ FO^k local-type diversification.
