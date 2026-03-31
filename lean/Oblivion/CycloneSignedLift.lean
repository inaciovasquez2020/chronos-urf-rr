import Oblivion.Graph
import Oblivion.Beta1
import Oblivion.Ball
import Oblivion.Cycle
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

theorem beta1_signedLift_of_connected
    [Fintype G.V] [Fintype G.E]
    (σ : G.E → Bool)
    (hG : Connected G)
    (hL : Connected (signedLift (G := G) σ)) :
    beta1 (signedLift (G := G) σ) = 2 * beta1 G - 1 := by
  admit

theorem signedLift_beta1_changes
    [Fintype G.V] [Fintype G.E]
    (σ : G.E → Bool)
    (hG : Connected G)
    (hL : Connected (signedLift (G := G) σ))
    (hβ : 2 ≤ beta1 G) :
    beta1 (signedLift (G := G) σ) ≠ beta1 G := by
  admit

theorem girth_gt_twoR_implies_ball_acyclic
    (R : Nat) (v : G.V) (hG : Connected G) (hg : 2 * R < girth G) :
    Oblivion.IsTree (ball G v R) := by
  refine ⟨connected_ball (G := G) hG v R, ?_⟩
  intro C
  obtain ⟨C', hlen⟩ := ball_cycle_embeds_in_graph (G := G) v R C
  have h1 : C.edges.card ≤ 2 * R := cycle_length_le_twoR_of_subgraph_ball (G := G) v R C
  have h2 : girth G ≤ C'.edges.card := girth_le_cycle_length C'
  rw [hlen] at h2
  omega
  · admit
  · simp [ball]

theorem signedLift_ball_iso
    (R : Nat) (σ : G.E → Bool) (v : G.V) :
    ∃ w : (signedLift (G := G) σ).V,
      BallIso G (signedLift (G := G) σ) v w R := by
  refine ⟨(v, ⟨0, by decide⟩), ?_⟩
  obtain ⟨f, hf⟩ := signedLift_ball_local_bijection (G := G) σ v R
  refine ⟨f, Classical.choose ?_, ?_, ?_, ?_⟩
  · exact Classical.choice (Classical.decEq _)
  · admit
  · admit
  · exact signedLift_ball_local_adjacency (G := G) σ v R f

end Oblivion.LocalityAndLift
