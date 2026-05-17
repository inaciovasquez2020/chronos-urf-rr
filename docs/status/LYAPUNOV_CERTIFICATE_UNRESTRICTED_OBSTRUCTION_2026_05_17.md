# Lyapunov Certificate Unrestricted Obstruction

Status: `UNRESTRICTED_LYAPUNOV_CERTIFICATE_FALSE`.

## Closed

The unrestricted statement is false:

```lean
¬ ∀ D : NaturalHyperbolicBoundSystem,
  ∃ L B : ℝ, LyapunovFiberBoundData D L B
The counterexample is zeroBoundSystem, where expansion, loss, and entropy mass are all zero. Any certificate would require 0 < L - B, while the lower/upper bounds force L - B ≤ 0.
Main Theorem
unrestricted_LyapunovFiberBoundData_false
Next Required Input
restricted admissible domain excluding zero-gap systems
Boundary
Obstruction only.
This does not prove:
construction of a replacement admissible domain
unrestricted RateThickFiberCoercivity
unrestricted UniversalFiberEntropyGap
unrestricted Chronos-RR
H4.1/FGL
P vs NP
any Clay problem
