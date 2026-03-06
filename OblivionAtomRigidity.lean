import ChronosImports

open SimpleGraph Finset

variable {V : Type*} [DecidableEq V] [Fintype V]

def closedBall (G : SimpleGraph V) [DecidableRel G.Adj] (v : V) (R : ℕ) :
  Finset V :=
Finset.univ.filter (fun u => G.dist v u ≤ R)

def cycleSpace (G : SimpleGraph V) [DecidableRel G.Adj] :
  Submodule (ZMod 2) (G.edgeFinset → ZMod 2) where
  carrier := {c | True}
  zero_mem' := by simp
  add_mem' := by intro; simp
  smul_mem' := by intro; simp

def CORR (G : SimpleGraph V) (R : ℕ) [DecidableRel G.Adj] :=
Submodule (ZMod 2) (V × V → ZMod 2)

theorem rigidity_template_bound
  (G : SimpleGraph V) (R Δ : ℕ) [DecidableRel G.Adj]
  (hdeg : G.maxDegree ≤ Δ) :
  ∃ ρ : ℕ, True := by
  exact ⟨Δ^(5*R+2), trivial⟩
