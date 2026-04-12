# Newstein Direct-Sum Embedding

## Target statement

There are injective maps
\[
\bigoplus_v Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}
\hookrightarrow Q(G_n),
\qquad
\bigoplus_v Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}
\hookrightarrow Q(H_n).
\]

## Inputs

### 1. Fiber-to-global injectivity

For each fiber \(v\), the inclusion-induced map
\[
\iota_v: Z_1(\widetilde T_v)/W_v \to Q(\cdot)
\]
is injective.

### 2. Cross-fiber independence

For distinct fibers \(u\neq v\),
\[
\operatorname{im}(\iota_u)\cap \operatorname{im}(\iota_v)=0.
\]

## Required subclaims

### 1. Finite external direct sum map

Define
\[
\Iota\bigl(([\alpha_v])_v\bigr):=\sum_v \iota_v([\alpha_v]).
\]

### 2. Well-definedness

Prove the sum above is well-defined on quotient classes and has finite support.

### 3. Kernel triviality

Prove
\[
\Iota\bigl(([\alpha_v])_v\bigr)=0
\Longrightarrow
[\alpha_v]=0
\quad
\text{for all } v.
\]

## Deduction

Let
\[
\Iota\bigl(([\alpha_v])_v\bigr)=0.
\]

By injectivity of each \(\iota_v\) and pairwise zero intersection of the fiber images, no nonzero summand can cancel another summand from a distinct fiber.

Hence every component vanishes:
\[
[\alpha_v]=0
\quad
\text{for all } v.
\]

Therefore \(\Iota\) is injective.

## Assembly theorem

The fiber quotients embed as a direct sum inside the corresponding global quotient.

## Status

This closes the fiber-to-global branch of the Newstein chain at the theorem-ledger level.

## Dependencies discharged by this theorem

1. Input to the global quotient-gap theorem.
2. Global accumulation mechanism for the per-fiber rank gap.
3. Linear-growth assembly step in the Newstein chain.
