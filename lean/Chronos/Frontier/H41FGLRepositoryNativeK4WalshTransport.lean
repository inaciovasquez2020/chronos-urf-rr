import Chronos.Frontier.H41FGLRepositoryNativeK4HistoryRealizabilityInterface
import Chronos.Frontier.H41FGLAffineLiftK4WalshCertificate

namespace Chronos
namespace Frontier

namespace H41FGLRepositoryNativeK4HistoryRealizability

/-- A noncanonical enumeration of the four-bit carrier by `Fin 16`. -/
noncomputable def h41FGLK4BitVectorEquivFin16 :
    H41FGLK4BitVector ≃ Fin 16 :=
  Fintype.equivFinOfCardEq (by native_decide)

/--
Reindex rational-valued functions along an equivalence of their carrier
types.
-/
def h41FGLK4FunctionReindexEquiv
    {α β : Type*}
    (e : α ≃ β) :
    (α → ℚ) ≃ (β → ℚ) where
  toFun f := fun b => f (e.symm b)
  invFun g := fun a => g (e a)
  left_inv := by
    intro f
    funext a
    simp
  right_inv := by
    intro g
    funext b
    simp

/--
Under repository-native vertex extensionality, the abstract history carrier
is equivalent to the concrete sixteen-state Walsh index carrier.
-/
noncomputable def repositoryNativeHistoryEquivFin16
    (data : H41FGLRepositoryNativeK4HistoryRealizability)
    (hvertexExt : H41FGLRepositoryNativeK4VertexExt data) :
    data.History ≃ Fin 16 :=
  (historyEquivBitVector data hvertexExt).trans
    h41FGLK4BitVectorEquivFin16

/--
The existing concrete sixteen-state Walsh transform transported to rational
functions on the repository-native history carrier.

This remains conditional on `hvertexExt`; it does not construct or prove
repository-native vertex extensionality.
-/
noncomputable def repositoryNativeK4WalshTransform
    (data : H41FGLRepositoryNativeK4HistoryRealizability)
    (hvertexExt : H41FGLRepositoryNativeK4VertexExt data) :
    (data.History → ℚ) → data.History → ℚ := by
  let e := repositoryNativeHistoryEquivFin16 data hvertexExt
  let reindex := h41FGLK4FunctionReindexEquiv e
  exact fun f =>
    reindex.symm
      (h41FGLK4WalshTransform (reindex f))

/--
Concrete Walsh injectivity transports by conjugation through the conditional
history equivalence.
-/
theorem repositoryNativeK4WalshTransform_injective
    (data : H41FGLRepositoryNativeK4HistoryRealizability)
    (hvertexExt : H41FGLRepositoryNativeK4VertexExt data) :
    Function.Injective
      (repositoryNativeK4WalshTransform data hvertexExt) := by
  let e := repositoryNativeHistoryEquivFin16 data hvertexExt
  let reindex := h41FGLK4FunctionReindexEquiv e
  change Function.Injective
    (fun f : data.History → ℚ =>
      reindex.symm
        (h41FGLK4WalshTransform (reindex f)))
  exact
    reindex.symm.injective.comp
      (h41FGLK4WalshTransform_injective.comp reindex.injective)

end H41FGLRepositoryNativeK4HistoryRealizability

end Frontier
end Chronos
