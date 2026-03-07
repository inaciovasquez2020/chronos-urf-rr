# Support–Separation Realization

## Status

Conditional bridge lemma for the deterministic Oblivion chain.

---

## Setting

Fix integers \(k,\Delta,B \in \mathbb N\).

Let \(G=(V,E)\) be a finite graph with

\[
\maxdeg(G)\le \Delta .
\]

Let

\[
\mathcal C=\{C_1,\dots,C_m\}
\]

be a normalized family of cycle supports with

\[
|\operatorname{supp}(C_j)|\le B
\qquad (1\le j\le m).
\]

For each \(j\), fix an anchor vertex

\[
a_j \in \operatorname{supp}(C_j).
\]

Assume:

### (A1) Anchor uniqueness

For each \(j\) there exists a formula

\[
\alpha_j(x)\in FO^k_{r_0}
\]

such that

\[
G\models \alpha_j(v)\iff v=a_j .
\]

### (A2) Support reconstruction from the anchor

For each \(j\) there exists a formula

\[
\psi_j(x,y)\in FO^k_{r_1}
\]

such that

\[
G\models \psi_j(v,a_j)\iff v\in \operatorname{supp}(C_j).
\]

Equivalently, defining

\[
\varphi_j(x):=\exists y\,(\alpha_j(y)\wedge \psi_j(x,y)),
\]

we have

\[
G\models \varphi_j(v)\iff v\in \operatorname{supp}(C_j).
\]

### (A3) Sparse overlap

There exists \(B_\ast\in\mathbb N\) such that for every vertex \(v\in V\),

\[
\bigl|\{j : v\in \operatorname{supp}(C_j)\}\bigr|\le B_\ast .
\]

### (A4) Signature diversity

Define the signature map

\[
\sigma(v)_j := \mathbf 1_{\,G\models \varphi_j(v)} \in \mathbb F_2,
\qquad
\sigma:V\to \mathbb F_2^m .
\]

Assume there exists \(\beta>0\) such that

\[
|\sigma(V)|\ge \beta m .
\]

---

## Lemma

Let

\[
r := 1+\max(r_0,r_1).
\]

Under assumptions (A1)–(A4),

\[
|FO^k_r(G)| \ge |\sigma(V)| \ge \beta m .
\]

In particular, if

\[
m = COR_R(G),
\]

then

\[
|FO^k_r(G)| \ge \beta \, COR_R(G).
\]

---

## Proof

Let \(u,v\in V\) with

\[
\sigma(u)\neq \sigma(v).
\]

Then there exists some index \(j\) such that

\[
\sigma(u)_j\neq \sigma(v)_j.
\]

By definition of \(\sigma\),

\[
G\models \varphi_j(u)
\quad\text{and}\quad
G\not\models \varphi_j(v),
\]

or vice versa.

Hence the \(FO^k_r\)-types of \(u\) and \(v\) are distinct:

\[
\operatorname{tp}^k_r(u)\neq \operatorname{tp}^k_r(v).
\]

Therefore the map

\[
v \longmapsto \operatorname{tp}^k_r(v)
\]

is injective on each fiber of the signature map only when the signatures agree; equivalently, distinct signatures yield distinct \(FO^k_r\)-types. Thus

\[
|FO^k_r(G)| \ge |\sigma(V)|.
\]

By (A4),

\[
|FO^k_r(G)| \ge |\sigma(V)| \ge \beta m.
\]

This proves the claim.

---

## Consequence for Oblivion Atom

Once the sparse-incidence step yields

\[
|\sigma(V)|\ge \beta\, COR_R(G),
\]

the deterministic chain becomes

\[
COR_R(G)
\Rightarrow
\text{signature diversity}
\Rightarrow
|FO^k_r(G)|\ge \beta\, COR_R(G)
\Rightarrow
\text{non-homogeneity}.
\]

---

## Remaining input required

The only unresolved ingredient is a proof of (A4) from the normalized sparse incidence structure.

