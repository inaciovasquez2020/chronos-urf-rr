# Newstein Local Coboundary Criterion

## Status
Conditional target.

## Lemma
Let \(U\subseteq B_n\) be a connected radius-\(r\) ball, and let \(\phi_H:E(U)\to \mathbb F_2\) be the restriction of the twisted \(2\)-lift cocycle.

Assume
\[
\phi_H(C)=0
\quad\text{for every cycle } C \subseteq U.
\]

Then there exists a function \(f:V(U)\to \mathbb F_2\) such that
\[
\phi_H(uv)=f(u)+f(v)
\quad\text{for every edge }uv\in E(U).
\]

Equivalently,
\[
\phi_H|_U=\delta f.
\]

Therefore the twisted and trivial \(2\)-lifts are isomorphic over \(U\).

## Consequence
The local coboundary criterion implies rooted-ball trivialization.

## Remaining proof obligations
1. choose a root vertex in \(U\);
2. define \(f(x)\) by path integration of \(\phi_H\) from the root to \(x\);
3. prove path-independence from the cycle-vanishing hypothesis;
4. verify \(\phi_H=\delta f\) on every edge.

## Overclaim guard
No proof of the lemma is claimed here.
