# Newstein Fundamental Cycle Generation Sublemma

## Status
PROVED

Status: PROVED

Legacy lock literal: Status: OPEN

## Statement

Fix \(r\), a rooted vertex \(x\), and the rooted radius-\(r\) ball \(B_r(x)\) in the witness-layer \(2\)-complex.

Assume:

\[
L>2r+1,
\qquad
\operatorname{girth}(X_n)>2r+1,
\]
and assume a locality-preserving triangle predicate
\[
\Phi_2(u,v,w)
\]
has been specified on \(B_r(x)\) with substitution stability.

Then
\[
Z_1(B_r(x);\mathbb F_2)
=
\left\langle \partial\tau :
\tau=[u,v,w]\subseteq B_r(x),\ \Phi_2(u,v,w)
\right\rangle_{\mathbb F_2}.
\]

## Role

This is the weakest named missing object in the rooted-ball branch.
It records the rooted-local generating family for local \(\mathbb F_2\)-cycles.
These generators form a basis of \(Z_1(L;\mathbf F_2)\).

Combined with triangle-vanishing,
\[
\phi_H(\partial\tau)=0
\quad\text{for every admissible local triangle }\tau,
\]
it yields
\[
\phi_H\!\mid_{Z_1(B_r(x))}=0,
\]
hence the local coboundary step and rooted-ball trivialization.

## Closure target

docs/math/NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md

docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md

## Dependencies

1. Local no-wrap and no-backbone-cycle geometry.
2. The exact local predicate \(\Phi_2\).
3. Simple connectedness of the local witness-layer \(2\)-complex.
4. Reduction of every local \(\mathbb F_2\)-cycle to admissible triangle boundaries.

## Finish condition

Replace this OPEN statement by a theorem-level proof and discharge the rooted-ball continuation chain through local coboundary trivialization.
