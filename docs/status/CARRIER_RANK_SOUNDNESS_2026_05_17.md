# CarrierRankSoundness

Date: 2026-05-17

Status: RESTRICTED_POSITIVE_BRIDGE

## Added

```lean
def CarrierRankSoundness (sys : DynamicalSystem) : Prop :=
  ∀ ρ : Set (Set sys.State),
    (∃ n : Nat, sys.rankRate ρ n > 0) →
    NonNullFiberWitness sys
Proved
theorem restrictedRankRateBridge
theorem restrictedRankRateBridge_fromLowerBound
Boundary
Does not prove:
unrestricted RankRateBridgeLaw
RateThickFiberCoercivity
unrestricted UniversalFiberEntropyGap
unrestricted Chronos-RR
H4.1/FGL
P vs NP
any Clay problem
