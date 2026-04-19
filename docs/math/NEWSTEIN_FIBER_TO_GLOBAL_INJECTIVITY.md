# Newstein Fiber-to-Global Injectivity and Direct-Sum Independence

Status: OPEN

## Statement
For each fiber \(v\), prove the inclusion-induced map
\[
\iota_v^{\mathrm{triv}}:
Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}
\to
Q(G_n)
\]
is injective, and likewise
\[
\iota_v^{\mathrm{tw}}:
Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}
\to
Q(H_n)
\]
is injective, where
\[
Q(G):=
Z_1(G)\Big/\Big\langle Z_1(B_r^G(x)):x\in V(G)\Big\rangle.
\]

For distinct fibers \(u\neq v\), prove
\[
\operatorname{im}(\iota_u)\cap \operatorname{im}(\iota_v)=0.
\]

Deduce
\[
\bigoplus_v Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}
\hookrightarrow Q(G_n),
\qquad
\bigoplus_v Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}
\hookrightarrow Q(H_n).
\]

## Required inputs
1. No local-ball relation kills a nonzero fiber quotient class.
2. Connector edges do not create quotient identifications between different fibers.
3. Direct-sum embedding follows from fiberwise injectivity and cross-fiber independence.

## Role
This locks items III.1, III.2, and III.3 in `docs/math/NEWSTEIN_REMAINING_THEOREM_LEVEL_OBLIGATIONS.md`.

## Finish condition
Replace this file by a proof sufficient to feed the quotient-gap theorem.
