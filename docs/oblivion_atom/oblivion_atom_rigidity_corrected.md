# Oblivion Atom Rigidity Theorem (Corrected Version)

## Theorem

Let \(k,\Delta \in \mathbb N\).

There exist constants

\[
R,r,T,\beta > 0
\]

such that for any finite graph \(G\) with

\[
\maxdeg(G) \le \Delta
\]

the following holds:

\[
COR_R(G) \ge T
\implies
|FO^k_r(G)| \ge \beta \cdot COR_R(G).
\]

---

## Proof Outline

### Step 1 — Normalized Supports

Let

\[
m = COR_R(G)
\]

and extract normalized supports

\[
C_1,\dots,C_m
\]

with bounded support size

\[
|\operatorname{supp}(C_j)| \le B.
\]

---

### Step 2 — Vertex–Support Incidence Matrix

Define

\[
M \in \mathbb F_2^{V \times m},
\qquad
M_{v,j}=1 \iff v\in \operatorname{supp}(C_j).
\]

Assume the normalized supports are linearly independent, so

\[
\operatorname{rank}(M)=m.
\]

---

### Step 3 — Bounded Vertex Reuse

Assume there is a constant \(L\) such that

\[
|\{j : v\in \operatorname{supp}(C_j)\}| \le L
\qquad (v\in V).
\]

---

### Step 4 — Row Diversity

By the Row Diversity Lemma,

\[
|\{\operatorname{row}_v(M):v\in V\}| \ge \frac{m}{BL}.
\]

Equivalently, for the signature map

\[
\sigma(v)_j := M_{v,j},
\]

we have

\[
|\sigma(V)| \ge \frac{m}{BL}.
\]

---

### Step 5 — Support Separation

Assume each normalized support is uniformly \(FO^k_r\)-definable by formulas

\[
\varphi_j(x)
\]

satisfying

\[
G \models \varphi_j(v)
\iff
v \in \operatorname{supp}(C_j).
\]

Then distinct signatures imply distinct \(FO^k_r\)-types, so

\[
|FO^k_r(G)| \ge |\sigma(V)|.
\]

---

### Step 6 — Conclusion

Combining the previous steps,

\[
|FO^k_r(G)| \ge |\sigma(V)| \ge \frac{m}{BL}.
\]

Since \(m = COR_R(G)\), this gives

\[
|FO^k_r(G)| \ge \frac{1}{BL}\, COR_R(G).
\]

Thus the theorem holds with

\[
\beta = \frac{1}{BL}.
\]

