# Restricted QL Mass-Radius Gate Monotonicity — 2026-05-28

Status: `SOLVED_RESTRICTED_LOCAL_ARITHMETIC_GATE_ONLY`.

This package proves one small restricted gravity certificate step.

## Proved Lean objects

- `restrictedQLCollapseGate_mono_massRadius`
- `restrictedQLCollapseGate_zero_mass_rigid`

## Content

Inside a finite restricted quasi-local mass-radius gate model, define the local collapse-gate flag by:

    concentrationRadius <= massRadius

Then:

1. If the gate is active, increasing the available mass-radius budget preserves the gate.
2. If the mass-radius budget is zero and the gate is active, then the concentration radius is zero.

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

- `PhysicalMassRadiusExtractionMap`
- `RestrictedEinsteinMatterDataToMassRadiusSample`
- `TrappedSurfaceFormationFromRestrictedGate`
- `PDEConstraintPropagationForRestrictedCollapseDomain`
