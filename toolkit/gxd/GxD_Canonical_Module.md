GxD — Global × Detectability (Canonical Toolkit Module)

Status: Complete (F2 closure model verified)

Definition:
Given a finitely generated group H with generating set S and word length ℓ,
and an action H ↷ 𝒮,
with observer O: 𝒮 → 𝒴,

Define:

Code_O(s;R) = { O(h⋅s) : ℓ(h) ≤ R }

GxD_O(s) = limsup_{R→∞} (1/R) log |Code_O(s;R)|

Growth exponent:
κ(H,S) = limsup_{R→∞} (1/R) log |B_R|

Core Results:

1. 0 ≤ GxD_O(s) ≤ κ(H,S)

2. Polynomial collision bound ⇒ GxD_O(s) = κ(H,S)

3. Exponential collision bound δ ⇒
   GxD_O(s) ≥ κ(H,S) − δ

4. Orbit invariance:
   GxD_O(g⋅s) = GxD_O(s)

5. Monotonicity:
   Observer refinement increases GxD.

F2 Instance:
κ(F2,S) = log 3
Length–Separation constant explicit
Collision polynomial ⇒ GxD = log 3

Interpretation:
GxD measures exponential detectability of global expansion through bounded observation.

Relationship:
Rflect = inevitability (qualitative)
GxD = entropy rate (quantitative)
Chronos = depth amplification under bounded capacity
