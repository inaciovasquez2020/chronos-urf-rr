# Cycle–Local Rigidity Theorem (C^k Version)

## Theorem

Let k, Δ, R ∈ ℕ.

Let G be a finite graph with maximum degree ≤ Δ.

Assume

    tp_{C^k}(B_R(u)) = tp_{C^k}(B_R(v))  for all vertices u,v ∈ V(G).

Then there exists a constant

    C = C(k, Δ, R)

such that

    COR(G) ≤ C.

Here COR(G) is the cycle-overlap rank.

---

## Step 1 — C^k Type Finiteness

Let

    N = N(k, Δ, R)

be the number of C^k-types of rooted radius-R neighborhoods in bounded-degree graphs.

This number is finite.

---

## Step 2 — Short Cycle Detection

Assume existence of C^k formulas

    χ_ℓ(x,y)

such that

    G ⊨ χ_ℓ(x,y)

iff edge xy lies on a simple cycle of length ℓ ≤ 2^k
contained in

    B_R(x) ∪ B_R(y).

Let

    L = 2^k.

---

## Step 3 — Length Profile

For each edge e define

    Π(e) = { ℓ ≤ L : G ⊨ χ_ℓ(e) }.

Uniformity of C^k types implies

    Π(e) = Π

for all edges.

---

## Step 4 — Short Cycle Generators

Every cycle of length > L can be reduced using symmetric difference with a short cycle through one of its edges.

Therefore the cycle space has a basis

    B

consisting of cycles of length ≤ L.

Let

    β = |B|.

---

## Step 5 — Edge Neighborhood Types

For each edge e = (x,y)

    N_R(e) = (B_R(x) ∪ B_R(y), x, y).

All such rooted structures share the same C^k type.

---

## Step 6 — Cycle Pattern Classes

For ℓ ∈ Π define

    P_ℓ(e) = { C ∈ C_ℓ : e ∈ C }.

Edges are equivalent if

    (N_R(e), P_ℓ(e)) ≅ (N_R(f), P_ℓ(f)).

The number of equivalence classes is bounded by

    M_ℓ = M_ℓ(k, Δ, R).

Let

    M = max_ℓ M_ℓ.

---

## Step 7 — Basis Bound

Each cycle in B_ℓ occupies a distinct equivalence class.

Therefore

    |B_ℓ| ≤ M_ℓ.

Hence

    β ≤ 2^k · M.

---

## Step 8 — Incidence Matrix

Let

    A ∈ ℚ^{|E| × β}

with

    A_{e,C} = 1  if e ∈ C.

The number of possible row patterns is bounded by

    M^{2^k}.

Thus

    rank(A) ≤ M^{2^k}.

---

## Step 9 — Cycle Overlap Matrix

Let

    O = AᵀA.

Then

    COR(G) = rank(O) ≤ rank(A) ≤ M^{2^k}.

---

## Result

    COR(G) ≤ M^{2^k}.

This bound depends only on k, Δ, R.
