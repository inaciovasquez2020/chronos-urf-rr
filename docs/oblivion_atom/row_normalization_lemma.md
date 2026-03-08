# Row Normalization Lemma

## Statement

Fix \(k,\Delta,R\).

Let \(M_R(G)\) be the bounded-radius cycle incidence matrix.

Let cycles be grouped by logical signature

\[
\tau(C)=\text{FO}^k\text{-type}(B_R(v),C).
\]

Then there exists a normalization map

\[
N : \mathcal C_R(G) \to \mathbb F_2^{E_{\text{orbit}}}
\]

such that

\[
\tau(C_1)=\tau(C_2) \Rightarrow N(C_1)=N(C_2).
\]

Thus cycles of the same signature produce identical rows in the compressed matrix.

---

## Construction

1. Compress vertices by \(FO^k_R\) type.
2. Compress edges by the pair of endpoint types.
3. Encode a cycle by the multiset of compressed edges it uses.

This defines a canonical compressed row.

---

## Rank Bound

Let

\[
s = |\mathcal S_R(G)|
\]

be the number of cycle signatures.

Then the compressed matrix has at most \(s\) distinct rows.

Hence

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G)) \le s.
\]

Combined with the Cycle-Signature Boundedness Lemma,

\[
s \le C(k,\Delta,R),
\]

so

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G)) \le C(k,\Delta,R).
\]

---

## Role in Rigidity

This lemma ensures that logical cycle types determine linear row behavior.

Thus bounded logical types imply bounded cycle-incidence rank.
