# H4.1 finite-patch basis reduction

## Status
Conditional.

For fixed \(k,R,B \in \mathbb N\), let
\[
\mathcal B_{k,R,B}
\]
be any basis of the finite-dimensional space \(V_{k,R,B}\).

To prove
\[
V_{k,R,B}\cap U_{k,R,B}^{\perp}=\{0\},
\]
it is sufficient to prove:
\[
\forall b\in \mathcal B_{k,R,B},\quad b\in U_{k,R,B}\ \text{or}\ b\notin U_{k,R,B}^{\perp}.
\]

Equivalently, it is sufficient to prove:
\[
\forall b\in \mathcal B_{k,R,B}\setminus U_{k,R,B},\quad \exists u\in U_{k,R,B}\ \text{such that}\ \langle b,u\rangle\neq 0.
\]

## Reduction target
Every FO\(^k\)-local basis element outside \(U_{k,R,B}\) has nonzero correlation with some element of \(U_{k,R,B}\).
