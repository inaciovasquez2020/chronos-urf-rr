import Chronos.Frontier.H41FGLRepositoryNativeK4WalshTransportBoundary

namespace Chronos
namespace Frontier

universe u

/--
The exact remaining carrier-construction obligation.

`IsRepositoryNativeCarrier` must be supplied by an independent mathematical
definition of the intended admissible-history space `X(𝒫_{4,0,1})`. This
structure then requires:

* a carrier satisfying that independent specification,
* four native Boolean observables,
* realization of every four-bit assignment, and
* vertex extensionality.

The existing abstract realizability interface, transported Walsh theorem, and
duplicated-history countermodel do not construct an inhabitant of this
structure.
-/
structure H41FGLRepositoryNativeK4CarrierConstruction
    (IsRepositoryNativeCarrier : Type u → Prop) where
  History : Type u
  repository_native : IsRepositoryNativeCarrier History

  vertexObservable : Fin 4 → History → ZMod 2
  historyOfBits : H41FGLK4BitVector → History

  vertexObservable_historyOfBits :
    ∀ (σ : H41FGLK4BitVector) (i : Fin 4),
      vertexObservable i (historyOfBits σ) = σ i

  vertex_ext :
    ∀ h₁ h₂ : History,
      (∀ i : Fin 4,
        vertexObservable i h₁ = vertexObservable i h₂) →
      h₁ = h₂

namespace H41FGLRepositoryNativeK4CarrierConstruction

/-- Forget the independent carrier evidence and retain realizability data. -/
def toRealizability
    {IsRepositoryNativeCarrier : Type u → Prop}
    (construction :
      H41FGLRepositoryNativeK4CarrierConstruction
        IsRepositoryNativeCarrier) :
    H41FGLRepositoryNativeK4HistoryRealizability where
  History := construction.History
  vertexObservable := construction.vertexObservable
  historyOfBits := construction.historyOfBits
  vertexObservable_historyOfBits :=
    construction.vertexObservable_historyOfBits

/--
A completed carrier construction supplies the exact vertex-extensionality
hypothesis required by the transported K4 Walsh injectivity theorem.
-/
theorem toRealizability_vertexExt
    {IsRepositoryNativeCarrier : Type u → Prop}
    (construction :
      H41FGLRepositoryNativeK4CarrierConstruction
        IsRepositoryNativeCarrier) :
    H41FGLRepositoryNativeK4HistoryRealizability.H41FGLRepositoryNativeK4VertexExt
      construction.toRealizability := by
  intro h₁ h₂ hcoordinates
  apply construction.vertex_ext
  intro i
  exact congrFun hcoordinates i

/--
A completed repository-native carrier construction directly supplies the
conditional transported K4 Walsh-transform injectivity theorem.
-/
theorem repositoryNativeK4WalshTransform_injective
    {IsRepositoryNativeCarrier : Type u → Prop}
    (construction :
      H41FGLRepositoryNativeK4CarrierConstruction
        IsRepositoryNativeCarrier) :
    Function.Injective
      (H41FGLRepositoryNativeK4HistoryRealizability.repositoryNativeK4WalshTransform
        construction.toRealizability
        (toRealizability_vertexExt construction)) := by
  exact
    H41FGLRepositoryNativeK4HistoryRealizability.repositoryNativeK4WalshTransform_injective
      construction.toRealizability
      (toRealizability_vertexExt construction)

/--
An independently supplied carrier specification may be empty. In that case,
no completed repository-native carrier construction exists.
-/
theorem noCarrierConstructionForEmptySpecification :
    ¬ Nonempty
      (H41FGLRepositoryNativeK4CarrierConstruction
        (fun _ : Type u => False)) := by
  intro hconstruction
  rcases hconstruction with ⟨construction⟩
  exact construction.repository_native

/--
The current interfaces and transported Walsh results cannot uniformly
manufacture a carrier-construction inhabitant for every independent
repository-native carrier specification.

This does not refute construction for the intended `X(𝒫_{4,0,1})`
specification; that specification and its inhabitant remain separate inputs.
-/
theorem carrierConstruction_not_unconditional :
    ¬ ∀ IsRepositoryNativeCarrier : Type u → Prop,
        Nonempty
          (H41FGLRepositoryNativeK4CarrierConstruction
            IsRepositoryNativeCarrier) := by
  intro hall
  exact
    noCarrierConstructionForEmptySpecification
      (hall (fun _ : Type u => False))

end H41FGLRepositoryNativeK4CarrierConstruction

end Frontier
end Chronos
