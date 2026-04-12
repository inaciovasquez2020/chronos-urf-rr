# Newstein Parent-Iteration Closure Proof Blueprint

## Status
OPEN

## Target
Prove the Newstein Parent-Iteration Closure Sublemma.

## Input
Let \(T\subseteq B_R(v)\) be a rooted spanning tree of the rooted-local patch.
Let \(w\in B_R(v)\) be a non-root vertex of its tree component, and let
\[
p=\operatorname{par}_T(w)
\]
be its parent.

## Required output
Show that
\[
p\in B_R(v).
\]

## Minimal proof decomposition
1. Express \(w\in B_R(v)\) by a rooted-local admissibility predicate.
2. Identify the parent map \(\operatorname{par}_T\) as one-step rooted descent toward the root.
3. Prove that the rooted-local admissibility predicate is closed under one-step parent iteration.
4. Conclude that
\[
\operatorname{par}_T(w)\in B_R(v).
\]

## Weakest missing sublemma
The rooted-local admissibility predicate is stable under one-step parent iteration in the rooted spanning tree.

## Finish condition
This file is replaceable by a proof exactly when one-step parent stability is discharged.
