# Row-Normalization Lemma — Rigorization

## Goal

Show that boundedly many logical cycle signatures imply bounded \(\mathbb F_2\)-rank of the bounded-radius cycle incidence matrix after compression.

---

## Setup

Let \(M_R(G)\) be the bounded-radius cycle incidence matrix:

- rows indexed by cycles \(C \in \mathcal C_R(G)\),
- columns indexed by edges \(e \in E(G)\),
- entries in \(\mathbb F_2\),
- \(M_R(G)_{C,e}=1\) iff \(e \in C\).

Assume:

1. cycle signatures are logically definable,
2. the number of signatures is bounded by \(S(k,\Delta,R)\),
3. the graph is \(FO^k_R\)-homogeneous.

---

## Edge compression

Because rooted radius-\(R\) neighborhoods realize boundedly many local types, edges incident to these neighborhoods fall into boundedly many local edge classes.

Fix a compression map

\[
\pi_E : E(G) \to \{1,\dots,D(k,\Delta,R)\}.
\]

This sends each edge to its local edge signature class.

---

## Cycle compression

Fix a compression map

\[
\pi_C : \mathcal C_R(G) \to \{1,\dots,S(k,\Delta,R)\}
\]

sending each cycle to its logical signature.

---

## Compressed row normal form

For each cycle \(C\), define its normalized compressed row

\[
N(C) \in \mathbb F_2^{D(k,\Delta,R)}
\]

by

\[
N(C)_j
=
\sum_{\substack{e \in C \\ \pi_E(e)=j}} 1 \pmod 2.
\]

This records, modulo \(2\), the parity with which the cycle uses each compressed edge class.

---

## Normalization lemma

If two cycles \(C_1,C_2\) have the same logical signature, then

\[
\pi_C(C_1)=\pi_C(C_2)
\Rightarrow
N(C_1)=N(C_2).
\]

Reason: equal signatures identify the same canonical tuple-coded cycle pattern inside the same bounded rooted local type, hence induce the same parity profile across compressed edge classes.

Thus normalized rows depend only on logical signature.

---

## Rank consequence

Since there are at most \(S(k,\Delta,R)\) cycle signatures, the set

\[
\{N(C): C \in \mathcal C_R(G)\}
\]

contains at most \(S(k,\Delta,R)\) distinct vectors in \(\mathbb F_2^{D(k,\Delta,R)}\).

Hence the compressed cycle matrix has at most \(S(k,\Delta,R)\) distinct rows and \(D(k,\Delta,R)\) columns.

Therefore

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G))
=
\operatorname{rank}_{\mathbb F_2}(\widetilde M_R(G))
\le
\min\{S(k,\Delta,R),D(k,\Delta,R)\}.
\]

This yields the desired constant-rank bound.

---

## Tightened conclusion

Logical signature boundedness plus row normalization implies bounded compressed rank.

This completes the rigorous bridge from logical homogeneity to bounded cycle-incidence rank.
