/-
Concrete analytic Einstein-matter estimate package target.

This module formalizes the exact analytic objects still missing after the
restricted gravity certificate stack:

  N(t): continuation norm
  B(t): bootstrap inequalities
  Q(t): concentration functional

It also isolates the two remaining analytic lemmas:

  RESTRICTED_CONCENTRATION_MONOTONICITY
  RESTRICTED_CONTINUATION_NORM_CONTROL

Boundary:
This does not prove the analytic Einstein-matter bootstrap package,
concrete analytic Einstein-matter estimate package, finite continuation norm,
bootstrap bounds, concentration monotonicity, threshold crossing,
gravity closure, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
-/

universe u v w

namespace Chronos
namespace Frontier

structure ConcreteAnalyticEinsteinMatterEstimateDatum where
  Time : Type u
  State : Type v
  Scalar : Type w
  leTime : Time → Time → Prop
  zeroTime : Time
  finalTime : Time
  triggerTime : Time
  continuationNormN : Time → State → Scalar
  bootstrapInequalitiesB : Time → State → Prop
  concentrationFunctionalQ : Time → State → Scalar
  thresholdQ : Scalar
  evolvesOnConcreteSeed : State → Prop
  localWellposedEvolution : State → Prop
  initialBootstrap : State → Prop
  belowTriggerTime : Time → Prop
  finiteContinuationNorm : Time → State → Prop
  concentrationMonotone : State → Prop
  thresholdCrossing : Time → State → Prop

def ContinuationNormFormalized
    (D : ConcreteAnalyticEinsteinMatterEstimateDatum) : Prop :=
  ∀ t : D.Time, ∀ s : D.State,
    D.evolvesOnConcreteSeed s →
    D.leTime D.zeroTime t →
    D.leTime t D.finalTime →
    D.finiteContinuationNorm t s

def BootstrapInequalitiesFormalized
    (D : ConcreteAnalyticEinsteinMatterEstimateDatum) : Prop :=
  ∀ t : D.Time, ∀ s : D.State,
    D.evolvesOnConcreteSeed s →
    D.leTime D.zeroTime t →
    D.leTime t D.finalTime →
    D.bootstrapInequalitiesB t s

def ConcentrationFunctionalFormalized
    (D : ConcreteAnalyticEinsteinMatterEstimateDatum) : Prop :=
  ∀ s : D.State,
    D.evolvesOnConcreteSeed s →
    D.concentrationMonotone s →
    D.thresholdCrossing D.triggerTime s

def RESTRICTED_CONCENTRATION_MONOTONICITY
    (D : ConcreteAnalyticEinsteinMatterEstimateDatum) : Prop :=
  ∀ s : D.State,
    D.evolvesOnConcreteSeed s →
    D.localWellposedEvolution s →
    D.initialBootstrap s →
    D.concentrationMonotone s

def RESTRICTED_CONTINUATION_NORM_CONTROL
    (D : ConcreteAnalyticEinsteinMatterEstimateDatum) : Prop :=
  ∀ t : D.Time, ∀ s : D.State,
    D.evolvesOnConcreteSeed s →
    D.localWellposedEvolution s →
    D.initialBootstrap s →
    D.leTime D.zeroTime t →
    D.leTime t D.finalTime →
    D.belowTriggerTime t →
    D.bootstrapInequalitiesB t s →
    D.finiteContinuationNorm t s

theorem restricted_continuation_norm_control_of_finite_continuation_norm_estimate
    {D : ConcreteAnalyticEinsteinMatterEstimateDatum}
    (h :
      ∀ t : D.Time,
      ∀ s : D.State,
        D.evolvesOnConcreteSeed s →
        D.localWellposedEvolution s →
        D.initialBootstrap s →
        D.leTime D.zeroTime t →
        D.leTime t D.finalTime →
        D.belowTriggerTime t →
        D.bootstrapInequalitiesB t s →
        D.finiteContinuationNorm t s) :
    RESTRICTED_CONTINUATION_NORM_CONTROL D := by
  intro t s hs hwell hinit ht0 htT hbelow hboot
  exact h t s hs hwell hinit ht0 htT hbelow hboot

def ConcreteAnalyticEinsteinMatterEstimatePackage
    (D : ConcreteAnalyticEinsteinMatterEstimateDatum) : Prop :=
  ∀ s : D.State,
    D.evolvesOnConcreteSeed s →
    D.localWellposedEvolution s →
    D.initialBootstrap s →
    (∀ t : D.Time,
      D.leTime D.zeroTime t →
      D.leTime t D.finalTime →
      D.belowTriggerTime t →
      D.bootstrapInequalitiesB t s →
      D.finiteContinuationNorm t s)
    ∧
    (∀ t : D.Time,
      D.leTime D.zeroTime t →
      D.leTime t D.finalTime →
      D.bootstrapInequalitiesB t s)
    ∧
    D.concentrationMonotone s
    ∧
    D.thresholdCrossing D.triggerTime s

structure ConcreteAnalyticEinsteinMatterEstimatePackageTarget
    (D : ConcreteAnalyticEinsteinMatterEstimateDatum) where
  restricted_concentration_monotonicity :
    RESTRICTED_CONCENTRATION_MONOTONICITY D
  restricted_continuation_norm_control :
    RESTRICTED_CONTINUATION_NORM_CONTROL D
  bootstrap_persistence :
    ∀ t : D.Time, ∀ s : D.State,
      D.evolvesOnConcreteSeed s →
      D.localWellposedEvolution s →
      D.initialBootstrap s →
      D.leTime D.zeroTime t →
      D.leTime t D.finalTime →
      D.bootstrapInequalitiesB t s
  threshold_crossing :
    ∀ s : D.State,
      D.evolvesOnConcreteSeed s →
      D.localWellposedEvolution s →
      D.initialBootstrap s →
      D.thresholdCrossing D.triggerTime s

theorem concrete_analytic_einstein_matter_estimate_package_of_target
    {D : ConcreteAnalyticEinsteinMatterEstimateDatum}
    (target : ConcreteAnalyticEinsteinMatterEstimatePackageTarget D) :
    ConcreteAnalyticEinsteinMatterEstimatePackage D := by
  intro s hs hwell hinit
  exact ⟨
    fun t ht0 htT hbelow hboot =>
      target.restricted_continuation_norm_control t s hs hwell hinit ht0 htT hbelow hboot,
    fun t ht0 htT =>
      target.bootstrap_persistence t s hs hwell hinit ht0 htT,
    target.restricted_concentration_monotonicity s hs hwell hinit,
    target.threshold_crossing s hs hwell hinit
  ⟩

theorem finite_continuation_norm_of_target
    {D : ConcreteAnalyticEinsteinMatterEstimateDatum}
    (target : ConcreteAnalyticEinsteinMatterEstimatePackageTarget D)
    (s : D.State)
    (hs : D.evolvesOnConcreteSeed s)
    (hwell : D.localWellposedEvolution s)
    (hinit : D.initialBootstrap s)
    (t : D.Time)
    (ht0 : D.leTime D.zeroTime t)
    (htT : D.leTime t D.finalTime)
    (hbelow : D.belowTriggerTime t)
    (hboot : D.bootstrapInequalitiesB t s) :
    D.finiteContinuationNorm t s :=
  target.restricted_continuation_norm_control t s hs hwell hinit ht0 htT hbelow hboot

theorem concentration_monotone_of_target
    {D : ConcreteAnalyticEinsteinMatterEstimateDatum}
    (target : ConcreteAnalyticEinsteinMatterEstimatePackageTarget D)
    (s : D.State)
    (hs : D.evolvesOnConcreteSeed s)
    (hwell : D.localWellposedEvolution s)
    (hinit : D.initialBootstrap s) :
    D.concentrationMonotone s :=
  target.restricted_concentration_monotonicity s hs hwell hinit

end Frontier
end Chronos
