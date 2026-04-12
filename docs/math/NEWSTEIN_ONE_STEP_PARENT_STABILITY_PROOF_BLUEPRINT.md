# Newstein One-Step Parent Stability Proof Blueprint

## Status
OPEN

## Target
Prove the Newstein One-Step Parent Stability Predicate.

## Input
Let \(T\subseteq B_R(v)\) be a rooted spanning tree of the rooted-local patch.
Let \(w\in B_R(v)\) be a non-root vertex, and let
\[
p=\operatorname{par}_T(w)
\]
be its parent in \(T\).

## Required output
Show that
\[
p\in B_R(v).
\]

## Minimal proof decomposition
1. Unfold the rooted-local admissibility predicate:
   \[
   \mathrm{Adm}_{v,R}(w)\iff w\in B_R(v).
   \]
2. Express the parent map as one-step motion toward the root in the rooted spanning tree.
3. Use monotonicity of rooted distance under parent iteration:
   \[
   d(v,\operatorname{par}_T(w)) \le d(v,w).
   \]
4. Combine with
   \[
   d(v,w)\le R
   \]
   to conclude
   \[
   d(v,\operatorname{par}_T(w))\le R.
   \]
5. Conclude
   \[
   \operatorname{par}_T(w)\in B_R(v).
   \]

## Weakest missing sublemma
Rooted distance is nonincreasing under one-step parent iteration in the rooted spanning tree.

## Finish condition
This file is replaceable by a proof exactly when the rooted-distance monotonicity sublemma is discharged.
