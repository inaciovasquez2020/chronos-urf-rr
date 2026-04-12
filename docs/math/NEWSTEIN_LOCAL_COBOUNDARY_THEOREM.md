# Newstein Local Coboundary Theorem

## Target statement

Let \(U\) be a connected local subgraph. If
\[
\phi(C)=0
\quad
\text{for every cycle } C \subseteq U,
\]
then there exists
\[
f:V(U)\to\mathbb F_2
\quad\text{such that}\quad
\phi=\delta f
\]
on every edge of \(U\).

## Required subclaims

### 1. Path-difference produces a cycle

For any two paths \(P,Q\) in \(U\) with the same endpoints,
\[
P+Q
\]
is an \(\mathbb F_2\)-cycle in \(U\).

### 2. Path integral is endpoint-defined

Fix a basepoint \(u_0 \in V(U)\). Define
\[
f(v):=\int_{P_{u_0,v}}\phi
\]
for any path \(P_{u_0,v}\) from \(u_0\) to \(v\).

Prove this is independent of path choice.

### 3. Edgewise coboundary identity

For every edge \(ab\) of \(U\),
\[
\phi(ab)=f(a)+f(b).
\]

## Deduction

By 1, any two paths with common endpoints differ by a cycle.

By the cycle-vanishing hypothesis,
\[
\phi(P+Q)=0.
\]

Hence path integrals agree, so \(f\) is well-defined.

By adjoining an edge \(ab\) to a basepoint path, the difference of the two endpoint paths is the single edge \(ab\), hence
\[
\phi(ab)=f(a)+f(b).
\]

Therefore
\[
\phi=\delta f.
\]

## Assembly theorem

Combining 1–3 yields:
if \(\phi\) vanishes on every cycle in connected \(U\), then \(\phi\) is a coboundary on \(U\).

## Status

This is the next theorem-level closure target after local cycle-vanishing.

## Dependencies discharged by this theorem

1. Input to rooted-ball trivialization.
2. Input to local-type equality in the Newstein chain.
3. Completion of the rooted-ball cocycle-trivialization branch.
