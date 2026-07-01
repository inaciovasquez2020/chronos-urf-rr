import Lean

variable (C : SemanticCore)

-- finite cost (existing definition assumed present elsewhere)
def cost_finite [Fintype C.α] (p : C.σ) : Nat :=
  (Finset.univ.filter (fun x => C.eval p x ≠ 0)).card

-- infinite fallback (no computation)
noncomputable def cost_infinite (p : C.σ) : Nat :=
0

-- unified dispatcher
def cost_dispatch (p : C.σ) : Nat :=
  by
    classical
    by_cases h : Fintype C.α
    · exact cost_finite (C := C) (p := p)
    · exact cost_infinite (C := C) (p := p)
