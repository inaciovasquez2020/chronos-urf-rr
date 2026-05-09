# Admissibility Positivity Decision Lock — 2026-05-09

Status: DECISION_LOCKED

Decision:

```text
Current RealChronosAdmissiblePredicate semantics permit zero-arity.
Therefore ZeroArityExclusion is not currently theorem-level provable
without strengthening admissibility.
Current semantic state:
RealChronosAdmissiblePredicate contains arity : Nat but does not enforce arity_pos.
Repository-native bridge requires positive arity.
RepositoryNativeImageCoverageCounterexample records a zero-arity admissible object outside repository-native image.
Blocked theorem:
ZeroArityExclusion:
∀ P, ZeroArityPredicate P → ¬ RealChronosAdmissiblePredicate P
Minimal missing assumption for exclusion:
PositiveArityAdmissibility:
∀ P, RealChronosAdmissiblePredicate P → 0 < arity(P)
Viable route without semantic change:
ZeroArityRepresentation:
∀ P, ZeroArityPredicate P ∧ RealChronosAdmissiblePredicate P →
  ∃ C ∈ RegisteredChronosCarriers, Represents C P
Required semantic change for exclusion:
Strengthen RealChronosAdmissiblePredicate with positive arity.
Invalidate the existing zero-arity admissible counterexample.
Boundary:
This file does not prove ZeroArityExclusion.
This file does not prove ZeroArityRepresentation.
This file does not resolve ZeroArityCarrierObstruction.
This file does not prove CarrierRegistryExhaustiveness.
This file does not prove Reg-SNF.
This file does not prove UniversalFiberEntropyGap.
This file does not prove DepthBridge.
This file does not prove Chronos-RR.
This file does not prove H4.1/FGL.
This file does not prove P vs NP.
This file does not prove any Clay problem.
