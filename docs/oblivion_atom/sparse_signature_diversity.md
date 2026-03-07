# Sparse Incidence → Signature Diversity

## Lemma

Let

M ∈ F₂^{V × m}

be the vertex–support incidence matrix of normalized supports.

Assume

1. Support size bound

|supp(C_j)| ≤ B

2. Bounded vertex reuse

|{ j : v ∈ supp(C_j) }| ≤ L

for every vertex v.

3. Column independence

rank(M) = m

Then the number of distinct rows satisfies

|{σ(v)}| ≥ m / (B L).

Thus

|σ(V)| ≥ β m

with β = 1/(B L).

## Proof Sketch

Each column uses at most B vertices.

Each vertex can appear in at most L columns.

Therefore a single vertex can support at most L columns.

To realize m independent columns we require at least m/(B L) vertices.

Each vertex produces a row signature.

Thus the number of distinct signatures is Ω(m).
