import Chronos.Frontier.CanonicalRepositoryNativeCarrierSelectionBridge
import Chronos.RepositoryNativeCarrierSelection

namespace Chronos.Frontier.ConcreteRepositoryNativeCarrierSelectionBridge

open Chronos.RepositoryNativeCarrierSelection
open Chronos.Frontier.CanonicalRepositoryNativeCarrierSelectionBridge

def ConcreteRepositoryNativeCarrierSelectionCompatibility : Prop :=
  RepositoryNativeCarrierSelectionCompatibleWithCanonicalSemantics ∧
  ∀ (S : RepositoryNativeCarrierSelection) (n : Nat),
    Function.Injective (selectedEmbed S n) ∧
    Nonempty (selectedCPDL S n) ∧
    ∀ x : S.TRepo, selectedEmbed_property S n x

theorem concrete_repository_native_carrier_selection_compatible_with_canonical_semantics :
    ConcreteRepositoryNativeCarrierSelectionCompatibility := by
  constructor
  · exact repository_native_carrier_selection_compatible_with_canonical_semantics
  · intro S n
    refine ⟨selectedEmbed_injective S n, ?_, ?_⟩
    · exact ⟨selected_missingCPDLCCSLWitness S n⟩
    · intro x
      exact selectedEmbed_property S n x

end Chronos.Frontier.ConcreteRepositoryNativeCarrierSelectionBridge
