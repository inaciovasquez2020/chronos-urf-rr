# Oblivion Atom — Formal Definitions

## Radius-R Ball

For a graph G = (V,E) and vertex v ∈ V,

B_R(v) = { u ∈ V : dist_G(u,v) ≤ R }.

## Cycle Rank (Betti Number)

For a finite graph H,

β₁(H) = |E(H)| − |V(H)| + c(H)

where c(H) is the number of connected components.

## Cycle-Overlap Rank

Let Z_R(G) be the span over F₂ of all cycles contained in
radius-R balls of G.

COR_R(G) = dim_F₂ Z_R(G).

## FO^k_R Neighborhood Type

Two vertices u,v are FO^k_R-equivalent if their
radius-R neighborhoods satisfy the same FO^k formulas.

A graph is FO^k_R-homogeneous if all vertices share
the same FO^k_R type.

## Oblivion Atom Target

For bounded-degree graphs:

COR_R(G) ≥ T ⇒ FO^k_R type diversity.

