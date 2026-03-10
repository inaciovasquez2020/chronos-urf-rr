# Cyclone Proof Skeleton

## Goal

Prove:

For fixed k, Δ, R there exists C(k,Δ,R) such that

∀u,v ∈ V(G),
tp_FO^k(B_R(u)) = tp_FO^k(B_R(v))
⇒
COR(G) ≤ C(k,Δ,R).

---

## Dependency Chain

1. FO^k local type finiteness
2. Cycle pumping
3. Vertex signature bound
4. Cycle signature bound
5. Local EF extension
6. Edge agreement on short segments
7. Symmetric-difference short-cycle decomposition
8. Basis-signature injectivity
9. Rank bound for overlap matrix
10. Cyclone conclusion

---

## Lemma A

FO^k type finiteness:

T(k,Δ,R) < ∞.

---

## Lemma B

Cycle pumping:

L(k,Δ,R) = T(k,Δ,R)(2R+1)

and every cycle longer than L can be shortened preserving local FO^k signatures.

---

## Lemma C

Vertex signature count:

S(k,Δ,R) ≤ T(k,Δ,R) · 2^(Δ^(R+1)).

---

## Lemma D

Cycle signature count:

|Σ| ≤ S^L.

---

## Lemma E

Local EF radius:

r(k,R) = min(R/2, 3^k).

Every ≤ k-vertex pattern in B_r(u) is reproduced in B_r(v)
whenever

tp_FO^k(B_R(u)) = tp_FO^k(B_R(v)).

---

## Lemma F

Short segment agreement:

If two cycles have identical signatures, then every cycle segment
of length ≤ k agrees under local matching.

---

## Lemma G

Symmetric difference decomposition:

For cycles C1, C2 with identical signatures,

D = C1 ⊕ C2

decomposes into short cycles contained in unions of radius-r neighborhoods.

---

## Lemma H

Basis injectivity:

Distinct basis cycles have distinct signatures.

Hence if B is a short-cycle basis,

|B| ≤ S^L.

---

## Lemma I

Rank bound:

If M is the cycle-incidence matrix and O = M M^T, then

rank(O) ≤ rank(M) ≤ |B| ≤ S^L.

---

## Cyclone Bound

C(k,Δ,R) =
(T(k,Δ,R) · 2^(Δ^(R+1)))^(T(k,Δ,R)(2R+1)).

Thus

COR(G) ≤ C(k,Δ,R).

