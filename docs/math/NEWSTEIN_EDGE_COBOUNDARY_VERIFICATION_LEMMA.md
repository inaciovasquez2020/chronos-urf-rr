# Newstein Edge-Coboundary Verification Lemma

## Status
Conditional target.

## Lemma
Let \(U\) be a connected graph, let \(x_0\in V(U)\), let \(\phi:E(U)\to\mathbb F_2\), and define
\[
f(x):=\sum_{e\in P_{x_0,x}}\phi(e)\in\mathbb F_2
\]
using any path \(P_{x_0,x}\) from \(x_0\) to \(x\), assuming path-independence.

Then for every edge \(uv\in E(U)\),
\[
\phi(uv)=f(u)+f(v).
\]

Equivalently,
\[
\phi=\delta f.
\]

## Consequence
The edge-coboundary verification lemma supplies the final step in the Newstein path-integration lemma.

## Remaining proof obligations
1. choose a path \(P_{x_0,u}\) from \(x_0\) to \(u\);
2. extend it by the edge \(uv\) to a path from \(x_0\) to \(v\);
3. compare the two expressions for \(f(v)\);
4. rearrange in \(\mathbb F_2\).

## Overclaim guard
No proof of the lemma is claimed here.
