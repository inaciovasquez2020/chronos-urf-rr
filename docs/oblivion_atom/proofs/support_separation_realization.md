# Support–Separation Realization Lemma

## Statement

Let \(G\) be a finite graph with maximum degree \(\Delta\).

Let

\[
C_1,\dots,C_m
\]

be normalized supports with

\[
|\operatorname{supp}(C_j)| \le B.
\]

Assume each support is uniformly definable by an \(FO^k_r\) formula

\[
\varphi_j(x)
\]

such that

\[
G \models \varphi_j(v) \iff v \in \operatorname{supp}(C_j).
\]

Define the signature map

\[
\sigma(v)_j =
\begin{cases}
1 & v \in \operatorname{supp}(C_j) \\
0 & \text{otherwise}
\end{cases}
\]

Then

\[
\sigma(u) \neq \sigma(v)
\Rightarrow
tp^k_r(u) \neq tp^k_r(v).
\]

Therefore

\[
|FO^k_r(G)| \ge |\sigma(V)|.
\]

---

## Proof

Each coordinate of the signature corresponds to evaluation of a formula

\[
\sigma(v)_j = 1 \iff G \models \varphi_j(v).
\]

Hence the signature vector is exactly the truth-value vector

\[
(\varphi_1(v),\dots,\varphi_m(v)).
\]

If

\[
\sigma(u) \neq \sigma(v)
\]

then there exists some \(j\) with

\[
G \models \varphi_j(u)
\quad\text{and}\quad
G \not\models \varphi_j(v).
\]

Thus the two vertices satisfy different \(FO^k_r\) formulas.

Therefore

\[
tp^k_r(u) \neq tp^k_r(v).
\]

---

## Consequence

The map

\[
v \mapsto tp^k_r(v)
\]

is injective on signature classes.

Hence

\[
|FO^k_r(G)| \ge |\sigma(V)|.
\]

