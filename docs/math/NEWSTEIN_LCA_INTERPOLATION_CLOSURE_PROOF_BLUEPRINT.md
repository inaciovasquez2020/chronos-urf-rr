# Newstein LCA Interpolation Closure Proof Blueprint

## Status
OPEN

## Target
Prove the Newstein LCA Interpolation Closure Sublemma.

## Input
Let \(x,y\in B_r(v)\) lie in the same rooted tree component of \(T\subseteq B_R(v)\).
Let \(a=\operatorname{LCA}_T(x,y)\).

## Required output
Show that every vertex on
\[
P_T(x,y)=P_T(a,x)\cup P_T(a,y)
\]
lies in \(B_R(v)\).

## Minimal proof decomposition
1. Define the rooted partial order induced by \(T\).
2. Prove existence and uniqueness of \(a=\operatorname{LCA}_T(x,y)\).
3. Decompose \(P_T(x,y)\) into the two ancestor-descent segments \(P_T(a,x)\) and \(P_T(a,y)\).
4. Prove closure of the rooted-local patch under ancestor descent.
5. Deduce that every vertex on \(P_T(a,x)\) and \(P_T(a,y)\) lies in \(B_R(v)\).
6. Conclude
\[
P_T(x,y)\subseteq B_R(v).
\]

## Weakest missing sublemma
The rooted-local patch is closed under ancestor descent in the rooted spanning tree.

## Finish condition
This file is replaceable by a proof exactly when ancestor-descent closure is discharged.
