namespace Chronos.Frontier.FiberEntropyGap

universe u

structure BatchedUnitObservation (Lambda : Type u) where
  mu : Lambda -> Nat
  nontrivial_lower_bound : forall lam : Lambda, mu lam >= 2

def unit_dimension
    {Lambda : Type u}
    (_B : BatchedUnitObservation Lambda)
    (_lam : Lambda) :
    Nat :=
  1

def batched_dimension
    {Lambda : Type u}
    (B : BatchedUnitObservation Lambda)
    (lam : Lambda) :
    Nat :=
  B.mu lam

def FiberEntropyGap
    {Lambda : Type u}
    (B : BatchedUnitObservation Lambda) :
    Prop :=
  exists lam0 : Lambda,
    batched_dimension B lam0 > unit_dimension B lam0

private theorem ge_two_gt_one {n : Nat} (h : n >= 2) : n > 1 :=
  Nat.lt_of_lt_of_le (by decide : 1 < 2) h

theorem fiber_entropy_gap_inhabited
    {Lambda : Type u}
    (B : BatchedUnitObservation Lambda)
    (lam0 : Lambda) :
    FiberEntropyGap B :=
  Exists.intro lam0 (ge_two_gt_one (B.nontrivial_lower_bound lam0))

def MultiplicityWeightedObservationDimension
    {Lambda : Type u}
    (B : BatchedUnitObservation Lambda) :
    Lambda -> Nat :=
  fun lam => B.mu lam

theorem BatchedUnitObservationDimensionExtraction
    {Lambda : Type u}
    (B : BatchedUnitObservation Lambda) :
    forall lam : Lambda, MultiplicityWeightedObservationDimension B lam >= 2 :=
  fun lam => B.nontrivial_lower_bound lam

theorem fiber_entropy_gap_from_batched_unit_observation
    {Lambda : Type u}
    (B : BatchedUnitObservation Lambda)
    (hGap :
      (forall lam : Lambda, MultiplicityWeightedObservationDimension B lam >= 2) ->
        FiberEntropyGap B) :
    FiberEntropyGap B :=
  hGap (BatchedUnitObservationDimensionExtraction B)

theorem fiber_entropy_gap_unconditional
    {Lambda : Type u}
    (B : BatchedUnitObservation Lambda)
    (lam0 : Lambda) :
    FiberEntropyGap B := by
  exact fiber_entropy_gap_inhabited B lam0

axiom UnitObservationNontrivialEntropyGap_FRONTIER_OPEN : Prop

end Chronos.Frontier.FiberEntropyGap
