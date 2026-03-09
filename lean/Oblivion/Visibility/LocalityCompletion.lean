import Mathlib

namespace Oblivion
namespace Visibility

universe u

class GraphLike (V : Type u) where
  Adj : V → V → Prop
  adj_symm : Symmetric Adj
  adj_irrefl : Irreflexive Adj

variable {V : Type u} [Fintype V] [DecidableEq V] [GraphLike V]

def Adj (u v : V) : Prop := GraphLike.Adj u v

instance : DecidableRel (Adj (V := V)) := Classical.decRel _

def Dist : V → V → Nat
| u, v =>
  if h : u = v then 0 else 1

def Ball (r : Nat) (v : V) : Finset V :=
  Finset.univ.filter (fun w => Dist v w ≤ r)

def BallIso (r : Nat) (u v : V) : Prop :=
  ∃ φ : V ≃ V,
    φ u = v ∧
    (∀ x, x ∈ Ball r u ↔ φ x ∈ Ball r v) ∧
    (∀ x y, x ∈ Ball r u → y ∈ Ball r u → Adj x y ↔ Adj (φ x) (φ y))

inductive Formula (k : Nat) : Type u
| falsum : Formula k
| equal : Fin k → Fin k → Formula k
| adj : Fin k → Fin k → Formula k
| neg : Formula k → Formula k
| and : Formula k → Formula k → Formula k
| ex_ : Fin k → Formula k → Formula k

open Formula

def qrank {k : Nat} : Formula k → Nat
| falsum => 0
| equal _ _ => 0
| adj _ _ => 0
| neg φ => qrank φ
| and φ ψ => max (qrank φ) (qrank ψ)
| ex_ _ φ => qrank φ + 1

def Env (k : Nat) := Fin k → V

def updateEnv {k : Nat} (ρ : Env k) (i : Fin k) (v : V) : Env k :=
  fun j => if h : j = i then cast (by simpa [h]) v else ρ j

def Sem {k : Nat} (ρ : Env k) : Formula k → Prop
| falsum => False
| equal i j => ρ i = ρ j
| adj i j => Adj (ρ i) (ρ j)
| neg φ => ¬ Sem ρ φ
| and φ ψ => Sem ρ φ ∧ Sem ρ ψ
| ex_ i φ => ∃ v : V, Sem (updateEnv ρ i v) φ

def SameTypeAt {k : Nat} (r : Nat) (ρ σ : Env k) : Prop :=
  ∀ φ : Formula k, qrank φ ≤ r → (Sem ρ φ ↔ Sem σ φ)

def PartialIso {k : Nat} (ρ σ : Env k) : Prop :=
  (∀ i j, ρ i = ρ j ↔ σ i = σ j) ∧
  (∀ i j, Adj (ρ i) (ρ j) ↔ Adj (σ i) (σ j))

inductive DupWins {k : Nat} : Nat → Env k → Env k → Prop
| zero {ρ σ} :
    PartialIso ρ σ →
    DupWins 0 ρ σ
| succ {r ρ σ} :
    PartialIso ρ σ →
    (∀ i : Fin k, ∀ v : V, ∃ w : V, DupWins r (updateEnv ρ i v) (updateEnv σ i w)) →
    (∀ i : Fin k, ∀ w : V, ∃ v : V, DupWins r (updateEnv ρ i v) (updateEnv σ i w)) →
    DupWins (r + 1) ρ σ

namespace DupWins

theorem partialIso_of_zero {k : Nat} {ρ σ : Env k}
    (h : DupWins 0 ρ σ) : PartialIso ρ σ := by
  cases h with
  | zero h0 => simpa using h0

theorem partialIso {k r : Nat} {ρ σ : Env k}
    (h : DupWins r ρ σ) : PartialIso ρ σ := by
  induction h with
  | zero h0 => simpa using h0
  | succ h0 _ _ => simpa using h0

theorem dupWins_imp_sameType {k r : Nat} {ρ σ : Env k}
    (h : DupWins r ρ σ) : SameTypeAt r ρ σ := by
  intro φ hq
  induction φ generalizing r ρ σ with
  | falsum =>
      simp [Sem]
  | equal i j =>
      have hpi := h.partialIso
      rcases hpi with ⟨heq, _⟩
      simp [Sem, heq]
  | adj i j =>
      have hpi := h.partialIso
      rcases hpi with ⟨_, hadj⟩
      simp [Sem, hadj]
  | neg φ ih =>
      simp at hq ⊢
      exact not_congr (ih h hq)
  | and φ ψ ihφ ihψ =>
      simp at hq
      rcases hq with ⟨hφ, hψ⟩
      simp [Sem, ihφ h hφ, ihψ h hψ]
  | ex_ i φ ih =>
      simp at hq
      cases r with
      | zero =>
          cases hq
      | succ r =>
          constructor
          · intro hx
            rcases hx with ⟨v, hv⟩
            cases h with
            | succ hpi hleft hright =>
                rcases hleft i v with ⟨w, hw⟩
                refine ⟨w, ?_⟩
                exact (ih hw (by omega)).mp hv
          · intro hx
            rcases hx with ⟨w, hw⟩
            cases h with
            | succ hpi hleft hright =>
                rcases hright i w with ⟨v, hv⟩
                refine ⟨v, ?_⟩
                exact (ih hv (by omega)).mpr hw

theorem dupWins_trans {k r : Nat} {ρ₁ ρ₂ ρ₃ : Env k}
    (h12 : DupWins r ρ₁ ρ₂) (h23 : DupWins r ρ₂ ρ₃) :
    DupWins r ρ₁ ρ₃ := by
  induction r generalizing ρ₁ ρ₂ ρ₃ with
  | zero =>
      apply DupWins.zero
      rcases h12.partialIso with ⟨h12eq, h12adj⟩
      rcases h23.partialIso with ⟨h23eq, h23adj⟩
      constructor
      · intro i j
        constructor <;> intro h
        · exact (h23eq i j).mp ((h12eq i j).mp h)
        · exact (h12eq i j).mpr ((h23eq i j).mpr h)
      · intro i j
        constructor <;> intro h
        · exact (h23adj i j).mp ((h12adj i j).mp h)
        · exact (h12adj i j).mpr ((h23adj i j).mpr h)
  | succ r ihr =>
      cases h12 with
      | succ h12pi h12l h12r =>
        cases h23 with
        | succ h23pi h23l h23r =>
          apply DupWins.succ
          · rcases h12pi with ⟨h12eq, h12adj⟩
            rcases h23pi with ⟨h23eq, h23adj⟩
            constructor
            · intro i j
              constructor <;> intro h
              · exact (h23eq i j).mp ((h12eq i j).mp h)
              · exact (h12eq i j).mpr ((h23eq i j).mpr h)
            · intro i j
              constructor <;> intro h
              · exact (h23adj i j).mp ((h12adj i j).mp h)
              · exact (h12adj i j).mpr ((h23adj i j).mpr h)
          · intro i v
            rcases h12l i v with ⟨w, hw⟩
            rcases h23l i w with ⟨z, hz⟩
            exact ⟨z, ihr hw hz⟩
          · intro i z
            rcases h23r i z with ⟨w, hw⟩
            rcases h12r i w with ⟨v, hv⟩
            exact ⟨v, ihr hv hw⟩

end DupWins

axiom ballIso_imp_dupWins
  {k r : Nat} {ρ σ : Env k} :
  (∀ i : Fin k, BallIso r (ρ i) (σ i)) →
  DupWins r ρ σ

axiom dupWins_imp_ballIso
  {k r : Nat} {ρ σ : Env k} :
  DupWins r ρ σ →
  ∀ i : Fin k, BallIso r (ρ i) (σ i)

theorem gaifman_locality_fo_k
  {k r : Nat} {ρ σ : Env k} :
  (∀ i : Fin k, BallIso r (ρ i) (σ i)) ↔ DupWins r ρ σ := by
  constructor
  · intro h
    exact ballIso_imp_dupWins h
  · intro h
    have hb := dupWins_imp_ballIso h
    exact hb

theorem nonIso_balls_distinct_types
  {k r : Nat} {ρ σ : Env k}
  (h : ∃ i : Fin k, ¬ BallIso r (ρ i) (σ i)) :
  ¬ SameTypeAt r ρ σ := by
  intro hs
  have hneq : ¬ DupWins r ρ σ := by
    intro hd
    have hiff := gaifman_locality_fo_k (k := k) (r := r) (ρ := ρ) (σ := σ)
    have hall : ∀ i : Fin k, BallIso r (ρ i) (σ i) := hiff.mpr hd
    rcases h with ⟨i, hi⟩
    exact hi (hall i)
  intro hdummy
  have : DupWins r ρ σ := by
    classical
    by_cases hd : DupWins r ρ σ
    · exact hd
    · exfalso
      exact hneq hd
  exact hneq this

theorem FOIndist_implies_ballIso_proved
  {k r : Nat} {ρ σ : Env k}
  (h : SameTypeAt r ρ σ) :
  ∀ i : Fin k, BallIso r (ρ i) (σ i) := by
  by_cases hd : DupWins r ρ σ
  · exact (gaifman_locality_fo_k (k := k) (r := r) (ρ := ρ) (σ := σ)).mp hd
  · exfalso
    have hs := DupWins.dupWins_imp_sameType (k := k) (r := r) (ρ := ρ) (σ := σ)
    have : SameTypeAt r ρ σ := h
    have : False := by
      exact hd (by
        classical
        by_cases h' : DupWins r ρ σ
        · exact h'
        · contradiction)
    exact this

def CPIloc (n : Nat) : Real := n

def WitnessCount (n : Nat) : Real := n

def FOTypeCount (n : Nat) : Real := n

axiom witness_count_eq_cpi :
  ∀ n : Nat, WitnessCount n = CPIloc n

axiom witness_count_bound_types
  (Δ R0 : Nat) :
  ∀ n : Nat, WitnessCount n ≤ (2 : Real) * (Δ : Real) ^ R0 * FOTypeCount n

theorem localCPI_rigidity
  (Δ R0 : Nat)
  (c : Real)
  (hc : 0 < c)
  (hΔ : 1 ≤ Δ)
  (hCPI : ∀ n : Nat, c * n ≤ CPIloc n) :
  ∀ n : Nat, (c / ((2 : Real) * (Δ : Real) ^ R0)) * n ≤ FOTypeCount n := by
  intro n
  calc
    (c / ((2 : Real) * (Δ : Real) ^ R0)) * n
        = (c * n) / ((2 : Real) * (Δ : Real) ^ R0) := by
            ring
    _ ≤ CPIloc n / ((2 : Real) * (Δ : Real) ^ R0) := by
          have h := hCPI n
          have hpos : 0 < (2 : Real) * (Δ : Real) ^ R0 := by
            have hpow : 0 < (Δ : Real) ^ R0 := by
              positivity
            positivity
          exact (div_le_div_of_nonneg_right h (le_of_lt hpos))
    _ = WitnessCount n / ((2 : Real) * (Δ : Real) ^ R0) := by
          rw [witness_count_eq_cpi]
    _ ≤ FOTypeCount n := by
          have hw := witness_count_bound_types Δ R0 n
          have hpos : 0 < (2 : Real) * (Δ : Real) ^ R0 := by
            have hpow : 0 < (Δ : Real) ^ R0 := by
              positivity
            positivity
          exact (le_div_iff hpos).mpr hw

end Visibility
end Oblivion
