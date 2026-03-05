# FOᵏ Formula from EF-Game Cycle Detection

## Status

Translate Spoiler winning strategy into explicit FOᵏ formula.

---

# 1. Cycle Detection Predicate

Let

Cycle(x)

denote

“x lies on a simple cycle of length ≤ L”.

FO formula:

∃x₁,…,x_L  
forming a closed walk with distinct vertices.

---

# 2. Cycle Participation

Define

Cycle_i(x)

for cycles detected within radius R.

---

# 3. Signature Formula

For vertex x define

\[
\sigma(x)
=
(Cycle_1(x),\dots,Cycle_m(x)).
\]

---

# 4. Distinguishing Formula

If two vertices differ in signature:

\[
\exists x \big(Cycle_i(x)\land\neg Cycle_i(y)\big).
\]

This formula uses only bounded variables.

---

# 5. Result

Thus EF Spoiler strategy corresponds to an FOᵏ formula detecting cycle participation differences.
