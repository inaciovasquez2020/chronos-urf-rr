# Newstein LCA Interpolation Closure Sublemma

## Status
OPEN

## Statement
Let \(G\) be a bounded-degree graph, let \(v\) be a root vertex, let \(B_r(v)\subseteq B_R(v)\), and let
\[
T \subseteq B_R(v)
\]
be a rooted spanning tree of the rooted-local patch.

For any \(x,y\in B_r(v)\) in the same tree component of \(T\), let
\[
a=\operatorname{LCA}_T(x,y)
\]
be their least common ancestor in \(T\).

Assume the rooted-local patch is closed under ancestor descent from \(a\) to \(x\) and from \(a\) to \(y\).
Then every vertex on the unique tree path
\[
P_T(x,y)
\]
lies in \(B_R(v)\).

Equivalently, the rooted-local patch is closed under least-common-ancestor interpolation.

## Role
This is the weakest sufficient missing sublemma for Newstein geodesic interpolation closure.

## Consequence
Once proved, the Newstein Geodesic Interpolation Closure Sublemma follows immediately.
