# Spherical Null Expansion Criterion Surface

Status: RESTRICTED_SPHERICAL_NULL_EXPANSION_SURFACE

## Scope

This status object records only the restricted spherical null-expansion criterion surface.

The repository-native predicates are:

`FutureTrappedSphericalSurface(S) := S.outgoingExpansion < 0 and S.ingoingExpansion < 0`

`FutureOuterMarginalSphericalSurface(S) := S.outgoingExpansion <= 0 and S.ingoingExpansion < 0`

`TrappedOrMarginalByNullExpansions(S) := FutureTrappedSphericalSurface(S) or FutureOuterMarginalSphericalSurface(S)`

## Lean target

`Chronos.Frontier.SphericalNullExpansionCriterionSurface`

Closed theorems:

`trapped_spherical_null_expansions_imply_trapped_or_marginal`

`marginal_spherical_null_expansions_imply_trapped_or_marginal`

## Boundary

Restricted spherical null-expansion criterion surface only.

Does not prove:

- compactness-threshold-to-null-expansion bridge
- nonspherical collapse exclusion
- Cosmic Censorship
- Hoop Conjecture
- unrestricted UniversalBoundaryCompactness
- unrestricted Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay-problem closure

## Next target

Bridge the spherical compactness threshold

`arealRadius <= 2 * misnerSharpMass`

to the null-expansion condition

`outgoingExpansion <= 0 and ingoingExpansion < 0`

as a separate restricted spherical bridge surface.
