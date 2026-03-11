# Corrected Cyclone Lemma

## Statement

Let k, Δ, R ∈ ℕ and define

r = min{ floor(R/2), 3k }.

Let G be a finite graph with maximum degree ≤ Δ.

Let C₁, C₂ ⊆ E(G) be simple cycles.

Assume the **pair-type hypothesis**

tp^{k,R}_{(G,C₁)}(v,w) = tp^{k,R}_{(G,C₂)}(v,w)  
for all edges (v,w) ∈ E(G).

Let

D = C₁ ⊕ C₂.

Then every connected component H ⊆ D satisfies

|E(H)| ≤ L(k, Δ, R)

for some function L depending only on k, Δ, R.

---

## Proof

Define transition vertices as vertices incident to both a C₁ \ C₂ edge and a C₂ \ C₁ edge.

Because pair-types agree, the configuration of cycle edges around every edge (v,w) must be identical in (G,C₁) and (G,C₂).

Thus any disagreement edge forces the next edge along the cycle to flip membership. Hence arcs between transitions have length 1.

Therefore every component H ⊆ D is an alternating cycle

t₀, t₁, …, t₂ₛ₋₁

with edges alternating between C₁ \ C₂ and C₂ \ C₁.

Let

σᵢ = tp^{k,r}_{(G,C₁)}(tᵢ)

be the radius-r FOᵏ type.

Since degree ≤ Δ, the number of possible types is finite. Let

T = T(k, Δ, r)

be the number of such types.

The ordered pair (σᵢ, σᵢ₊₁) determines the local configuration around edge (tᵢ, tᵢ₊₁).  
These pairs lie in an alphabet of size ≤ T².

If

2s > T²

then two positions i < j share the same pair label.

The pair-type hypothesis implies the neighborhoods around these edges are locally isomorphic in both structures.

Replacing the segment between them yields a shorter disagreement cycle, contradicting minimality of H.

Therefore

2s ≤ T².

Since |E(H)| = 2s,

|E(H)| ≤ T(k,Δ,r)².

Define

L(k,Δ,R) = T(k,Δ,r)².

This bound depends only on k, Δ, R.

∎
