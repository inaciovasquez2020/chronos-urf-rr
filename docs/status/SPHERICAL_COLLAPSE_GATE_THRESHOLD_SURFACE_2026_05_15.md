# Spherical Collapse Gate Threshold Surface

Status: RESTRICTED_SPHERICAL_THRESHOLD_SURFACE

## Scope

This status object records only the restricted spherical compactness-threshold surface.

The repository-native spherical gate is:

`SphericalCollapseGate(S) := S.arealRadius <= 2 * S.misnerSharpMass`

The repository-native trapped-or-marginal spherical surface predicate is:

`TrappedOrMarginalSphericalSurface(S) := S.arealRadius <= 2 * S.misnerSharpMass`

Therefore the Lean theorem closes the definitional implication:

`SphericalCollapseGate(S) -> TrappedOrMarginalSphericalSurface(S)`

## Lean target

`Chronos.Frontier.SphericalCollapseGateThresholdSurface`

Closed theorem:

`spherical_collapse_gate_implies_trapped_or_marginal_surface`

## Boundary

Restricted spherical threshold surface only.

Does not prove:

- nonspherical collapse exclusion
- Cosmic Censorship
- Hoop Conjecture
- unrestricted UniversalBoundaryCompactness
- unrestricted Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay-problem closure

## Next target

Replace this definitional spherical threshold surface with a geometric spherical model layer using Misner-Sharp mass, areal radius, and null-expansion signs.
