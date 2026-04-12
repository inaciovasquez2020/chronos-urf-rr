# Newstein Ancestor-Descent Closure Sublemma

## Status
OPEN

## Statement
Let \(T\subseteq B_R(v)\) be a rooted spanning tree of the rooted-local patch.
Let \(u,w\) be vertices in the same rooted tree component with \(u\) an ancestor of \(w\).

Assume \(u,w\in B_R(v)\) and the rooted-local patch is stable under parent iteration.
Then every vertex on the ancestor-descent path
\[
P_T(u,w)
\]
lies in \(B_R(v)\).

## Role
This is the weakest sufficient missing sublemma for LCA interpolation closure.

## Consequence
Once proved, least-common-ancestor interpolation closure follows by decomposition into two ancestor-descent segments.
