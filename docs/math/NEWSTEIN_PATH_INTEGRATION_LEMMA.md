# Newstein Path-Integration Lemma

## Status
Conditional target.

## Lemma
Let \(U\subseteq B_n\) be a connected graph, let \(x_0\in V(U)\), and let \(\phi:E(U)\to\mathbb F_2\).

Assume
\[
\phi(C)=0
\quad\text{for every cycle }C\subseteq U.
\]

For each \(x\in V(U)\), define
\[
f(x):=\sum_{e\in P_{x_0,x}} \phi(e)\in \mathbb F_2,
\]
where \(P_{x_0,x}\) is any path from \(x_0\) to \(x\).

Then:

1. \(f\) is well-defined;
2. for every edge \(uv\in E(U)\),
   \[
   \phi(uv)=f(u)+f(v).
   \]

Equivalently,
\[
\phi=\delta f.
\]

## Consequence
The path-integration lemma implies the Newstein local coboundary criterion.

## Remaining proof obligations
1. show two paths from \(x_0\) to \(x\) differ by a cycle;
2. use cycle-vanishing to prove path-independence of \(f(x)\);
3. compare the two root-to-endpoint paths obtained by appending the edge \(uv\).

## Overclaim guard
No proof of the lemma is claimed here.
