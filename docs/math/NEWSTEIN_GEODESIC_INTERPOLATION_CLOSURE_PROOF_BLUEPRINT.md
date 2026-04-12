# Newstein Geodesic Interpolation Closure Proof Blueprint

## Status
OPEN

## Target
Prove the Newstein Geodesic Interpolation Closure Sublemma.

## Input
Let \(v\) be a root vertex.
Let \(x,y\in B_r(v)\).
Let \(T\subseteq B_R(v)\) be a rooted spanning tree of the rooted-local patch.

## Required output
Show that every vertex of the unique tree path
\[
P_T(x,y)
\]
lies in \(B_R(v)\).

## Minimal proof decomposition
1. Prove uniqueness of \(P_T(x,y)\) in \(T\).
2. Parameterize vertices of \(P_T(x,y)\) by tree distance from \(x\).
3. Use rooted tree ancestry to show every path vertex lies below the least common ancestor of \(x\) and \(y\).
4. Bound rooted distance of every path vertex by the maximum rooted distance of \(x\) and \(y\), plus the local tree-convexity allowance.
5. Deduce
\[
P_T(x,y)\subseteq B_R(v).
\]
6. Conclude that every local fundamental cycle determined by a non-tree edge stays inside \(B_R(v)\).

## Weakest missing sublemma
The rooted-local patch is closed under least-common-ancestor interpolation in the rooted spanning tree.

## Finish condition
This file is replaceable by a proof exactly when the least-common-ancestor interpolation sublemma is discharged.
