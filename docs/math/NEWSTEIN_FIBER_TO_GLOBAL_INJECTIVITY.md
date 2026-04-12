# Newstein Fiber-to-Global Injectivity

## Target statement

For each fiber \(v\), the inclusion-induced maps
\[
\iota_v^{\mathrm{triv}}:
Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}
\to
Q(G_n)
\]
and
\[
\iota_v^{\mathrm{tw}}:
Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}
\to
Q(H_n)
\]
are injective, where
\[
Q(G):=
Z_1(G)\Big/\Big\langle Z_1(B_r^G(x)):x\in V(G)\Big\rangle.
\]

## Required subclaims

### 1. Fiber support survives local-ball quotienting

Prove no nonzero fiber quotient class is killed by a sum of local-ball cycle classes.

### 2. Local-ball relations remain locally generated

Prove every generator of
\[
\Big\langle Z_1(B_r^G(x)):x\in V(G)\Big\rangle
\]
is supported inside a rooted radius-\(r\) ball.

### 3. Fiber quotient classes are globally nonlocal

Prove every nonzero class in
\[
Z_1(\widetilde T_v)/W_v
\]
has nontrivial image modulo the local-ball span.

### 4. Inclusion descends to quotient

Prove the fiber inclusion map sends \(W_v\) into the local-ball quotient kernel, so the induced map on
\[
Z_1(\widetilde T_v)/W_v
\]
is well-defined.

## Deduction

Let \([\alpha]\in Z_1(\widetilde T_v)/W_v\) map to zero in the global quotient.

Then \(\alpha\) lies in the span of local-ball cycle classes.

By 1 and 3, this implies \([\alpha]=0\) already in the fiber quotient.

Hence the induced map is injective.

The same argument applies in both the trivial and twisted cover cases.

## Assembly theorem

For every fiber \(v\), the fiber quotient injects into the corresponding global quotient.

## Status

This is the first theorem-level target in the fiber-to-global branch.

## Dependencies discharged by this theorem

1. Input to cross-fiber independence.
2. Input to the direct-sum embedding theorem.
3. Input to global quotient-gap assembly.
