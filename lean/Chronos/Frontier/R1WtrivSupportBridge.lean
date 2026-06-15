import Chronos.Frontier.R1R2R3SemanticTheoremProofTargets

namespace Chronos
namespace Frontier

universe u

def R1WtrivSupportGenerationBridge (D : R1SemanticData) : Prop :=
  ∀ word edge,
    D.TrivWord word →
    D.WordSupport word edge →
      ∃ face, D.TrivFace face ∧ D.FaceBoundarySupport face edge

structure R1ExactWtrivSupportBridgeInputs (D : R1SemanticData) where
  r1a_trivialFacesAvoidLongChords :
    ∀ face, D.TrivFace face →
      ¬ D.FaceBoundarySupport face D.e1 ∧
      ¬ D.FaceBoundarySupport face D.e2
  r1b_wtrivGeneratedByTrivialFaces :
    R1WtrivSupportGenerationBridge D
  r1c_maximalSeparationForbidsTrivialLongChord : Prop
  r1c_supplied : r1c_maximalSeparationForbidsTrivialLongChord

theorem R1WtrivSupportGenerationBridge_from_semantic_inputs
    (D : R1SemanticData)
    (H : R1TheoremProofInputs D) :
    R1WtrivSupportGenerationBridge D := by
  intro word edge hword hsupport
  exact H.R1b_trivialWordSupportComesFromTrivialFaces word edge hword hsupport

theorem R1_exactWtriv_support_statement_from_R1a_R1b_R1c_bridge
    (D : R1SemanticData)
    (H : R1ExactWtrivSupportBridgeInputs D) :
    R1LongChordExclusionTheorem D := by
  intro word hword
  constructor
  · intro hsupport
    rcases H.r1b_wtrivGeneratedByTrivialFaces
      word D.e1 hword hsupport with ⟨face, hface, hboundary⟩
    exact (H.r1a_trivialFacesAvoidLongChords face hface).1 hboundary
  · intro hsupport
    rcases H.r1b_wtrivGeneratedByTrivialFaces
      word D.e2 hword hsupport with ⟨face, hface, hboundary⟩
    exact (H.r1a_trivialFacesAvoidLongChords face hface).2 hboundary

def R1WtrivSupportBridgeStatus : String :=
  "CONDITIONAL_SEMANTIC_BRIDGE_ONLY_NOT_R1_NATIVE_CLOSURE"

def R1WtrivSupportBridgeBoundary : String :=
  "Does not prove native R1 geometry, R2, R3, full FGL closure, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem."

end Frontier
end Chronos
