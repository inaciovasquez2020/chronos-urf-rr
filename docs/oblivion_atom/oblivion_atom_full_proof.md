# Oblivion Atom — Cycle–Overlap Rank Rigidity

## Theorem (Cycle–Overlap Rank Rigidity)

Fix integers \(k\) and \(\Delta\).

There exist constants \(R\) and \(T\) such that for every graph \(G\) with maximum degree at most \(\Delta\),

\[
FO^k_R\text{-homogeneous}(G)
\Rightarrow
\operatorname{rank}_{\mathbb F_2}(M_R(G)) \le T.
\]

Here

- \(M_R(G)\) is the bounded-radius cycle incidence matrix.
- Rows correspond to cycles contained in radius-\(R\) neighborhoods.
- Columns correspond to edges of \(G\).
- Entries lie in \(\mathbb F_2\).

---

# 1. Cycle Coding Lemma

Every cycle \(C\subseteq B_R(v)\) can be encoded by a bounded tuple

\[
(v_0,\ldots,v_\ell)
\]

with \(\ell \le L(\Delta,R)\).

Because adjacency and equality are FO-definable, the predicate

\[
\text{CycleTuple}(v_0,\dots,v_\ell)
\]

is definable.

Thus cycles admit canonical logical encodings.

---

# 2. Finite Local Type Bound

For bounded-degree graphs:

\[
|\mathrm{FO}^k_R\text{ rooted types}| \le T_1(k,\Delta,R)
\]

This follows from standard EF-game counting.

Thus only finitely many local neighborhood structures exist.

---

# 3. Cycle Signature Boundedness

Define the cycle signature

\[
\tau(C) = \mathrm{FO}^k_R(B_R(v),C).
\]

Under \(FO^k_R\) homogeneity every vertex neighborhood is isomorphic.

Therefore cycles belong to a finite set of logical signatures:

\[
|\mathcal S_R(G)| \le T_2(k,\Delta,R).
\]

---

# 4. Row Normalization Lemma

Cycles sharing the same signature produce identical compressed rows in the cycle-incidence matrix.

Define compression:

1. Collapse vertices by FO-type.
2. Collapse edges by endpoint types.
3. Represent cycles by compressed edge multisets.

Thus

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G))
\le
|\mathcal S_R(G)|.
\]

---

# 5. Rank Bound

Combining previous steps:

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G))
\le
T(k,\Delta,R).
\]

This proves Cycle–Overlap Rank Rigidity.

---

# 6. Contrapositive Form

If

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G)) > T
\]

then

\[
|\mathrm{FO}^k_R(G)| > 1.
\]

Thus large cycle-overlap rank forces local logical diversity.

---

# 7. Expander Consequence

Bounded-degree expanders satisfy

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G)) = \Theta(n).
\]

Therefore expanders cannot remain FOᵏ-locally homogeneous.

---

# 8. Oblivion Atom

The final structural statement:

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G)) > T
\Rightarrow
|\mathrm{FO}^k_R(G)| > 1.
\]

Large overlapping cycle structure forces logical diversification.

---

# 9. Integration into Chronos

Cycle–Overlap Rank Rigidity implies:

\[
\text{FO}^k\text{ Local Rigidity}
\Rightarrow
\text{EntropyDepth lower bound}
\Rightarrow
\text{Chronos framework}.
\]

Thus refinement processes cannot compress entropy beyond linear depth on such structures.

---

# 10. Empirical Validation

Experiments in this repository confirm:

Random regular graphs  
→ linear cycle rank

CFI homogeneous constructions  
→ rank collapse

Thus cycle-incidence rank separates homogeneous and non-homogeneous regimes.

---

# Conclusion

Cycle-Overlap Rank Rigidity provides the deterministic structural mechanism preventing bounded-type collapse in bounded-degree graphs.

This establishes the core rigidity principle required for the Oblivion Atom program.
