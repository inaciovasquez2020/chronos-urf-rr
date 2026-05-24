# Newstein R1/R2/R3 Native Binding Specification

Status: OPEN_SPECIFICATION_REQUIRED.

## Purpose

This document must define the repository-native mathematical objects that instantiate:

- `R1SemanticData`
- `R2SemanticData`
- `R3SemanticData`

from `Chronos.Frontier.R1R2R3SemanticTheoremProofTargets`.

Until this specification is completed, R1/R2/R3 remain open theorem-level inputs.

## R1 Native Binding: Long-Chord Exclusion

Required theorem:

\[
\forall i\in\{1,2\},\ \forall w\in W^{\text{triv}},\ e_i\notin \text{supp}(w).
\]

Required native definitions:

1. `Word`
2. `Edge`
3. `Face`
4. `e_1`
5. `e_2`
6. `W^{\text{triv}}`
7. `\Phi_2^{\text{triv}}`
8. `\partial\tau`
9. `\text{supp}(w)`
10. native proof that every trivial word avoids both long chords

Missing until supplied:

- definition of `W^{\text{triv}}`
- definition of `\text{supp}(w)`
- identification of long chords `e_1,e_2`
- proof that trivial 2-face boundaries avoid long chords
- proof that trivial word support comes from trivial face boundaries

## R2 Native Binding: Diameter-Separation Filling Obstruction

Required theorem:

\[
u\neq v\land \partial S=c_u-c_v
\Rightarrow
\text{diam}(supp(S))>L.
\]

Required native definitions:

1. `Fiber`
2. `\text{FiberClass}`
3. `\text{TwoChain}`
4. `Boundary`
5. `c_u`
6. `c_v`
7. `supp(S)`
8. `\text{diam}`
9. `L`
10. native proof that distinct nonzero fiber classes remain globally separated

Missing until supplied:

- definition of fiber classes
- definition of global quotient placement
- definition of bounded two-chain
- definition of \text{diam}eter on support
- proof that bounded fillings cannot join distinct fibers

## R3 Native Binding: Uniform Local-Type Capacity

Required theorem:

\[
Q\text{ factors through bounded }(r,k,\Delta)\text{-local type}
\Rightarrow
\dim_{\mathbb F_2}(Z_1/W^{glob})\le C(r,k,\Delta).
\]

Required native definitions:

1. `QuotientData`
2. `Q`
3. `Z₁`
4. `W^{glob}`
5. `\text{LocalType}(r, k, \Delta)`
6. `FactorsThroughBoundedLocalType`
7. `C(r, k, \Delta)`
8. native proof of the uniform dimension bound

Missing until supplied:

- definition of quotient data
- definition of bounded local type
- definition of the factorization relation
- explicit function `C(r, k, \Delta)`
- proof that local-type factorization bounds quotient dimension

## Promotion Rule

No promotion to:

- `NON_FACTORISATION`
- `ChronosRRPromotionAllowed`
- `H41FGLPromotionAllowed`

is admissible until the native R1/R2/R3 binding is supplied and theorem-proved.

## Boundary

This document does not prove:

- LongChordExclusion
- DiameterSeparationFillingObstruction
- UniformLocalTypeCapacity
- NON_FACTORISATION
- Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem


## Verifier Token Anchors

- `e_1, e_2`
- `Z_1 / W^{\text{glob}}`
