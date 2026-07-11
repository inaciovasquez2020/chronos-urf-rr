import Chronos.Frontier.H41FGLRepositoryNativeK4WalshTransport

namespace Chronos
namespace Frontier

namespace H41FGLRepositoryNativeK4HistoryRealizability

/--
A realizability interface may contain two distinct histories with identical
four-bit observations.

The extra Boolean coordinate is deliberately invisible to every vertex
observable.
-/
def h41FGLK4DuplicatedHistoryRealizability :
    H41FGLRepositoryNativeK4HistoryRealizability where
  History := H41FGLK4BitVector × Bool
  vertexObservable := fun i h => h.1 i
  historyOfBits := fun σ => (σ, false)
  vertexObservable_historyOfBits := by
    intro σ i
    rfl

/--
The duplicated-history realizability interface does not satisfy vertex
extensionality.
-/
theorem h41FGLK4DuplicatedHistoryRealizability_not_vertexExt :
    ¬ H41FGLRepositoryNativeK4VertexExt
      h41FGLK4DuplicatedHistoryRealizability := by
  intro hvertexExt
  let σ : H41FGLK4BitVector := fun _ => 0
  have hpairs :
      (σ, false) = (σ, true) := by
    apply hvertexExt
    rfl
  have hfalseTrue : false = true :=
    congrArg Prod.snd hpairs
  cases hfalseTrue

/--
Repository-native vertex extensionality cannot be derived from the current
realizability interface alone at the concrete universe containing the
duplicated-history countermodel.

Consequently, transported Walsh injectivity remains conditional on an
independently supplied `H41FGLRepositoryNativeK4VertexExt` proof.
-/
theorem repositoryNativeK4VertexExt_not_unconditional :
    ¬ ∀ data : H41FGLRepositoryNativeK4HistoryRealizability.{0},
        H41FGLRepositoryNativeK4VertexExt data := by
  intro hall
  exact
    h41FGLK4DuplicatedHistoryRealizability_not_vertexExt
      (hall h41FGLK4DuplicatedHistoryRealizability)

end H41FGLRepositoryNativeK4HistoryRealizability

end Frontier
end Chronos
