# Gravitational Constant Input — 2026-05-29

Status: `PHYSICAL_CONSTANT_INPUT_ONLY_NO_NEW_G_MEASUREMENT`

This artifact introduces `GravitationalConstantInput`.

Dependency:

```text
SpacetimeFabricMetricInput
```

Constant:

```text
G = 6.67430e-11 m^3 kg^-1 s^-2
standard uncertainty = 0.00015e-11 m^3 kg^-1 s^-2
relative standard uncertainty = 2.2e-5
source = NIST CODATA Newtonian constant of gravitation
```

Newtonian role:

```text
F = G m_1 m_2 / r^2
```

Einstein-equation coupling role:

```text
G_{mu nu} + Lambda g_{mu nu} = (8 pi G / c^4) T_{mu nu}
```

Required objects:

```text
gravitationalConstantSymbolRecorded
codataValueRecorded
codataSourceRecorded
siUnitRecorded
standardUncertaintyRecorded
relativeUncertaintyRecorded
newtonianForceUseRecorded
einsteinCouplingUseRecorded
notFittedParameterBoundaryRecorded
noVaryingGClaimBoundaryRecorded
boundaryPreserved
```

Boundary:

```text
Physical-constant input only.
No new measurement of G.
No derivation of G.
No varying-G claim.
No time variation of G claim.
No spatial variation of G claim.
No quantum gravity proof.
No new gravity claim.
No standard GR failure claim.
No Lambda-CDM failure claim.
No dark matter replacement claim.
No empirical validation claim.
No independent replication claim.
No unrestricted Chronos-RR.
No unrestricted H4.1/FGL.
No P vs NP.
No Clay problem.
```

Next object:

```text
EinsteinCouplingConstantSlot
```
