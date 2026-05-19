# Finite Rational Sink Quadratic Relaxation Theorem

Status: `FINITE_RATIONAL_RESTRICTED_THEOREM_SOLVED`

## Closed object

For every finite rational domain `S : Finset Rat` containing `0`, the sink relaxation

```lean
rationalSinkRelax x = 0
with rational quadratic entropy
rationalQuadraticEntropy x = x * x
has:
closure under relaxation
entropy production nonnegativity
entropy monotonicity
The closed Lean certificate is:
finite_rational_sink_quadratic_relaxation_certificate
The concrete rational symmetric domain
{-2,-1,0,1,2}
is represented by:
concrete_rational_symmetric_domain_certificate
Relation to PR #411
This extends the finite sink-quadratic relaxation theorem from finite integer domains to finite rational domains.
Boundary
Finite rational sink-quadratic relaxation theorem only.
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
