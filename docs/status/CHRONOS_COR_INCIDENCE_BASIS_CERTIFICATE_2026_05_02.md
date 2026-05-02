# Chronos COR Incidence-Basis Certificate — 2026-05-02

Status: FINITE INCIDENCE-BASIS CERTIFICATE / THEOREM ASSUMPTION SURFACE

## Object

This upgrades the Chronos COR certificate surface from arithmetic-only checking to finite raw graph checking.

The certificate records:

- vertices by count,
- edge list,
- field \(\mathbb F_2\),
- radius \(R\),
- cycle-basis vectors,
- local-cycle-basis vectors,
- certified cycle-space dimension,
- certified local-cycle-subspace rank,
- certified obstruction rank.

## Checked Finite Claims

The verifier computes the incidence boundary map

\[
\partial:C_1(G)\to C_0(G)
\]

from the raw edge list and verifies:

\[
\partial z=0
\]

for every declared cycle-basis vector.

It computes

\[
\dim Z_1(G)=|E(G)|-\operatorname{rank}_{\mathbb F_2}(\partial)
\]

and verifies that the declared cycle basis has exactly this rank.

It computes the radius-\(R\) local-cycle generators from graph balls and verifies:

\[
\operatorname{rank}_{\mathbb F_2}(L_R(G))
\]

against the declared local-cycle-subspace rank.

Finally it verifies:

\[
\operatorname{COR}_R(G)
=
\dim Z_1(G)-\operatorname{rank}_{\mathbb F_2}(L_R(G)).
\]

## Boundary

This verifies one finite incidence-basis certificate only.

It does not prove the finite-to-general lift.

It does not prove the locality-to-depth bridge.

It does not prove theorem-level Chronos closure.

## Weakest Next Lemma

The next theorem-level bridge is a family certificate:

\[
\forall n\ge n_0,\quad
\operatorname{COR}_R(G_n)\ge \alpha |V(G_n)|.
\]

