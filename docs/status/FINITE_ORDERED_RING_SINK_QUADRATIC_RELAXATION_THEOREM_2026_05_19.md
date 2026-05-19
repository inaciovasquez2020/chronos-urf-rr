# Finite Ordered-Data Sink Quadratic Relaxation Theorem

Status: `FINITE_ORDERED_DATA_RESTRICTED_THEOREM_SOLVED`

## Closed object

For every finite domain `S : Finset α` over explicit quadratic sink order data `D : QuadraticSinkOrderData α`, if `S` contains `D.zero`, the sink relaxation

```lean
orderedRingSinkRelax D x = D.zero
with quadratic entropy
orderedRingQuadraticEntropy D x = D.mul x x
has:
closure under relaxation
entropy production nonnegativity
entropy monotonicity
The closed Lean certificate is:
finite_ordered_ring_sink_quadratic_relaxation_certificate
The integer and rational specializations are exposed as:
finite_ordered_ring_sink_quadratic_relaxation_certificate_int
finite_ordered_ring_sink_quadratic_relaxation_certificate_rat
Relation to PR #411 and PR #412
This abstracts the finite sink-quadratic relaxation theorem from finite integer and finite rational domains to arbitrary finite domains over explicit square-nonnegative quadratic sink order data.
Boundary
Finite ordered-data sink-quadratic relaxation theorem only.
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
