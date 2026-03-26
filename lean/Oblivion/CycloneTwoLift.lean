import ChronosUrfRr.Graph

open Oblivion Oblivion.LocalityAndLift

namespace Oblivion

variable (k R : Nat)
variable (G : Graph)
variable (σ : G.E → Bool)
variable [Fintype G.V] [Fintype G.E]

variable (hconn  : Connected G)
variable (hlift  : Connected (signedLift (G := G) σ))
variable (hgirth : 2 * R < girth G)
variable (hβ     : 2 ≤ beta1 G)

lemma fo_equiv :
    FO_equiv_R k R G (signedLift (G := G) σ) := by
  sorry

lemma beta1_differs :
    beta1 G ≠ beta1 (signedLift (G := G) σ) := by
  exact (signedLift_beta1_changes σ hconn hlift hβ).symm

theorem cyclone_test :
    ∃ G₀ G₁ : Graph,
      FO_equiv_R k R G₀ G₁ ∧ beta1 G₀ ≠ beta1 G₁ :=
  ⟨G, signedLift (G := G) σ,
    fo_equiv k R G σ hconn hlift hgirth hβ,
    beta1_differs G σ hconn hlift hβ⟩

end Oblivion
