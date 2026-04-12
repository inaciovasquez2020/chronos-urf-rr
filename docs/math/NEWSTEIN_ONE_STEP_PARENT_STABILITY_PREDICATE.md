# Newstein One-Step Parent Stability Predicate

## Status
OPEN

## Statement
Let \(T\subseteq B_R(v)\) be a rooted spanning tree of the rooted-local patch.
Define the rooted-local admissibility predicate
\[
\mathrm{Adm}_{v,R}(w)
\]
by
\[
\mathrm{Adm}_{v,R}(w)\iff w\in B_R(v).
\]

The one-step parent stability predicate is:
for every non-root vertex \(w\) in the rooted tree component of \(T\), if
\[
\mathrm{Adm}_{v,R}(w),
\]
then
\[
\mathrm{Adm}_{v,R}(\operatorname{par}_T(w)).
\]

Equivalently,
\[
w\in B_R(v)\Longrightarrow \operatorname{par}_T(w)\in B_R(v).
\]

## Role
This is the atomic predicate required to discharge the Newstein Parent-Iteration Closure Sublemma.

## Consequence
Once proved, it promotes directly to parent-iteration closure, and hence to ancestor-descent closure.
