import Chronos.Frontier.ConcreteRepositoryNativeCarrierSelectionBridge
import Chronos.Frontier.CanonicalRepositoryNativeSemantics
import Chronos.RepositoryNativeCarrierSelection

namespace Chronos.Frontier.ConcreteExportSemanticPreservation

open Chronos.RepositoryNativeCarrierSelection
open Chronos.Frontier.ConcreteRepositoryNativeCarrierSelectionBridge
open Chronos.Frontier.CanonicalRepositoryNativeSemantics

def ConcreteExportSemanticPreservation : Prop :=
  ConcreteRepositoryNativeCarrierSelectionCompatibility ∧
  CanonicalRepositoryNativeSemantics ∧
  ∀ (S : RepositoryNativeCarrierSelection) (n : Nat),
    Function.Injective (selectedEmbed S n) ∧
    Nonempty (selectedCPDL S n) ∧
    ∀ x : S.TRepo, selectedEmbed_property S n x

theorem concrete_export_semantic_preservation :
    ConcreteExportSemanticPreservation := by
  constructor
  · exact concrete_repository_native_carrier_selection_compatible_with_canonical_semantics
  · constructor
    · exact canonical_repository_native_semantics
    · intro S n
      refine ⟨selectedEmbed_injective S n, ?_, ?_⟩
      · exact ⟨selected_missingCPDLCCSLWitness S n⟩
      · intro x
        exact selectedEmbed_property S n x

end Chronos.Frontier.ConcreteExportSemanticPreservation
