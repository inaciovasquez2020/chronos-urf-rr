# Corrected Signature Diversity Lemma

## Motivation

The earlier sparse-matrix argument for signature diversity was incomplete.
Column independence alone does not force many distinct rows.

A counterexample exists when many supports reuse the same vertices.

To fix this, we introduce a bounded vertex reuse condition.

---

## Lemma (Corrected Signature Diversity)

Let

\[
M \in \mathbb{F}_2^{V \times m}
\]

be the vertex–support incidence matrix of normalized supports.

Assume:

### 1. Support size bound

\[
|supp(C_j)| \le B
\]

### 2. Bounded vertex reuse

\[
|\{j : v \in supp(C_j)\}| \le L
\]

for all \(v \in V\).

### 3. Column independence

\[
rank(M) = m
\]

Then the number of distinct rows satisfies

\[
|\{\sigma(v)\}| \ge \frac{m}{B L}.
\]

Thus

\[
|\sigma(V)| \ge \beta m
\]

with

\[
\beta = \frac{1}{BL}.
\]

---

## Proof Sketch

Each column introduces at most \(B\) vertices.

Each vertex can appear in at most \(L\) supports.

Thus each vertex can only account for at most \(L\) columns.

To realize \(m\) independent columns we therefore require

\[
|V| \ge \frac{m}{BL}.
\]

Each vertex contributes a row signature.

Thus the number of distinct signatures is at least

\[
\Omega(m).
\]

---

## Consequence

Combining with Support-Separation Realization:

\[
|\sigma(V)| \ge \beta m
\Rightarrow
|FO^k_r(G)| \ge \beta m
\]

which completes the logical bridge.

