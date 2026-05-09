# Zero-Arity Carrier Obstruction Boundary — 2026-05-09

Status: FRONTIER_OPEN

Minimal blocker:

```text
ZeroArityCarrierObstruction:
Unrestricted CarrierRegistryExhaustiveness is blocked unless
zero-arity admissible predicates are either represented by a registered carrier
or formally excluded from RealChronosAdmissiblePredicate.
Weakest sufficient resolution:
Either:
  ZeroArityRepresentation:
  every zero-arity admissible predicate has a registered carrier

Or:
  ZeroArityExclusion:
  zero-arity predicates are not RealChronosAdmissiblePredicate objects
Downstream chain:
ZeroArityCarrierObstruction resolved
⇒ CarrierRegistryExhaustiveness domain no longer blocked by arity-zero cases
⇒ Full Reg-SNF eligibility
⇒ UniversalFiberEntropyGap eligibility
⇒ DepthBridge eligibility
Boundary:
This file does not resolve ZeroArityCarrierObstruction.
This file does not prove ZeroArityRepresentation.
This file does not prove ZeroArityExclusion.
This file does not prove CarrierRegistryExhaustiveness.
This file does not prove Reg-SNF.
This file does not prove UniversalFiberEntropyGap.
This file does not prove DepthBridge.
This file does not prove Chronos-RR.
This file does not prove H4.1/FGL.
This file does not prove P vs NP.
This file does not prove any Clay problem.
