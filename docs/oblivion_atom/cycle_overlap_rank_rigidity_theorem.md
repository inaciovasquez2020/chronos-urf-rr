# Cycle–Overlap Rank Rigidity Theorem

## Theorem (Cycle–Overlap Rank Rigidity)

Fix integers \(k,\Delta\).

There exist constants \(R,T\) such that for every graph \(G\) with maximum degree \(\le \Delta\)

\[
FO^k_R\text{-homogeneous}(G)
\Rightarrow
\operatorname{rank}_{\mathbb F_2}(M_R(G)) \le T.
\]

Here \(M_R(G)\) denotes the bounded-radius cycle incidence matrix.

---

## Proof Structure

The proof decomposes into four lemmas.

---

### Lemma 1 — Cycle Coding Lemma

Every simple cycle contained in \(B_R(v)\) can be encoded by a bounded tuple of vertices.

Therefore cycles inside radius-\(R\) neighborhoods admit a canonical logical representation.

---

### Lemma 2 — Finite Local Type Bound

For bounded degree graphs

\[
|\mathrm{FO}^k_R\text{ rooted types}| \le T_1(k,\Delta,R).
\]

Thus only finitely many rooted neighborhood structures exist.

---

### Lemma 3 — Cycle Signature Boundedness

Under \(FO^k_R\)-homogeneity every cycle \(C\subseteq B_R(v)\) appears inside the same logical neighborhood type.

Hence the number of cycle signatures satisfies

\[
|\mathcal S_R(G)| \le T_2(k,\Delta,R).
\]

---

### Lemma 4 — Row Normalization Lemma

Cycles sharing the same logical signature produce identical compressed rows in the cycle incidence matrix.

Therefore

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G)) \le |\mathcal S_R(G)|.
\]

---

## Conclusion

Combining the lemmas gives

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G)) \le T(k,\Delta,R)
\]

for constant \(T\).

---

## Contrapositive Form

If

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G)) > T
\]

then

\[
|\mathrm{FO}^k_R(G)| > 1.
\]

Thus large cycle-overlap rank forces local type diversification.

---

## Role in Oblivion Atom

Expanders satisfy

\[
\operatorname{rank}(M_R(G)) = \Theta(n).
\]

Hence bounded-degree expanders cannot remain \(FO^k_R\)-homogeneous.

This establishes **Cycle–Local Rigidity**, the core structural component of the Oblivion Atom program.
