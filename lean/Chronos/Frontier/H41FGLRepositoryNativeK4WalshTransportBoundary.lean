import Chronos.Frontier.H41FGLRepositoryNativeK4WalshTransport

namespace Chronos
namespace Frontier

namespace H41FGLRepositoryNativeK4HistoryRealizability

universe u

/--
A realizability interface may contain two distinct histories with identical
four-bit observations.

The extra Boolean coordinate is deliberately invisible to every vertex
observable. `ULift` places this countermodel in an arbitrary universe.
-/
def h41FGLK4DuplicatedHistoryRealizability :
    H41FGLRepositoryNativeK4HistoryRealizability.{u} where
  History := ULift.{u} (H41FGLK4BitVector × Bool)
  vertexObservable := fun i h => h.down.1 i
  historyOfBits := fun σ => ⟨(σ, false)⟩
  vertexObservable_historyOfBits := by
    intro σ i
    rfl

/--
The duplicated-history realizability interface does not satisfy vertex
extensionality in any universe.
-/
theorem h41FGLK4DuplicatedHistoryRealizability_not_vertexExt :
    ¬ H41FGLRepositoryNativeK4VertexExt
      (h41FGLK4DuplicatedHistoryRealizability.{u}) := by
  intro hvertexExt
  let σ : H41FGLK4BitVector := fun _ => 0
  let hFalse :
      (h41FGLK4DuplicatedHistoryRealizability.{u}).History :=
    ⟨(σ, false)⟩
  let hTrue :
      (h41FGLK4DuplicatedHistoryRealizability.{u}).History :=
    ⟨(σ, true)⟩
  have hpairs : hFalse = hTrue := by
    apply hvertexExt
    rfl
  have hfalseTrue : false = true :=
    congrArg
      (fun h : ULift.{u} (H41FGLK4BitVector × Bool) => h.down.2)
      hpairs
  cases hfalseTrue

/--
Repository-native vertex extensionality cannot be derived from the current
realizability interface alone in any universe.

Consequently, transported Walsh injectivity remains conditional on an
independently supplied `H41FGLRepositoryNativeK4VertexExt` proof.
-/
theorem repositoryNativeK4VertexExt_not_unconditional :
    ¬ ∀ data : H41FGLRepositoryNativeK4HistoryRealizability.{u},
        H41FGLRepositoryNativeK4VertexExt data := by
  intro hall
  exact
    h41FGLK4DuplicatedHistoryRealizability_not_vertexExt
      (hall h41FGLK4DuplicatedHistoryRealizability)

end H41FGLRepositoryNativeK4HistoryRealizability

end Frontier
end Chronos
