import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

open Finset
open scoped BigOperators

namespace Chronos.Frontier

variable {X Y : Type} [Fintype X] [Fintype Y] [DecidableEq Y] [Nonempty Y]

lemma fiber_large_exists
    (f : X → Y)
    (q g : ℕ)
    (h : Fintype.card X ≥ Fintype.card Y * q ^ g) :
    ∃ y : Y, Fintype.card {x : X // f x = y} ≥ q ^ g := by
  by_cases hq0 : q ^ g = 0
  · obtain ⟨y⟩ := (inferInstance : Nonempty Y)
    exact ⟨y, by simp [hq0]⟩

  have hqpos : 0 < q ^ g := Nat.pos_of_ne_zero hq0

  by_contra hnot
  push_neg at hnot

  have hfiber :
      ∀ y : Y, Fintype.card {x : X // f x = y} ≤ q ^ g - 1 := by
    intro y
    exact Nat.le_pred_of_lt (hnot y)

  have esigma : (Sigma fun y : Y => {x : X // f x = y}) ≃ X :=
    { toFun := fun p : Sigma fun y : Y => {x : X // f x = y} => p.2.1
      invFun := fun x : X => ⟨f x, ⟨x, rfl⟩⟩
      left_inv := by
        intro p
        cases p with
        | mk y z =>
          cases z with
          | mk x hx =>
            subst y
            rfl
      right_inv := by
        intro x
        rfl }

  have hsigmacard :
      Fintype.card (Sigma fun y : Y => {x : X // f x = y}) =
        Fintype.card X := by
    exact Fintype.card_congr esigma

  have hsum :
      (∑ y : Y, Fintype.card {x : X // f x = y}) = Fintype.card X := by
    have hsigma :
        Fintype.card (Sigma fun y : Y => {x : X // f x = y}) =
          ∑ y : Y, Fintype.card {x : X // f x = y} := by
      exact Fintype.card_sigma
    exact hsigma.symm.trans hsigmacard

  have hsum_le :
      (∑ y : Y, Fintype.card {x : X // f x = y}) ≤
        ∑ y : Y, (q ^ g - 1) := by
    exact Finset.sum_le_sum (fun y _ => hfiber y)

  have hupper :
      Fintype.card X ≤ Fintype.card Y * (q ^ g - 1) := by
    calc
      Fintype.card X =
          ∑ y : Y, Fintype.card {x : X // f x = y} := hsum.symm
      _ ≤ ∑ y : Y, (q ^ g - 1) := hsum_le
      _ = Fintype.card Y * (q ^ g - 1) := by simp

  have hy : 0 < Fintype.card Y := by
    exact Fintype.card_pos_iff.mpr inferInstance

  have hpred : q ^ g - 1 < q ^ g := by
    exact Nat.pred_lt (by simpa using Nat.ne_of_gt hqpos)

  have hstrict :
      Fintype.card Y * (q ^ g - 1) < Fintype.card Y * q ^ g := by
    exact (Nat.mul_lt_mul_left hy).mpr hpred

  exact (not_lt_of_ge h) (lt_of_le_of_lt hupper hstrict)

end Chronos.Frontier
