# Specification of C(k,Δ,R)

Let Δ be a maximum degree bound.

Let B = 1 + Δ + Δ^2 + ... + Δ^R.

Let T(k,B) be the number of FO^k-types on rooted structures of size ≤ B.

Define

C(k,Δ,R) := T(k,B) · (Δ^(2*R))

This is an explicit finite bound depending only on (k,Δ,R).

Target lemma:

FO^k_R-homogeneous(G) ⇒ COR_R(G) ≤ C(k,Δ,R).
