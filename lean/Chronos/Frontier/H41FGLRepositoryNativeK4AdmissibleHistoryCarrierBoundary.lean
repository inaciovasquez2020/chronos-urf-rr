import Chronos.Frontier.H41FGLRepositoryNativeK4AdmissibleHistoryCarrierCandidate

namespace Chronos
namespace Frontier

/--
Identification of the selected bounded admissible-history carrier with an
independently specified external history carrier.
-/
def H41FGLK4SelectedAdmissibleHistoryIdentifiesExternal
    (ExternalHistory : Type) :
    Prop :=
  Nonempty (H41FGLK4SelectedAdmissibleHistory ≃ ExternalHistory)

/--
The equivalence between the selected admissible subtype and the bounded
vertex-assignment carrier does not uniformly identify that subtype with an
arbitrary external history carrier.

This does not refute identification with the intended `X(𝒫_{4,0,1})`.
That carrier still requires an independent definition and a specific
equivalence proof.
-/
theorem h41FGLK4SelectedAdmissibleHistoryIdentification_not_unconditional :
    ¬ ∀ ExternalHistory : Type,
        H41FGLK4SelectedAdmissibleHistoryIdentifiesExternal
          ExternalHistory := by
  intro hall
  rcases hall Empty with ⟨identification⟩
  exact
    (identification
      (h41FGLK4SelectedAdmissibleHistoryOfBits
        (fun _ => 0))).elim

end Frontier
end Chronos
