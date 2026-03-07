# Row Diversity Lemma

## Statement

Let

\[
M \in \mathbb F_2^{V\times m}
\]

be a binary matrix.

Assume:

1. Full column rank:

\[
\operatorname{rank}(M)=m.
\]

2. Column support bound:

\[
| \operatorname{supp}(M_{\ast j}) | \le B
\qquad (1\le j\le m).
\]

3. Row support bound:

\[
|\{j : M_{v,j}=1\}| \le L
\qquad (v\in V).
\]

Then the number of distinct rows of \(M\) satisfies

\[
|\{\operatorname{row}_v(M): v\in V\}| \ge \frac{m}{BL}.
\]

---

## Proof

Let \(R\) denote the number of distinct rows of \(M\).

Since each row has Hamming weight at most \(L\), each distinct row contains at most \(L\) ones.

Hence the total number of ones in the matrix is at most

\[
RL.
\]

On the other hand, each of the \(m\) columns has support size at least \(1\), and at most \(B\). Therefore the total number of ones is at most \(mB\), but more importantly, to realize \(m\) linearly independent columns under row-weight bound \(L\), at least \(m\) pivot incidences are required.

Each distinct row can contribute to at most \(L\) pivot columns, so the number of pivot columns is at most

\[
RL.
\]

Thus

\[
m \le RL.
\]

Since each pivot column uses at most \(B\) rows, normalizing by the maximal column support gives

\[
m \le RBL.
\]

Therefore

\[
R \ge \frac{m}{BL}.
\]

This proves the claim.

---

## Role in Oblivion Atom

Applied to the vertex-support incidence matrix \(M\), this yields

\[
|\sigma(V)| \ge \frac{COR_R(G)}{BL}.
\]

Combined with support separation:

\[
|\sigma(V)| \le |FO^k_r(G)|.
\]

Hence

\[
|FO^k_r(G)| \ge \beta\, COR_R(G)
\qquad\text{with}\qquad
\beta=\frac1{BL}.
\]

