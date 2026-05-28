# Empty Active Detector Default Policy — 2026-05-28

Status: `SOLVED_RESTRICTED_EMPTY_ACTIVE_DETECTOR_DEFAULT_POLICY_ONLY`.

This package closes the empty-active-detector branch for the restricted finite-detector gravity bridge.

## Dependency

- `COMPUTED_ACTIVE_RADIUS_MINIMUM_2026_05_28`
- `RESTRICTED_QL_FINITE_DETECTOR_MASS_RADIUS_EXTRACTION_2026_05_28`
- `RESTRICTED_QL_MASS_RADIUS_GATE_MONOTONICITY_2026_05_28`

## Proved Lean objects

- `defaultActiveRadiusFloor`
- `defaultActiveRadiusFloor_eq_computed_of_nonempty`
- `defaultActiveRadiusFloor_eq_zero_of_empty`
- `activeRadiusValues_empty_of_no_active`
- `activeMass_eq_zero_of_no_active`
- `defaultActiveRadiusFloor_eq_zero_of_no_active`
- `finiteDetectorExtraction_gate_of_default_floor_le_mass`
- `finiteDetectorExtraction_no_active_default_gate`

## Content

The default active-radius floor is total:

1. if active-radius values are nonempty, it is the computed finite minimum;
2. if active-radius values are empty, it is zero.

The module also proves that if no detector is active, then active mass is zero and the default active-radius floor is zero. Therefore the restricted finite-detector extraction gate holds in the no-active-detector case.

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

- `PhysicalDetectorFieldExtractionMap`
- `RestrictedEinsteinMatterDataToFiniteDetectorField`
- `TrappedSurfaceFormationFromRestrictedGate`
- `PDEConstraintPropagationForRestrictedCollapseDomain`
