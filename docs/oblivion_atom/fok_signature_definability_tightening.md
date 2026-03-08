# FO^k Signature Definability Tightening

## Goal

Tighten the logical step asserting that bounded-radius cycle signatures are uniformly capturable in the finite-variable regime.

---

## Ambient setting

Fix integers \(k,\Delta,R\).  
Let \(G\) be a graph with maximum degree at most \(\Delta\).  
Let \(B_R(v)\) denote the radius-\(R\) neighborhood of a root \(v\).

Let \(\mathcal C_R(G)\) be the set of simple cycles contained in some \(B_R(v)\).

We seek a uniform coding of each \(C \in \mathcal C_R(G)\) by a bounded tuple so that logical comparison of cycles reduces to logical comparison of bounded tuples.

---

## Radius bound on cycle length

If \(C \subseteq B_R(v)\), then every pair of vertices of \(C\) has graph distance at most \(2R\) inside \(G\).

Hence every simple cycle contained in \(B_R(v)\) has length at most

\[
L(\Delta,R) \le |B_R(v)| \le 1+\Delta+\Delta(\Delta-1)+\cdots+\Delta(\Delta-1)^{R-1}.
\]

Thus cycle length is bounded by a constant depending only on \(\Delta,R\).

---

## Canonical tuple coding

For each simple cycle \(C\subseteq B_R(v)\), choose the unique tuple

\[
\mathrm{code}(C)=(x_0,\dots,x_{\ell-1})
\]

satisfying:

1. \((x_i,x_{i+1})\in E(G)\) for all \(i<\ell-1\),
2. \((x_{\ell-1},x_0)\in E(G)\),
3. the \(x_i\) are pairwise distinct,
4. \(\ell \le L(\Delta,R)\),
5. among all cyclic rotations and reversals of the cycle, \((x_0,\dots,x_{\ell-1})\) is lexicographically minimal with respect to a fixed local ordering of \(B_R(v)\).

This gives a canonical representative for each cycle.

---

## Definability ingredients

To compare codes logically, it suffices to define:

1. adjacency,
2. equality,
3. bounded-tuple distinctness,
4. root-relative local order inside \(B_R(v)\),
5. the predicate that a tuple is a simple cycle tuple.

Adjacency and equality are first-order.

Since \(B_R(v)\) has bounded size depending only on \(\Delta,R\), one may fix a finite canonical labeling scheme for rooted radius-\(R\) neighborhoods. Therefore local order is uniformly reducible to finitely many rooted neighborhood types.

Hence the predicate

\[
\mathrm{CycleTuple}_{\ell}(x_0,\dots,x_{\ell-1};v)
\]

is uniformly representable for each \(\ell \le L(\Delta,R)\).

---

## Signature definability statement

For each \(\ell \le L(\Delta,R)\), the logical signature of a cycle is the rooted \(FO^k\)-type of the expansion

\[
(B_R(v),v,x_0,\dots,x_{\ell-1})
\]

where \((x_0,\dots,x_{\ell-1})=\mathrm{code}(C)\).

Because both the rooted neighborhood size and tuple length are bounded, the number of such \(FO^k\)-types is finite and bounded by a constant depending only on \(k,\Delta,R\).

Therefore cycle signatures are uniformly definable from bounded tuples.

---

## Tightened conclusion

There exists a constant \(S(k,\Delta,R)\) such that every cycle in \(\mathcal C_R(G)\) has one of at most \(S(k,\Delta,R)\) logically definable signatures.

This justifies the signature-compression step used in Cycle-Signature Boundedness.
