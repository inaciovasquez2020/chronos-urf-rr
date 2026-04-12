# Newstein Rooted-Distance Monotonicity Proof Blueprint

## Status
OPEN

## Target
Prove the Newstein Rooted-Distance Monotonicity Sublemma.

## Input
Let \(T\subseteq B_R(v)\) be a rooted spanning tree.
Let \(w\) be a non-root vertex and
\[
p=\operatorname{par}_T(w)
\]
its parent.

## Required output
Show that
\[
d(v,p)\le d(v,w).
\]

## Minimal proof decomposition
1. Use the rooted spanning-tree structure to express the unique tree path from \(v\) to \(w\).
2. Identify \(p\) as the penultimate vertex on that rooted path.
3. Show that the rooted path to \(p\) is an initial segment of the rooted path to \(w\).
4. Deduce
   \[
   d(v,w)=d(v,p)+1
   \]
   in tree distance.
5. Conclude
   \[
   d(v,p)\le d(v,w).
   \]

## Weakest missing sublemma
Parent edges decrease rooted tree depth by exactly one.

## Finish condition
This file is replaceable by a proof exactly when rooted tree depth decrement is discharged.
