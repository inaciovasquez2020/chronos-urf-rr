# Newstein Tree-Path Rooted-Locality Proof Blueprint

## Status
OPEN

## Target
Prove the Newstein Tree-Path Rooted-Locality Sublemma.

## Input
Let \(B_R(v)\) be a rooted radius-\(R\) ball in a bounded-degree graph.
Let
\[
T \subseteq B_R(v)
\]
be a rooted spanning forest.
Let
\[
e=\{x,y\}\in E(B_R(v))\setminus E(T)
\]
be a non-tree edge.

## Required output
Show that the unique tree path
\[
P_T(x,y)\subseteq T
\]
stays inside the rooted-local radius regime defining the Newstein generating family.

## Minimal proof decomposition
1. Use \(x,y\in B_R(v)\) to bound their rooted distance from \(v\).
2. Use connectedness of the tree component of \(T\) containing \(x\) and \(y\).
3. Show uniqueness of the path \(P_T(x,y)\).
4. Express every vertex of \(P_T(x,y)\) as lying on a rooted geodesic envelope controlled by \(R\).
5. Prove every edge of \(P_T(x,y)\) remains in the same rooted-local support class.
6. Conclude that
\[
C_e=P_T(x,y)\cup\{e\}
\]
is rooted-local.

## Weakest missing sublemma
The rooted-local regime is closed under tree geodesic interpolation inside \(B_R(v)\).

## Finish condition
This file is replaceable by a proof exactly when the geodesic-interpolation closure sublemma is discharged.
