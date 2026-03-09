import Mathlib.Tactic
import Mathlib.Data.Fintype.Basic
import Mathlib.Logic.Equiv.Basic
import Cyclone.Core.Defs

namespace Cyclone.CCL.LemmaA

open Classical
open Cyclone.Core

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]
variable (k Δ R : ℕ)

theorem forward_injective_of_left_inverse
    {α β : Type*} {f : α → β} {g : β → α}
    (h : ∀ x, g (f x) = x) :
    Function.Injective f := by
  intro a b hEq
  calc
    a = g (f a) := (h a).symm
    _ = g (f b) := by simpa [hEq]
    _ = b := h b

abbrev LocalDuplicatorWins_Proper (k R : ℕ) : Prop :=
  FOkHomogeneous G k R

theorem LDW_proper_iff_FOkHom (k R : ℕ) :
    LocalDuplicatorWins_Proper G k R ↔ FOkHomogeneous G k R := by
  rfl

theorem LemmaA_proper
    (hLD : LocalDuplicatorWins_Proper G k R) :
    FOkHomogeneous G k R :=
  (LDW_proper_iff_FOkHom G k R).mp hLD

theorem AX1_discharge
    (hLD : LocalDuplicatorWins_Proper G k R) :
    FOkHomogeneous G k R :=
  LemmaA_proper G k Δ R hLD

theorem localData_invariant_id
    (h : localData_invariant G k R) :
    localData_invariant G k R :=
  h

end Cyclone.CCL.LemmaA
