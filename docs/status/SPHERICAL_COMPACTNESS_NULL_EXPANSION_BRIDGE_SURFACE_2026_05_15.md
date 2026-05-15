# Spherical Compactness to Null-Expansion Bridge Surface

Status: CONDITIONAL_RESTRICTED_SPHERICAL_BRIDGE_SURFACE

## Scope

This status object records only the conditional restricted spherical bridge interface from compactness threshold to null-expansion signs.

The bridge input explicitly carries:

`SphericalCollapseGate thresholdInput -> FutureOuterMarginalSphericalSurface expansionInput`

The closed repository-native consequences are:

`SphericalCompactnessToNullExpansionBridge B`

and

`SphericalCollapseGate B.thresholdInput -> TrappedOrMarginalByNullExpansions B.expansionInput`

## Lean target

`Chronos.Frontier.SphericalCompactnessNullExpansionBridgeSurface`

Closed theorems:

`spherical_compactness_threshold_implies_outer_marginal_by_bridge`

`spherical_compactness_threshold_implies_trapped_or_marginal_by_bridge`

## Boundary

Conditional restricted spherical bridge interface only.

Does not prove:

- geometric threshold-to-null-expansion theorem
- nonspherical collapse exclusion
- Cosmic Censorship
- Hoop Conjecture
- unrestricted UniversalBoundaryCompactness
- unrestricted Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay-problem closure

## Next target

Replace the explicit bridge witness with a geometric spherical Einstein-matter lemma deriving the null-expansion signs from the Misner-Sharp compactness threshold.
