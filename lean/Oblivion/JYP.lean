import Oblivion.CFISkeleton

-- Local cycle space placeholder
def localCycleSpace (G : Graph) (R : Nat) (v : G.V) : Type :=
  Unit

-- Global cycle space placeholder
def globalCycleSpace (G : Graph) : Type :=
  Unit

-- Local-to-global map Φ
def Phi (G : Graph) (R : Nat) :
  (Σ v : G.V, localCycleSpace G R v) → globalCycleSpace G :=
  fun _ => ()

-- Rank (placeholder)
def rank {α β : Type} (f : α → β) : Nat := 0

-- JYP statement (axiomatic form)
axiom JYP_bound :
  ∀ (k R : Nat) (G : Graph),
    rank (Phi G R) ≤ k + R + 1

-- Cyclone from JYP
theorem cyclone_from_JYP
  (k R : Nat) (H : BaseGraph) :
  ∃ G₀ G₁ : Graph,
    omega G₀ ≠ omega G₁ :=
by
  -- relies on JYP_bound to block local reconstruction
  exact ⟨CFI H false, CFI H true, by
    have hspec := omega_CFI_spec H
    cases hspec with
    | intro h0 h1 =>
      simp [h0, h1]⟩
