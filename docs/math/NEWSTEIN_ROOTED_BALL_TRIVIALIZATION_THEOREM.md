# Newstein Rooted-Ball Trivialization Theorem

## Target statement

For every rooted center \(x\),
\[
\widetilde B_r^{\mathrm{tw}}(x)\cong \widetilde B_r^{\mathrm{triv}}(x).
\]

Hence
\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n).
\]

## Inputs

### 1. Local cycle-vanishing theorem

For every \(x \in V(B_n)\) and every local cycle \(C \subseteq B_r^{B_n}(x)\),
\[
\phi_H(C)=0.
\]

### 2. Local coboundary theorem

If \(U\) is connected and \(\phi(C)=0\) for every cycle \(C \subseteq U\), then there exists
\[
f:V(U)\to\mathbb F_2
\quad\text{such that}\quad
\phi=\delta f
\]
on every edge of \(U\).

## Deduction

Apply local cycle-vanishing on the rooted ball
\[
U:=B_r^{B_n}(x).
\]

By the local coboundary theorem, there exists
\[
f_x:V(U)\to\mathbb F_2
\]
such that
\[
\phi_H=\delta f_x
\]
on all edges of \(U\).

Use \(f_x\) as the gauge change trivializing the twisted cocycle on \(U\).

Therefore the twisted rooted ball and trivial rooted ball are isomorphic:
\[
\widetilde B_r^{\mathrm{tw}}(x)\cong \widetilde B_r^{\mathrm{triv}}(x).
\]

Since rooted radius-\(r\) balls agree for every center,
\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n).
\]

## Assembly theorem

Combining local cycle-vanishing and local coboundary yields rooted-ball trivialization and local-type equality.

## Status

This closes the rooted-ball branch of the Newstein chain at the theorem-ledger level.

## Dependencies discharged by this theorem

1. Local rooted-ball equivalence between twisted and trivial lifts.
2. Equality of rooted radius-\(r\) type data.
3. The local side of the non-factorization setup.
