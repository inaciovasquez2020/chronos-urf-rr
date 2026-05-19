# Uniform Temporal Relaxation Wave Target

Status: `FRONTIER_OPEN`

## Target isolated

This adds the unrestricted theorem target:

```lean
def UniformTemporalRelaxationWaveExistenceTarget : Prop :=
  ∀ D : TemporalRelaxationWaveData, UniformTemporalRelaxationWave D
It also adds the no-promotion bridge:
theorem uniformTemporalRelaxationWave_from_input
    (h : UniformTemporalRelaxationWaveExistenceTarget) :
    UniformTemporalRelaxationWaveExistenceTarget :=
  h
Boundary
Target isolation only.
Does not prove:
existence of UniformTemporalRelaxationWave
UniformTemporalRelaxationWaveExistenceTarget
construction of unrestricted admissible domains
finite-to-unrestricted relaxation lift
entropy production for arbitrary entropy functions
entropy monotonicity for arbitrary entropy functions
unrestricted admissible dissipation
unrestricted rate-thick coercivity
unrestricted UniversalFiberEntropyGap
unrestricted Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay problem
