import Mathlib

structure QKDiniCoefficientData where
  α : Nat → Real
  β : Nat → Real
  a : Nat → Real
  b : Nat → Real

def QKDiniUniformCoefficientBounds
    (D : QKDiniCoefficientData) : Prop :=
  ∃ μ : Real,
    0 < μ ∧
    ∀ k : Nat,
      D.β k + D.b k ≤ μ ∧
      D.α k + D.a k ≤ -μ

structure QKDiniShellData extends QKDiniCoefficientData where
  shellWeight : Nat → Real
  shellTransfer : Nat → Nat → Real

def QKDiniShellComparability
    (S : QKDiniShellData) : Prop :=
  ∃ C : Real,
    0 < C ∧
    ∀ k n : Nat,
      S.shellTransfer k n ≤ C * S.shellWeight n

structure QKDiniRA1nShellData extends QKDiniShellData where
  shellTerm : Nat → Real

def QKDiniRA1nShellSumClosure
    (R : QKDiniRA1nShellData) : Prop :=
  ∃ M : Real,
    0 < M ∧
    ∀ N : Nat,
      (Finset.range N).sum (fun n => R.shellTerm n) ≤ M

structure IntendedScientificDescentSystemInstance where
  Configuration : Type
  step : Configuration → Configuration
  rank : Configuration → Nat
  terminal : Configuration → Prop
  IntendedScientificConclusion : Configuration → Prop
  RepresentsIntendedScientificPhenomenon : Prop
  step_rank_drop :
    ∀ C : Configuration,
      ¬ terminal C → rank (step C) < rank C
  terminal_correct :
    ∀ C : Configuration,
      terminal C → IntendedScientificConclusion C
  interpretation_correct :
    RepresentsIntendedScientificPhenomenon

def QKDiniToIntendedScientificDescentSystemBridge
    (R : QKDiniRA1nShellData) : Prop :=
  QKDiniRA1nShellSumClosure R →
    Nonempty IntendedScientificDescentSystemInstance

def IntendedScientificDescentSystemInstance_witness : Prop :=
  Nonempty IntendedScientificDescentSystemInstance

theorem intended_scientific_descent_system_instance_witness_from_qk_dini_bridge
    (R : QKDiniRA1nShellData)
    (h_closure : QKDiniRA1nShellSumClosure R)
    (h_bridge : QKDiniToIntendedScientificDescentSystemBridge R) :
    IntendedScientificDescentSystemInstance_witness := by
  exact h_bridge h_closure
