import Chronos.Frontier.QKDiniSourceDerivedCoefficientFamilyInterface

namespace Chronos
namespace Frontier

structure ConcreteScientificQKDiniSourceObjectPayload where
  sourceId : String
  sourceKind : String
  provenance : String
  sourceObject : QKDiniSourceObject
  scientific_derivation_claim : Prop

def ConcreteScientificQKDiniSourceObject : Prop :=
  ∃ P : ConcreteScientificQKDiniSourceObjectPayload,
    P.scientific_derivation_claim

theorem concreteScientificQKDiniSourceObject_has_source_object
    (h : ConcreteScientificQKDiniSourceObject) :
    ∃ S : QKDiniSourceObject, S = S := by
  rcases h with ⟨P, _hP⟩
  exact ⟨P.sourceObject, rfl⟩

def concreteScientificQKDiniSourceObject_extracts_coefficient_family
    (P : ConcreteScientificQKDiniSourceObjectPayload)
    (_h : P.scientific_derivation_claim) :
    QKDiniCoefficientFamily :=
  P.sourceObject.toCoefficientFamily

def concreteScientificQKDiniSourceObject_extracts_uniform_bounds
    (P : ConcreteScientificQKDiniSourceObjectPayload)
    (_h : P.scientific_derivation_claim) :
    QKDiniUniformCoefficientBounds P.sourceObject.toCoefficientFamily :=
  P.sourceObject.toUniformCoefficientBounds

def ConcreteScientificQKDiniSourceObjectPayloadGateStatus : String :=
  "PAYLOAD_GATE_ONLY_NO_CONCRETE_SCIENTIFIC_SOURCE_SUPPLIED"

end Frontier
end Chronos
