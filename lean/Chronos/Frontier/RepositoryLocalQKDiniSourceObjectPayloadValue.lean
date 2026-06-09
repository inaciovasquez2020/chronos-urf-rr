import Chronos.Frontier.ConcreteScientificQKDiniSourceObjectPayloadGate

namespace Chronos
namespace Frontier

structure RepositoryLocalQKDiniAdmissibility
    (sourceObject : QKDiniSourceObject) : Prop where
  same_frontier_origin : True
  bounds_acknowledged : True

structure RepositoryLocalQKDiniSourceObjectPayload where
  sourceId : String
  sourceKind : String
  provenance : String
  sourceObject : QKDiniSourceObject
  repository_local_admissibility :
    RepositoryLocalQKDiniAdmissibility sourceObject

def RepositoryLocalQKDiniSourceObject :
    QKDiniSourceObject where
  Index := Unit
  coefficient := fun _ _ => 1
  bound := 1
  nonzero := by
    exact ⟨(), 0, by decide⟩
  uniform_bound := by
    intro _ _
    exact Nat.le_refl 1

def RepositoryLocalQKDiniSourceObjectPayloadValue :
    RepositoryLocalQKDiniSourceObjectPayload where
  sourceId := "QKDini.RepositoryLocal.001"
  sourceKind := "RepositoryLocalSymbolicFrontierObject"
  provenance := "repository-local symbolic payload; no external scientific derivation asserted"
  sourceObject := RepositoryLocalQKDiniSourceObject
  repository_local_admissibility :=
    { same_frontier_origin := trivial
      bounds_acknowledged := trivial }

def RepositoryLocalQKDiniSourceObjectPayloadValue.toCoefficientFamily :
    QKDiniCoefficientFamily :=
  RepositoryLocalQKDiniSourceObjectPayloadValue.sourceObject.toCoefficientFamily

def RepositoryLocalQKDiniSourceObjectPayloadValue.toUniformCoefficientBounds :
    QKDiniUniformCoefficientBounds
      RepositoryLocalQKDiniSourceObjectPayloadValue.toCoefficientFamily :=
  RepositoryLocalQKDiniSourceObjectPayloadValue.sourceObject.toUniformCoefficientBounds

theorem repositoryLocalQKDiniSourceObjectPayloadValue_nonzero :
    ∃ i : RepositoryLocalQKDiniSourceObjectPayloadValue.toCoefficientFamily.Index,
      ∃ n : Nat,
        RepositoryLocalQKDiniSourceObjectPayloadValue.toCoefficientFamily.coefficient i n ≠ 0 :=
  RepositoryLocalQKDiniSourceObjectPayloadValue.sourceObject.nonzero

theorem repositoryLocalQKDiniSourceObjectPayloadValue_uniform_bound :
    ∀ i : RepositoryLocalQKDiniSourceObjectPayloadValue.toCoefficientFamily.Index,
      ∀ n : Nat,
        RepositoryLocalQKDiniSourceObjectPayloadValue.toCoefficientFamily.coefficient i n
          ≤ RepositoryLocalQKDiniSourceObjectPayloadValue.toUniformCoefficientBounds.bound :=
  RepositoryLocalQKDiniSourceObjectPayloadValue.sourceObject.uniform_bound

def RepositoryLocalQKDiniSourceObjectPayloadValueStatus : String :=
  "REPOSITORY_LOCAL_PAYLOAD_VALUE_ONLY_NO_SCIENTIFIC_DERIVATION_CLAIM"

end Frontier
end Chronos
