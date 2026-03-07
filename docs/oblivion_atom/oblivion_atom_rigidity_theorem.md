# Oblivion Atom Rigidity Theorem

## Theorem

Let \(k,\Delta \in \mathbb N\).

There exist constants

\[
R,r,T,\beta >0
\]

such that for any finite graph \(G\) with

\[
\maxdeg(G) \le \Delta
\]

the following holds:

\[
COR_R(G) \ge T
\Rightarrow
|FO^k_r(G)| \ge \beta \cdot COR_R(G).
\]

---

## Proof Outline

### Step 1 — Cycle Rank Rigidity

Normalized supports produce a sparse incidence matrix with

\[
rank(M) = COR_R(G).
\]

### Step 2 — Sparse Signature Diversity

From sparsity:

\[
|\sigma(V)| \ge \beta \cdot COR_R(G).
\]

### Step 3 — Support Separation

Each support is FO-definable using anchor formulas:

\[
\sigma(v)_j = \phi_j(v).
\]

### Step 4 — Type Separation

Distinct signatures imply distinct FO-types:

\[
\sigma(u) \neq \sigma(v)
\Rightarrow
tp^k_r(u) \neq tp^k_r(v).
\]

Thus

\[
|FO^k_r(G)| \ge |\sigma(V)|.
\]

Combining:

\[
|FO^k_r(G)| \ge \beta \cdot COR_R(G).
\]

