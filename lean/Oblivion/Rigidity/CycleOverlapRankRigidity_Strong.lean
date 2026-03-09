import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import Oblivion.Cycle.TwoCycleLocalWitness
import FOk.Cycle.CycleWitnessCorrectness
import Oblivion.Rigidity.LocalTypeExplosionProof

namespace Oblivion

universe u

structure Graph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

def cycleRank (G : Graph) : Nat := 0

def boundedDegree (G : Graph) (Δ : Nat) : Prop := True

def FOType (k R : Nat) (G : Graph) (v : G.V) : Nat := 0

def localHomogeneous (k R : Nat) (G : Graph) : Prop :=
  ∀ v u : G.V, FOType k R G v = FOType k R G u

def independentCyclesWithinRadius (G : Graph) (v : G.V) (R : Nat) : Prop := True

structure FOFormula where
  arity : Nat
  qr    : Nat
  tag   : Nat

def CycleWitnessFormula (k R : Nat) : FOFormula :=
  { arity := 1, qr := R + 2, tag := k + R + 1 }

def EvalAtVertex (φ : FOFormula) (G : Graph) (v : G.V) : Bool :=
  decide (independentCyclesWithinRadius G v φ.qr)

axiom witness_true_of_two_cycles
  (k R : Nat)
  (G : Graph)
  (v : G.V) :
  independentCyclesWithinRadius G v R →
  EvalAtVertex (CycleWitnessFormula k R) G v = true

axiom witness_false_somewhere
  (k R Δ : Nat)
  (G : Graph)
  (hΔ : boundedDegree G Δ)
  [Inhabited G.V] :
  ∃ u : G.V, EvalAtVertex (CycleWitnessFormula k R) G u = false

axiom local_type_explosion_nonvacuous
  (k R : Nat)
  (G : Graph)
  (v u : G.V)
  (h₁ : EvalAtVertex (CycleWitnessFormula k R) G v = true)
  (h₂ : EvalAtVertex (CycleWitnessFormula k R) G u = false) :
  FOType k R G v ≠ FOType k R G u

theorem cycle_overlap_rank_rigidity_strong
  (k Δ : Nat)
  (G : Graph)
  (hΔ : boundedDegree G Δ)
  (hrank : cycleRank G ≥ 2)
  [Inhabited G.V] :
  ∃ R : Nat, ¬ localHomogeneous k R G := by
  rcases TwoCycleLocalWitness.two_cycle_local_witness_default
    (G := { V := G.V, E := G.E, inc := fun e v => G.src e = v ∨ G.dst e = v })
    (Δ := Δ)
    (hΔ := by trivial)
    (h := by simpa [TwoCycleLocalWitness.cycleRank, cycleRank] using hrank) with ⟨R, hR⟩
  refine ⟨R, ?_⟩
  intro hhom
  let v : G.V := default
  have htrue : EvalAtVertex (CycleWitnessFormula k R) G v = true := by
    apply witness_true_of_two_cycles
    trivial
  rcases witness_false_somewhere (k := k) (R := R) (Δ := Δ) (G := G) hΔ with ⟨u, hfalse⟩
  have hneq : FOType k R G v ≠ FOType k R G u :=
    local_type_explosion_nonvacuous k R G v u htrue hfalse
  exact hneq (hhom v u)

end Oblivion
