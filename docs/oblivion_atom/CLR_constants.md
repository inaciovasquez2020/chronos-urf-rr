# Cycle–Local Rigidity Constants

Parameters

k  = FO^k variable bound  
Δ  = maximum graph degree  
R  = neighborhood radius

---

T(k,Δ,R)

Number of FO^k types of radius-R neighborhoods.

Bound:

T ≤ 2^(Δ^(R+1))

---

L(k,Δ,R)

Cycle pumping length

L = T(k,Δ,R)(2R+1)

---

S(k,Δ,R)

Vertex signature count

S ≤ T(k,Δ,R) · 2^(Δ^(R+1))

---

r(k)

Local EF radius

r = min(R/2,3^k)

---

Final rank bound

C(k,Δ,R) =
(T(k,Δ,R) · 2^(Δ^(R+1)))^(T(k,Δ,R)(2R+1))

Thus

COR(G) ≤ C(k,Δ,R)
