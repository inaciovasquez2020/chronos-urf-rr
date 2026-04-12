# Newstein Geodesic Interpolation Closure Sublemma

## Status
OPEN

## Statement
Let \(G\) be a bounded-degree graph, let \(v\) be a root vertex, let \(B_r(v)\subseteq B_R(v)\) with \(r\le R\), and let
\[
T \subseteq B_R(v)
\]
be a rooted spanning tree of the induced rooted-local patch.

Assume the rooted-local regime is tree-convex inside \(B_R(v)\), i.e.
for every \(x,y\in B_r(v)\), every vertex on the unique tree path \(P_T(x,y)\) lies in \(B_R(v)\).

Then for every non-tree edge
\[
e=\{x,y\}\in E(B_r(v))\setminus E(T),
\]
the fundamental cycle
\[
C_e=P_T(x,y)\cup\{e\}
\]
is contained in \(B_R(v)\).

## Role
This is the weakest sufficient closure statement needed to promote tree-path rooted-locality.

## Consequence
Once proved, the rooted-locality step in the Newstein fundamental-cycle generation chain is discharged.
