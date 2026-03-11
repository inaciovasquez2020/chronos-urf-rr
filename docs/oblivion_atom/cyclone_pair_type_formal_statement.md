# Cyclone Lemma (Pair-Type Formal Statement)

Let k, Δ, R ∈ ℕ and define

r = min{ floor(R/2), 3k }.

Let G be a finite graph with maximum degree ≤ Δ.

Let C₁, C₂ ⊆ E(G) be simple cycles.

Assume the **pair-type FOᵏ equality condition**

tp^{k,R}_{(G,C₁)}(v,w) = tp^{k,R}_{(G,C₂)}(v,w)
for every edge (v,w) ∈ E(G).

Define the symmetric difference

D = C₁ ⊕ C₂.

Then every connected component H ⊆ D satisfies

|E(H)| ≤ L(k,Δ,R)

where

L(k,Δ,R) = T(k,Δ,r)²

and T(k,Δ,r) is the number of FOᵏ types of radius-r neighborhoods in graphs
with maximum degree ≤ Δ.
