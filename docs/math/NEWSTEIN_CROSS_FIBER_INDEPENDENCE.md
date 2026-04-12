# Newstein Cross-Fiber Independence

## Target statement

For distinct fibers \(u \neq v\),
\[
\operatorname{im}(\iota_u)\cap \operatorname{im}(\iota_v)=0
\]
inside the corresponding global quotient.

## Inputs

### 1. Fiber-to-global injectivity

Assume each fiber quotient injects into the global quotient.

### 2. Fiber decomposition

Assume distinct fibers are supported on distinct lifted torus components, joined only through connector structure external to the fiber quotient generators.

## Required subclaims

### 1. Disjoint fiber support at the quotient-generator level

Prove nonzero quotient generators from distinct fibers cannot be represented by the same fiber-supported cycle.

### 2. Connector edges do not identify fiber classes

Prove connector-edge relations do not produce quotient identifications between nonzero classes coming from different fibers.

### 3. Mixed local-ball relations do not collapse distinct fiber classes

Prove sums of local-ball cycle classes cannot transform a nonzero class from fiber \(u\) into a nonzero class from fiber \(v\) when \(u\neq v\).

### 4. Zero-intersection criterion

Prove that if
\[
\iota_u([\alpha])=\iota_v([\beta]),
\]
then both classes vanish.

## Deduction

Assume
\[
\iota_u([\alpha])=\iota_v([\beta]).
\]

Then
\[
\iota_u([\alpha])+\iota_v([\beta])=0
\]
in the global quotient.

By 1–3, no nontrivial quotient relation identifies distinct nonzero fiber classes across different fibers.

Hence
\[
[\alpha]=0
\quad\text{and}\quad
[\beta]=0.
\]

Therefore
\[
\operatorname{im}(\iota_u)\cap \operatorname{im}(\iota_v)=0.
\]

## Assembly theorem

Distinct fiber images are independent in the global quotient.

## Status

This is the second theorem-level target in the fiber-to-global branch.

## Dependencies discharged by this theorem

1. Input to the direct-sum embedding theorem.
2. Input to the global quotient-gap theorem.
3. Separation of per-fiber contributions in the Newstein assembly.
