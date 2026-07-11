import Chronos.Frontier.H41FGLRepositoryNativeK4VertexAssignmentCarrierCandidate

namespace Chronos
namespace Frontier

/--
Identification of the bounded vertex-assignment candidate with an independently
specified external history carrier.
-/
def H41FGLK4VertexAssignmentIdentifiesExternal
    (ExternalHistory : Type) :
    Prop :=
  Nonempty (H41FGLK4VertexAssignmentHistory ≃ ExternalHistory)

/--
The bounded candidate construction and its Walsh-transform injectivity do not
uniformly identify the candidate with an arbitrary external history carrier.

This theorem does not refute identification with the intended
`X(𝒫_{4,0,1})`; that carrier still requires an independent definition and a
specific equivalence proof.
-/
theorem h41FGLK4VertexAssignmentIdentification_not_unconditional :
    ¬ ∀ ExternalHistory : Type,
        H41FGLK4VertexAssignmentIdentifiesExternal ExternalHistory := by
  intro hall
  rcases hall Empty with ⟨identification⟩
  exact
    (identification
      (h41FGLK4VertexAssignmentHistoryOfBits
        (fun _ => 0))).elim

end Frontier
end Chronos
