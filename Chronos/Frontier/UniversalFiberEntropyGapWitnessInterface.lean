import Chronos.Frontier.SelectedDepthBridgeSemanticGapNonPromotion

open Chronos.Frontier.SemanticEntropyBridge
open Chronos.Frontier.SemanticTwoPointUniversalFiberGapWitness

namespace Chronos.Frontier.UniversalFiberEntropyGapWitnessInterface

universe u

def UniversalFiberEntropyGapWitnessInterface : Prop :=
  ∀ {Omega : Type u} (P : ProbabilisticUnitObservation Omega),
    UnitObservationTwoPointSupport P → UniversalFiberEntropyGap P

theorem universal_fiber_entropy_gap_witness_interface :
    UniversalFiberEntropyGapWitnessInterface := by
  intro Omega P h
  exact semantic_two_point_universal_fiber_gap_witness P h

end Chronos.Frontier.UniversalFiberEntropyGapWitnessInterface
