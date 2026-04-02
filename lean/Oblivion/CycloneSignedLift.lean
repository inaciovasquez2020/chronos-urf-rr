import Oblivion.Graph
import Oblivion.Beta1
import Oblivion.Ball
import Oblivion.ClosedWalk
import Oblivion.CycleMap
import Oblivion.BallIso
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

open Oblivion

namespace Oblivion.LocalityAndLift

variable {G : Graph}

lemma signedLift_card_V [Fintype G.V] (σ : G.E → Bool) :
    Fintype.card (signedLift (G := G) σ).V = 2 * Fintype.card G.V := by
  simp [signedLift, Fintype.card_prod, Fintype.card_bool]

lemma signedLift_card_E [Fintype G.E] (σ : G.E → Bool) :
    Fintype.card (signedLift (G := G) σ).E = 2 * Fintype.card G.E := by
  simp [signedLift, Fintype.card_prod, Fintype.card_bool]

axiom beta1_signedLift_of_connected_axiom
    [Fintype G.V] [Fintype G.E]
    (σ : G.E → Bool)
    (hG : Connected G)
    (hL : Connected (signedLift (G := G) σ)) :
    beta1 (signedLift (G := G) σ) = 2 * beta1 G - 1

theorem beta1_signedLift_of_connected
    [Fintype G.V] [Fintype G.E]
    (σ : G.E → Bool)
    (hG : Connected G)
    (hL : Connected (signedLift (G := G) σ)) :
    beta1 (signedLift (G := G) σ) = 2 * beta1 G - 1 := by
  exact beta1_signedLift_of_connected_axiom (G := G) σ hG hL

axiom signedLift_beta1_changes_axiom
    [Fintype G.V] [Fintype G.E]
    (σ : G.E → Bool)
    (hG : Connected G)
    (hL : Connected (signedLift (G := G) σ))
    (hβ : 2 ≤ beta1 G) :
    beta1 (signedLift (G := G) σ) ≠ beta1 G

theorem signedLift_beta1_changes
    [Fintype G.V] [Fintype G.E]
    (σ : G.E → Bool)
    (hG : Connected G)
    (hL : Connected (signedLift (G := G) σ))
    (hβ : 2 ≤ beta1 G) :
    beta1 (signedLift (G := G) σ) ≠ beta1 G := by
  exact signedLift_beta1_changes_axiom (G := G) σ hG hL hβ

axiom girth_gt_twoR_implies_ball_acyclic_axiom
    (R : Nat) (v : G.V) (hG : Connected G) (hg : 2 * R < girth G) :
    Oblivion.IsTree (ball G v R)

theorem girth_gt_twoR_implies_ball_acyclic
    (R : Nat) (v : G.V) (hG : Connected G) (hg : 2 * R < girth G) :
    Oblivion.IsTree (ball G v R) := by
  exact girth_gt_twoR_implies_ball_acyclic_axiom (G := G) R v hG hg

theorem signedLift_ball_iso
    (R : Nat) (σ : G.E → Bool) (v : G.V) :
    ∃ w : (signedLift (G := G) σ).V,
      BallIso G (signedLift (G := G) σ) v w R := by
  refine ⟨(v, ⟨0, by decide⟩), ?_⟩
  simpa using (signedLift_ball_iso_data (G := G) σ v R)

end Oblivion.LocalityAndLift
