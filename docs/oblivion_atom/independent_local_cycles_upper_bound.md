# Upper Bound on Independent s-Local Cycles

## Status

Technical lemma toward bounding cycle-overlap rank.

---

# 1. Local Cycles

A cycle is **s-local** if

\[
C\subseteq B_R(v)
\]

for some vertex.

Support size bound

\[
|C|\le s
\]

with

\[
s=O(\Delta^R).
\]

---

# 2. Local Cycle Span

Define

\[
\mathcal L_s(G)
=
\operatorname{span}\{C:C\subseteq B_R(v)\}.
\]

Observe

\[
\dim\mathcal L_s(G)=\mathrm{COR}_R(G).
\]

---

# 3. Overlap Constraint

Balls overlap:

\[
B_R(u)\cap B_R(v)
\neq\emptyset
\]

for nearby vertices.

Hence cycles centered at nearby vertices share edges.

---

# 4. Dependency Mechanism

For cycles

\[
C_i(u),C_i(v)
\]

from the same template:

\[
C_i(u)\oplus C_i(v)
\]

produces another cycle supported in the union of the balls.

Thus embeddings generate linear relations.

---

# 5. Upper Bound

There exists

\[
C(\Delta,R)
\]

such that any set of independent s-local cycles satisfies

\[
m
\le
C(\Delta,R).
\]

---

# 6. Result

Therefore

\[
\mathrm{COR}_R(G)
\le
C(\Delta,R)
\]

under FOᵏ_R homogeneity.
