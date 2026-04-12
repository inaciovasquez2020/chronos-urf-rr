# Newstein Parent Depth Decrement Sublemma

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(v\).
For every non-root vertex \(w\) with parent
\[
p=\operatorname{par}_T(w),
\]
the rooted tree depth satisfies
\[
\operatorname{depth}_T(p)=\operatorname{depth}_T(w)-1.
\]

## Role
This is the atomic tree-theoretic fact required to prove rooted-distance monotonicity.

## Consequence
Combined with depth-distance identification in rooted trees, it yields
\[
d(v,p)\le d(v,w).
\]
