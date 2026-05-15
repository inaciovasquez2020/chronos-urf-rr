namespace Chronos
namespace Frontier

/--
Weakest admissibility axiom for unrestricted operational boundary compactness.

This axiom does not assert a collapse theorem.
It only states that the non-collapsed admissible state space has finite
recoverable boundary energy at fixed region and fixed resolution.
-/
structure FiniteNonCollapsedEnergyBudgetInput where
  Region : Type
  State : Type
  Mode : Type
  boundaryEnergy : Region → State → Nat
  admissible : Region → State → Prop
  energyBudget : Region → Nat
  finiteNonCollapsedEnergyBudget :
    ∀ (R : Region) (ψ : State),
      admissible R ψ →
      boundaryEnergy R ψ ≤ energyBudget R

/--
Boundary spectral structure.

`spectralCountingBound` records the finite-counting witness numerically.
The compactness theorem below only needs the resulting modal cutoff; the
finite-counting witness is retained as part of the status surface.
-/
structure BoundarySpectralInput
    (I : FiniteNonCollapsedEnergyBudgetInput) where
  eigenvalue : I.Mode → Nat
  spectralCountingBound : Nat → Nat
  finiteSpectralCountingWitness : ∀ (Λ : Nat), True

/--
Operational mode-energy structure.

The modal growth hypothesis is normalized to:

    eigenvalue k <= energyRequired R ψ k

This is the weakest Nat-valued form needed for the repository-native compactness
cutoff. Real-valued constants such as c_epsilon can be restored in an analytic
layer above this formal surface.
-/
structure BoundaryModeEnergyInput
    (I : FiniteNonCollapsedEnergyBudgetInput)
    (S : BoundarySpectralInput I) where
  energyRequired : I.Region → I.State → I.Mode → Nat
  resolvable : I.Region → I.State → I.Mode → Prop
  energyAccounting :
    ∀ (R : I.Region) (ψ : I.State) (k : I.Mode),
      I.admissible R ψ →
      resolvable R ψ k →
      energyRequired R ψ k ≤ I.boundaryEnergy R ψ
  normalizedResolvedModeEnergyGrowth :
    ∀ (R : I.Region) (ψ : I.State) (k : I.Mode),
      I.admissible R ψ →
      resolvable R ψ k →
      S.eigenvalue k ≤ energyRequired R ψ k

/--
Finite resolution bin structure.

This records the positive-bin/finite-resolution side separately from the modal
cutoff theorem. The repository-native compactness cutoff uses only the modal
bound; finite bin counts are retained as the detector-alphabet layer.
-/
structure FiniteResolutionBinInput
    (I : FiniteNonCollapsedEnergyBudgetInput)
    (S : BoundarySpectralInput I)
    (E : BoundaryModeEnergyInput I S) where
  binCount : I.Region → I.State → I.Mode → Nat
  finiteResolutionBins :
    ∀ (R : I.Region) (ψ : I.State) (k : I.Mode),
      I.admissible R ψ →
      E.resolvable R ψ k →
      binCount R ψ k ≤ I.energyBudget R + 1

/--
Operational detector algebra has a finite spectral cutoff at fixed region,
state, and resolution surface.
-/
def OperationalDetectorAlgebraFinite
    (I : FiniteNonCollapsedEnergyBudgetInput)
    (S : BoundarySpectralInput I)
    (E : BoundaryModeEnergyInput I S)
    (_B : FiniteResolutionBinInput I S E) : Prop :=
  ∀ (R : I.Region) (ψ : I.State),
    I.admissible R ψ →
    ∃ Λ : Nat,
      ∀ (k : I.Mode),
        E.resolvable R ψ k →
        S.eigenvalue k ≤ Λ

/--
Unrestricted UniversalBoundaryCompactness is conditional on
FiniteNonCollapsedEnergyBudget.
-/
def UniversalBoundaryCompactnessConditional
    (I : FiniteNonCollapsedEnergyBudgetInput)
    (S : BoundarySpectralInput I)
    (E : BoundaryModeEnergyInput I S)
    (B : FiniteResolutionBinInput I S E) : Prop :=
  OperationalDetectorAlgebraFinite I S E B

/--
Compactness theorem relative to the weakest admissibility axiom.
-/
theorem compactness_from_finite_noncollapsed_energy_budget
    (I : FiniteNonCollapsedEnergyBudgetInput)
    (S : BoundarySpectralInput I)
    (E : BoundaryModeEnergyInput I S)
    (B : FiniteResolutionBinInput I S E) :
    UniversalBoundaryCompactnessConditional I S E B := by
  intro R ψ hψ
  refine ⟨I.energyBudget R, ?_⟩
  intro k hk
  have h_growth :
      S.eigenvalue k ≤ E.energyRequired R ψ k :=
    E.normalizedResolvedModeEnergyGrowth R ψ k hψ hk
  have h_account :
      E.energyRequired R ψ k ≤ I.boundaryEnergy R ψ :=
    E.energyAccounting R ψ k hψ hk
  have h_budget :
      I.boundaryEnergy R ψ ≤ I.energyBudget R :=
    I.finiteNonCollapsedEnergyBudget R ψ hψ
  exact Nat.le_trans h_growth (Nat.le_trans h_account h_budget)

/--
Spherical Misner-Sharp closure is a restricted source of
FiniteNonCollapsedEnergyBudget.
-/
structure SphericalMisnerSharpClosureInput where
  Region : Type
  State : Type
  admissible : Region → State → Prop
  boundaryEnergy : Region → State → Nat
  circularEnergyThreshold : Region → Nat
  restrictedCollapseExclusion :
    ∀ (R : Region) (ψ : State),
      admissible R ψ →
      boundaryEnergy R ψ ≤ circularEnergyThreshold R

def spherical_misner_sharp_induces_finite_budget
    (Q : SphericalMisnerSharpClosureInput) :
    FiniteNonCollapsedEnergyBudgetInput where
  Region := Q.Region
  State := Q.State
  Mode := Nat
  boundaryEnergy := Q.boundaryEnergy
  admissible := Q.admissible
  energyBudget := Q.circularEnergyThreshold
  finiteNonCollapsedEnergyBudget := Q.restrictedCollapseExclusion

/--
Nonspherical finite-energy closure is separate from spherical Misner-Sharp
closure. It assumes the finite budget directly.
-/
structure NonsphericalFiniteEnergyClosureInput where
  Region : Type
  State : Type
  Mode : Type
  admissible : Region → State → Prop
  boundaryEnergy : Region → State → Nat
  energyBudget : Region → Nat
  finiteEnergyAxiom :
    ∀ (R : Region) (ψ : State),
      admissible R ψ →
      boundaryEnergy R ψ ≤ energyBudget R

def nonspherical_finite_energy_induces_budget
    (Q : NonsphericalFiniteEnergyClosureInput) :
    FiniteNonCollapsedEnergyBudgetInput where
  Region := Q.Region
  State := Q.State
  Mode := Q.Mode
  boundaryEnergy := Q.boundaryEnergy
  admissible := Q.admissible
  energyBudget := Q.energyBudget
  finiteNonCollapsedEnergyBudget := Q.finiteEnergyAxiom

/--
Open strengthening.

QL_CollapseGate is stronger than the finite-energy admissibility axiom:
it attempts to derive finite admissible energy from a geometric collapse theorem.
-/
structure QLCollapseGateOpenFrontier where
  Region : Type
  State : Type
  boundaryEnergy : Region → State → Nat
  quasiLocalThreshold : Region → Nat
  trappedOrExcluded : Region → State → Prop
  qlCollapseGate :
    ∀ (R : Region) (ψ : State),
      quasiLocalThreshold R < boundaryEnergy R ψ →
      trappedOrExcluded R ψ

/--
Final status marker.

Unrestricted boundary compactness is not closed unconditionally.
It is closed only relative to FiniteNonCollapsedEnergyBudget.
-/
def UnrestrictedUniversalBoundaryCompactnessStatus : String :=
  "CONDITIONAL_ON_FINITE_NONCOLLAPSED_ENERGY_BUDGET"

end Frontier
end Chronos
