# Cycle-Signature Boundedness and Remaining Failure Modes

## Target Lemma (Cycle-Signature Boundedness)

Fix integers \(k,\Delta,R\).

Let \(G\) be a finite graph with maximum degree at most \(\Delta\). Assume \(G\) is \(FO^k_R\)-homogeneous, i.e.

\[
\forall v,w \in V(G),\qquad (B_R(v),v) \equiv_{FO^k} (B_R(w),w).
\]

Let \(\mathcal C_R(G)\) denote the set of simple cycles contained in some radius-\(R\) neighborhood. For each \(C \in \mathcal C_R(G)\), define its local cycle signature to be the \(FO^k\)-type of the pair

\[
(B_R(v),C),
\]

where \(v\) is any vertex such that \(C \subseteq B_R(v)\).

Then there exists a constant \(C(k,\Delta,R)\) such that

\[
|\mathcal S_R(G)| \le C(k,\Delta,R),
\]

where \(\mathcal S_R(G)\) is the set of all such local cycle signatures.

## Step 1. Finite local type bound

Because \(\deg(G)\le \Delta\), every radius-\(R\) neighborhood has at most

\[
N(\Delta,R)=1+\Delta+\Delta(\Delta-1)+\cdots+\Delta(\Delta-1)^{R-1}
\]

vertices.

Hence there are only finitely many rooted radius-\(R\) graphs of degree at most \(\Delta\), and therefore only finitely many rooted \(FO^k\)-types:

\[
|\mathrm{Type}^{k}_{\Delta,R}| < \infty.
\]

## Step 2. Homogeneity collapses rooted local types

By \(FO^k_R\)-homogeneity, all rooted neighborhoods realize a single rooted \(FO^k\)-type.

Thus every cycle in \(\mathcal C_R(G)\) is contained in an ambient rooted neighborhood of one fixed \(FO^k\)-type.

## Step 3. Cycles are local objects

Every row of the bounded-radius cycle incidence matrix \(M_R(G)\) is represented by a simple cycle \(C\subseteq B_R(v)\) for some \(v\).

Therefore every row is coded by a pair \((B_R(v),C)\) inside one fixed bounded-size ambient structure.

## Step 4. Finite signature bound

Inside a bounded-size structure, the number of edge-subsets is finite. Therefore the number of \(FO^k\)-equivalence classes of pairs \((B_R(v),C)\), where \(C\) is a simple cycle, is bounded by a constant depending only on \(k,\Delta,R\).

Hence

\[
|\mathcal S_R(G)| \le C(k,\Delta,R).
\]

## Step 5. Orbit-compressed cycle matrix

Compress the rows of \(M_R(G)\) by cycle signature, and compress the columns by local edge signature. Denote the compressed matrix by \(\widetilde M_R(G)\).

Then

- the number of row types is at most \(C(k,\Delta,R)\),
- the number of column types is at most \(D(k,\Delta,R)\),

for some constant \(D(k,\Delta,R)\).

Therefore

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G))
=
\operatorname{rank}_{\mathbb F_2}(\widetilde M_R(G))
\le \min\{C(k,\Delta,R),D(k,\Delta,R)\}.
\]

Thus there exists \(T(k,\Delta,R)\) such that

\[
FO^k_R\text{-homogeneous}(G)
\Rightarrow
\operatorname{rank}_{\mathbb F_2}(M_R(G)) \le T(k,\Delta,R).
\]

## Contrapositive form

\[
\operatorname{rank}_{\mathbb F_2}(M_R(G)) > T(k,\Delta,R)
\Rightarrow
|\mathrm{FO}^k_R(G)| > 1.
\]

Equivalently, large bounded-radius cycle-overlap rank forces \(FO^k\)-local type diversification.

## First remaining failure mode

The argument above uses compression by \(FO^k\)-signature of pairs \((B_R(v),C)\). This requires that the class of simple cycles contained in \(B_R(v)\) is uniformly capturable at the logical level being used.

The possible failure point is:

\[
\text{``simple cycle'' may fail to be uniformly definable in the chosen } FO^k \text{ coding regime.}
\]

If cyclehood is not uniformly representable, then the passage from raw rows of \(M_R(G)\) to finitely many logical cycle signatures is not justified.

This is repaired by adding a coding lemma:

### Coding Lemma
For fixed \(R\) and bounded degree \(\Delta\), every simple cycle contained in a radius-\(R\) neighborhood can be encoded by a bounded tuple of local vertices/edges, and equality of codes is expressible in the chosen finite-variable logic or proxy formalism.

## Second remaining failure mode

The argument above tacitly identifies equal logical signatures with equal \(\mathbb F_2\)-row behavior after compression.

The possible failure point is:

\[
\text{distinct cycles with the same } FO^k \text{ signature may contribute linearly independent } \mathbb F_2 \text{-rows}.
\]

If that happens, boundedly many logical types would not imply bounded matrix rank.

This is repaired by adding a row-normalization lemma:

### Row-Normalization Lemma
For fixed \(k,\Delta,R\), the \(\mathbb F_2\)-row of a cycle in \(M_R(G)\) is determined, after local signature compression, by a bounded combinatorial normal form depending only on its \(FO^k\)-signature.

With this lemma, equal cycle signatures yield identical compressed rows, and boundedly many signatures imply bounded compressed rank.

## Final reduction chain

\[
\text{Cycle Coding Lemma}
\Rightarrow
\text{Cycle-Signature Boundedness}
\Rightarrow
\text{Row-Normalization Lemma}
\Rightarrow
\text{Cycle-Overlap Rank Rigidity}
\Rightarrow
\text{FO}^k\text{ Local Rigidity}
\Rightarrow
\text{EntropyDepth lower bound}
\Rightarrow
\text{Chronos closure.}
