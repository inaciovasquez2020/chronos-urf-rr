# Computed Active Radius Minimum — 2026-05-28

Status: `SOLVED_RESTRICTED_COMPUTED_ACTIVE_RADIUS_MINIMUM_ONLY`.

This package solves the next finite-detector gravity bridge: replacing the supplied explicit `activeRadiusFloor` with a computed finite minimum over active detector radii.

## Dependency

- `RESTRICTED_QL_FINITE_DETECTOR_MASS_RADIUS_EXTRACTION_2026_05_28`
- `RESTRICTED_QL_MASS_RADIUS_GATE_MONOTONICITY_2026_05_28`

## Proved Lean objects

- `activeDetectors`
- `activeRadiusValues`
- `computedActiveRadiusMinimum`
- `active_radius_mem_values_of_active`
- `computedActiveRadiusMinimum_le_active_radius`
- `finiteDetectorExtraction_gate_of_computed_min_le_mass`
- `finiteDetectorExtraction_computed_min_gate_mono_mass`

## Content

For a finite detector type:

1. collect active detectors;
2. map them to radius values;
3. require a nonempty active-radius-values certificate;
4. compute the finite minimum by `Finset.min'`;
5. prove the computed minimum is below every active detector radius;
6. use the computed minimum as the radius floor in the restricted finite-detector extraction gate.

## Boundary

This does not prove:

- cosmic censorship proved
- hoop conjecture proved
- Einstein-matter PDE well-posedness
- trapped-surface formation theorem
- black-hole formation theorem
- unrestricted QL_CollapseGate
- unrestricted UniversalBoundaryCompactness
- unrestricted Chronos-RR proved
- unrestricted H4.1/FGL proved
- solves P vs NP
- Clay problem solved

## Next missing objects

- `EmptyActiveDetectorDefaultPolicy`
- `PhysicalDetectorFieldExtractionMap`
- `RestrictedEinsteinMatterDataToFiniteDetectorField`
- `TrappedSurfaceFormationFromRestrictedGate`
- `PDEConstraintPropagationForRestrictedCollapseDomain`
