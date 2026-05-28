# Restricted Physical Detector Field Extraction Map

**Status:** `CONDITIONAL_RESTRICTED_INTERFACE_BRIDGE_SOLVED`

## Theorem Surface

A restricted physical detector field is a finite detector-indexed profile with:

- natural-valued readings;
- natural-valued radii;
- Boolean active flags.

The extraction map sends this finite physical sampling profile to finite detector data:

\[
F
\mapsto
(\text{atoms},\text{activeMass},\text{radiusFloor}).
\]

The active detector family is exactly the finite set of detectors whose active flag is true.

The extracted active mass is the finite sum of the declared readings over the active detector family.

The extracted radius floor is the finite minimum of active radii when active radii exist, and zero otherwise.

## Corrected Boundary Admissibility

The earlier pointwise condition

\[
F.reading(d) \le F.radius(d)
\]

does not imply

\[
\sum_{d \in active} F.reading(d)
\le
\min_{d \in active} F.radius(d).
\]

The corrected admissibility predicate therefore carries the aggregate gate condition directly:

\[
extractedActiveMass(F) \le extractedRadiusFloor(F).
\]

This is represented as:

```lean
structure PhysicalDetectorFieldAdmissible
    (F : PhysicalDetectorField Detector) : Prop where
  gate_bound :
    RestrictedFiniteDetectorGate
      (extractedActiveMass F)
      (extractedRadiusFloor F)
Closed Theorems
physicalExtraction_activeSet_correct
physicalExtraction_atomMass_coherent
physicalExtraction_data_activeMass
physicalExtraction_data_radiusFloor
physicalExtraction_feeds_restrictedFiniteDetectorGate
Proof Meaning
The bridge theorem is now immediate because admissibility contains the exact aggregate gate invariant required by the finite detector gate.
This is intentional. The theorem does not pretend to derive a global aggregate bound from insufficient pointwise data. Instead, it isolates the precise boundary condition required for physical detector samples to enter the verified finite-detector accounting layer.
Research Novelty
The result identifies the correct admissibility boundary for the physical-to-finite detector bridge.
The finite detector layer had already shown that coherent finite extraction is forced by atomic mass data. This artifact supplies the upper interface: a finite physical sampling profile can be converted into the data shape required by that layer, provided the aggregate gate bound is admitted as a structural boundary invariant.
Obstruction Removed
The removed obstruction is the false local-to-global aggregation route.
Pointwise reading/radius bounds are insufficient. The corrected bridge replaces that false route with an exact aggregate admissibility condition.
Boundary
This artifact proves only a conditional restricted interface bridge.
It does not prove:
derivation of gate_bound from raw physical readings;
arbitrary physical detector fields are admissible;
physical detector-field extraction for continuum GR data;
Einstein-matter PDE well-posedness;
trapped-surface formation theorem;
black-hole formation theorem;
cosmic censorship proof;
hoop conjecture proof;
unrestricted QL_CollapseGate;
unrestricted UniversalBoundaryCompactness;
unrestricted Chronos-RR;
unrestricted H4.1/FGL;
P vs NP;
any Clay problem.
