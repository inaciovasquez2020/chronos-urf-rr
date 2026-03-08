# Cycle Coding Lemma

## Statement

Fix integers \(R,\Delta\).

Let \(G\) be a graph with maximum degree \(\Delta\).  
Let \(B_R(v)\) denote the radius-\(R\) neighborhood around \(v\).

Then every simple cycle \(C \subseteq B_R(v)\) can be encoded by a bounded tuple of vertices

\[
(v_0,v_1,\dots,v_\ell)
\]

such that

- \(v_i\) are vertices of \(B_R(v)\)
- \((v_i,v_{i+1}) \in E(G)\)
- \(v_0=v_\ell\)
- the tuple length \(\ell \le L(\Delta,R)\)

for a constant

\[
L(\Delta,R) \le 2R.
\]

Thus every cycle inside \(B_R(v)\) admits a bounded representation.

---

## Canonical Cycle Encoding

Define the canonical code of a cycle \(C\) as

1. Choose the smallest vertex of \(C\) under the ordering of \(B_R(v)\).
2. Orient the cycle so that the lexicographically smallest edge sequence is chosen.
3. Record the ordered vertex sequence.

This produces a unique canonical tuple

\[
\mathrm{code}(C)=(v_0,v_1,\dots,v_\ell).
\]

---

## FOᵏ Definability

For sufficiently large \(k\) the following relations are expressible:

- adjacency
- equality
- vertex order inside \(B_R(v)\)

Thus the predicate

\[
\text{CycleTuple}(v_0,\dots,v_\ell)
\]

is definable.

Therefore cycle equality is expressible via equality of tuples.

---

## Consequence

Cycle signatures can be represented by bounded tuples.

Thus

\[
(B_R(v),C)
\]

has finitely many logical representations depending only on \(k,\Delta,R\).

This provides the coding step required in the Cycle-Signature Boundedness Lemma.
