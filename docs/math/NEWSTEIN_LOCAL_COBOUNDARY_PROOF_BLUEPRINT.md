# Newstein Local Coboundary Proof Blueprint

## Status
OPEN

## Target
Prove the Newstein Local Coboundary Criterion.

## Input
Let \(B_R(v)\) be a rooted radius-\(R\) ball in a bounded-degree graph.
Let \(\omega\) be a \(1\)-cocycle on \(B_R(v)\) supported on the rooted-local cycle sector.

Assume:
1. \(\omega\) has zero evaluation on every rooted-local cycle generator of \(H_1(B_R(v);\mathbb F_2)\).
2. \(\omega\) vanishes on every rooted boundary class entering the Newstein quotient.

## Required output
Construct a \(0\)-cochain \(f\) on \(B_R(v)\) such that
\[
\delta f = \omega.
\]

## Minimal proof decomposition
1. Choose a rooted spanning forest \(T \subseteq B_R(v)\).
2. Define \(f\) inductively on vertices along rooted tree paths in \(T\).
3. Show \(\delta f = \omega\) on every tree edge by construction.
4. Reduce every non-tree edge check to evaluation on the unique fundamental cycle determined by \(T\).
5. Use the zero-evaluation hypothesis on rooted-local cycle generators to show \(\delta f = \omega\) on every non-tree edge.
6. Use the boundary-vanishing hypothesis to eliminate quotient-boundary ambiguity.
7. Conclude \([\omega]=0 \in H^1(B_R(v);\mathbb F_2)\).

## Weakest missing sublemma
Every non-tree edge of \(B_R(v)\) determines a rooted-local fundamental cycle expressible in the generating family used by the Newstein quotient.

## Finish condition
This file is replaceable by a proof exactly when the weakest missing sublemma is discharged.
