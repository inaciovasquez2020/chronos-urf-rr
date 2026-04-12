# Newstein Ancestor-Descent Closure Proof Blueprint

## Status
OPEN

## Target
Prove the Newstein Ancestor-Descent Closure Sublemma.

## Input
Let \(u\) be an ancestor of \(w\) in the rooted spanning tree \(T\subseteq B_R(v)\).

## Required output
Show that every vertex on the unique tree path
\[
P_T(u,w)
\]
lies in \(B_R(v)\).

## Minimal proof decomposition
1. Parameterize the path \(P_T(u,w)\) by repeated parent iteration from \(w\) upward to \(u\).
2. Prove each intermediate parent remains in the rooted-local patch.
3. Use induction on tree depth difference \(d_T(u,w)\).
4. Conclude pathwise closure inside \(B_R(v)\).

## Weakest missing sublemma
The rooted-local patch is closed under one-step parent iteration.

## Finish condition
This file is replaceable by a proof exactly when one-step parent closure is discharged.
