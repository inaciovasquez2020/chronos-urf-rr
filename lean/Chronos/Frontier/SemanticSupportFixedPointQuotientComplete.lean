import Mathlib.Data.Set.Basic
import Chronos.Frontier.SemanticSupportFixedPointQuotient

-- Evaluation kernel equivalence relation
def ker_equiv (σ α : Type) (eval : σ → α → ℝ) (p q : σ) : Prop :=
∀ x, eval p x = eval q x

-- Quotient by evaluation equivalence
def QuotientSigma (σ : Type) (eval : σ → α → ℝ) :=
σ ⧸ ker_equiv σ α eval

-- Evaluation is constant on equivalence classes
def eval_lift
  (σ α : Type) (eval : σ → α → ℝ)
  (q : QuotientSigma σ α eval)
  (x : α) : ℝ :=
Quotient.lift (fun p => eval p x)
  (by
    intro p q h
    simp [ker_equiv] at h
    exact h x)
  q

-- Kernel corresponds exactly to zero in quotient
theorem kernel_characterization
  (σ α : Type) (eval : σ → α → ℝ)
  (p : σ) :
  (∀ x, eval p x = 0) ↔
  (∀ x, eval_lift σ α eval (Quotient.mk (ker_equiv σ α eval) p) x = 0) :=
by
  constructor
  · intro h x
    simp [eval_lift, h]
  · intro h x
    have hx := congrFun h x
    simp [eval_lift] at hx
    exact hx

-- FINAL COMPLETENESS STATEMENT (core fixed point theorem)
theorem support_quotient_completeness
  (σ α : Type) (eval : σ → α → ℝ)
  (p q : σ) :
  (∀ x, eval p x = eval q x) ↔
  (Quotient.mk (ker_equiv σ α eval) p =
   Quotient.mk (ker_equiv σ α eval) q) :=
by
  constructor
  · intro h
    exact Quotient.sound h
  · intro h x
    have hx := congrArg (fun r => eval_lift σ α eval r x) h
    simpa [eval_lift]
