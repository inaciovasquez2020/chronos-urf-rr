# Newstein Parent-Iteration Closure Sublemma

## Status
OPEN

## Statement
Let \(T\subseteq B_R(v)\) be a rooted spanning tree of the rooted-local patch.
If \(w\in B_R(v)\) is not the root of its tree component and \(\operatorname{par}_T(w)\) is its parent in \(T\), then
\[
\operatorname{par}_T(w)\in B_R(v).
\]

## Role
This is the atomic closure step underlying ancestor-descent closure.

## Consequence
Induction on parent iteration yields ancestor-descent closure, which yields LCA interpolation closure, which yields geodesic interpolation closure.
