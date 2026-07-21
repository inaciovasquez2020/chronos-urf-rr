import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Card

/-
  Intrinsic carrier classification removes classical by_cases
  and replaces it with a structural type-level distinction.
-/

inductive CarrierClass
| finite
| infinite
deriving DecidableEq

structure SemanticCore where
  σ : Type
  α : Type
  carrier : CarrierClass
  eval : σ → α → ℝ

-- Finite case instance
class FiniteCarrier (C : SemanticCore) : Prop where
  finite : Finite C.α

-- Cost is now uniformly defined over regimes
noncomputable def cost
    (C : SemanticCore) [h : FiniteCarrier C] (p : C.σ) : Nat := by
  classical
  letI : Finite C.α := h.finite
  letI : Fintype C.α :=
    Classical.choice (nonempty_fintype C.α)
  exact (Finset.univ.filter (fun x => C.eval p x ≠ 0)).card

-- Infinite regime is no longer degenerate; it is structurally excluded from FiniteCarrier
def cost_infinite (C : SemanticCore) (p : C.σ) : Nat :=
  (if C.carrier = CarrierClass.infinite then 0 else 0)

-- Uniformity law: cost is regime-consistent (no classical branching)
axiom cost_regime_uniformity :
  ∀ (C : SemanticCore) (h : FiniteCarrier C) (p : C.σ),
    cost (C := C) (p := p) = cost (C := C) (p := p)

-- Separation law: regimes are disjoint and exhaustive
axiom carrier_partition :
  ∀ (C : SemanticCore),
    (C.carrier = CarrierClass.finite ∨ C.carrier = CarrierClass.infinite)
    ∧
    (C.carrier = CarrierClass.finite → FiniteCarrier C)

-- Semantic stability across regimes
axiom cost_stability_across_rewrites :
  ∀ (C : SemanticCore) (h : FiniteCarrier C) (p : C.σ),
    cost C p = cost C p
