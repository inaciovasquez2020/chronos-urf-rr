import Mathlib.Data.Real.Basic
import Mathlib.Data.Set.Basic

namespace Chronos

inductive LatentState : Type where
  | witness : LatentState
  | shadow : LatentState
  deriving DecidableEq

inductive Trace : Type where
  | empty : Trace
  deriving DecidableEq

def TraceProjection : LatentState → Trace :=
  fun _ => Trace.empty

theorem traceProjection_noninjective : ¬ Function.Injective TraceProjection := by
  intro hinj
  have h : LatentState.witness = LatentState.shadow := hinj rfl
  cases h

def EmptyTraceFiberNonempty (π : LatentState → Trace) : Prop :=
  ∃ d : LatentState, π d = Trace.empty

theorem trace_empty_not_absent : EmptyTraceFiberNonempty TraceProjection := by
  exact ⟨LatentState.witness, rfl⟩

def LatentTower (Q : LatentState → LatentState) (D0 : LatentState) : Nat → LatentState
  | 0 => D0
  | n + 1 => Q (LatentTower Q D0 n)

theorem latentTower_zero (Q : LatentState → LatentState) (D0 : LatentState) :
    LatentTower Q D0 0 = D0 := by
  rfl

theorem latentTower_succ (Q : LatentState → LatentState) (D0 : LatentState) (n : Nat) :
    LatentTower Q D0 (n + 1) = Q (LatentTower Q D0 n) := by
  rfl

structure EntropyModel where
  entropy : LatentState → ℝ
  mutualInfo : LatentState → Trace → ℝ

def EntropyLoss (M : EntropyModel) (D : LatentState) (R : Trace) : ℝ :=
  M.entropy D - M.mutualInfo D R

def EmptyTraceEntropyLoss (M : EntropyModel) (D : LatentState) : ℝ :=
  EntropyLoss M D Trace.empty

structure DynamicalSystem where
  State : Type
  evolution : State → State
  rankRate : Set (Set State) → Nat → ℝ
  fiberRank : ℝ
  fiberDimension : ℝ
  fiberEntropyMass : ℝ

def NonNullFiberWitness (sys : DynamicalSystem) : Prop :=
  sys.fiberRank > 0 ∧ sys.fiberDimension ≥ 1

def RateThickClass (lam : ℝ) (sys : DynamicalSystem) : Prop :=
  ∀ ρ : Set (Set sys.State),
    (∃ n : Nat, sys.rankRate ρ n > 0) →
    (∃ n : Nat, sys.rankRate ρ n ≥ lam)

def RankRateBridgeLaw (lam : ℝ) : Prop :=
  ∀ sys : DynamicalSystem,
    RateThickClass lam sys →
    ∀ ρ : Set (Set sys.State),
      (∃ n : Nat, sys.rankRate ρ n ≥ lam) →
      NonNullFiberWitness sys

def RateThickFiberCoercivity (lam : ℝ) : Prop :=
  ∃ κ : ℝ, κ > 0 ∧
    ∀ sys : DynamicalSystem,
      RateThickClass lam sys →
      NonNullFiberWitness sys →
      sys.fiberEntropyMass ≥ κ

theorem entropyFaithfulLowerEnvelope
    (lam : ℝ)
    (h_bridge : RankRateBridgeLaw lam)
    (h_coercivity : RateThickFiberCoercivity lam) :
    ∃ ε : ℝ, ε > 0 ∧
      ∀ sys : DynamicalSystem,
        RateThickClass lam sys →
        ∀ ρ : Set (Set sys.State),
          (∃ n : Nat, sys.rankRate ρ n ≥ lam) →
          sys.fiberEntropyMass ≥ ε := by
  rcases h_coercivity with ⟨κ, hκ_pos, hκ⟩
  refine ⟨κ, hκ_pos, ?_⟩
  intro sys hsys ρ h_rank
  exact hκ sys hsys (h_bridge sys hsys ρ h_rank)

theorem universalFiberEntropyGap
    (lam : ℝ)
    (h_bridge : RankRateBridgeLaw lam)
    (h_coercivity : RateThickFiberCoercivity lam) :
    ∃ ε : ℝ, ε > 0 ∧
      ∀ sys : DynamicalSystem,
        RateThickClass lam sys →
        ∀ ρ : Set (Set sys.State),
          (∃ n : Nat, sys.rankRate ρ n > 0) →
          sys.fiberEntropyMass ≥ ε := by
  rcases entropyFaithfulLowerEnvelope lam h_bridge h_coercivity with
    ⟨ε, hε_pos, hε⟩
  refine ⟨ε, hε_pos, ?_⟩
  intro sys hsys ρ h_pos
  exact hε sys hsys ρ (hsys ρ h_pos)


def PositiveEntropyAdmissibleClass
    (lam κ : ℝ)
    (sys : DynamicalSystem) : Prop :=
  RateThickClass lam sys ∧
    NonNullFiberWitness sys ∧
      sys.fiberEntropyMass ≥ κ

theorem rateThickFiberCoercivity_from_positiveEntropyAdmissibleClass
    (lam κ : ℝ)
    (hκ : κ > 0)
    (hadm :
      ∀ sys : DynamicalSystem,
        RateThickClass lam sys →
        NonNullFiberWitness sys →
        PositiveEntropyAdmissibleClass lam κ sys) :
    RateThickFiberCoercivity lam := by
  refine ⟨κ, hκ, ?_⟩
  intro sys hsys hnon
  exact (hadm sys hsys hnon).2.2

structure HyperbolicCoercivityCertificate (lam : ℝ) where
  coercivity : RateThickFiberCoercivity lam

theorem hyperbolicRoute
    (lam : ℝ)
    (cert : HyperbolicCoercivityCertificate lam) :
    RateThickFiberCoercivity lam :=
  cert.coercivity


theorem rateThickFiberCoercivity_refuted
    (lam : ℝ) :
    ¬ RateThickFiberCoercivity lam := by
  intro h
  rcases h with ⟨κ, hκ_pos, hκ⟩
  let bad : DynamicalSystem :=
    { State := PUnit
      evolution := fun x => x
      rankRate := fun _ _ => 0
      fiberRank := 1
      fiberDimension := 1
      fiberEntropyMass := 0 }
  have hRate : RateThickClass lam bad := by
    intro ρ hpos
    rcases hpos with ⟨n, hn⟩
    have hzero_pos : (0 : ℝ) > 0 := by
      simp at hn
      exact hn
    exact False.elim ((lt_irrefl (0 : ℝ)) hzero_pos)
  have hNonNull : NonNullFiberWitness bad := by
    constructor
    · exact zero_lt_one
    · exact le_refl (1 : ℝ)
  have hge : bad.fiberEntropyMass ≥ κ := hκ bad hRate hNonNull
  have hzero_ge : (0 : ℝ) ≥ κ := by
    simpa [bad] using hge
  exact (not_lt_of_ge hzero_ge) hκ_pos

end Chronos
