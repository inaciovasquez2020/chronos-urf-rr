# Finite Sink Quadratic Relaxation Theorem

Status: `FINITE_RESTRICTED_THEOREM_SOLVED`

## Closed object

For every finite integer domain `S : Finset Int` containing `0`, the sink relaxation

```lean
sinkRelax x = 0
with quadratic entropy
quadraticEntropy x = Int.natAbs x * Int.natAbs x
has:
closure under relaxation
entropy production nonnegativity
entropy monotonicity
The closed Lean certificate is:
finite_sink_quadratic_relaxation_certificate
The concrete /tmp model
{-2,-1,0,1,2}
is represented by:
concrete_symmetric_domain_certificate
Boundary
Finite sink-quadratic relaxation theorem only.
Does not prove:
existence of UniformTemporalRelaxationWave
construction of unrestricted admissible domains
entropy production for arbitrary entropy functions
entropy monotonicity for arbitrary entropy functions
unrestricted admissible dissipation
unrestricted rate-thick coercivity
unrestricted UniversalFiberEntropyGap
unrestricted Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay problem
