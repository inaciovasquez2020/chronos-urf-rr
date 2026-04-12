# Newstein Rooted Ball Trivialization

## Status
OPEN

## Dependency
- `NEWSTEIN_TREE_CONTRACTION_HOMOTOPY_LEMMA.md`

## Minimal sufficient assumption
Assume there exists a chain homotopy
\[
h : C_k(B_R(r)) \to C_{k+1}(B_R(r))
\]
such that
\[
\operatorname{supp}(h(c)) \subseteq B_R(r)
\quad\wedge\quad
\partial h + h \partial = \mathrm{Id} - \mathrm{Retr}_r.
\]

## Target statement
For every \(k \ge 1\),
\[
Z_k(B_R(r)) = B_k(B_R(r)).
\]

Equivalently, every \(k\)-cycle in the rooted ball is null-homologous inside \(B_R(r)\).

## Derivation
Let \(c \in Z_k(B_R(r))\). Then \(\partial c = 0\). Apply the homotopy identity:
\[
(\partial h + h\partial)(c) = c - \mathrm{Retr}_r(c).
\]
Since \(\partial c = 0\),
\[
\partial h(c) = c - \mathrm{Retr}_r(c).
\]
For \(k \ge 1\), the constant retraction annihilates \(k\)-chains:
\[
\mathrm{Retr}_r(c)=0.
\]
Hence
\[
\partial h(c)=c.
\]
Thus \(c \in B_k(B_R(r))\).

## Closure criterion
This file may be flipped from `OPEN` to `PROVED` exactly when the existence of the local contraction homotopy is formalized repo-natively.

## Forward chain
\[
\mathrm{RootedBallTrivialization}
\Longrightarrow
\mathrm{FiberQuotientRank}
\Longrightarrow
\mathrm{DirectSumIndependence}
\Longrightarrow
\mathrm{PerStepInformationBound}
\Longrightarrow
\mathrm{QuotientGapClosure}.
\]

