import Chronos.Frontier.ReggeWheelerBoundedPotentialResponse

namespace Chronos.Frontier

noncomputable section

/-!
# Finite soft-memory backreaction on ordered hard emission

This module records the corrected finite-dimensional endpoint of the
soft-memory backreaction construction.

The conclusions are deliberately restricted:

* a qubit soft sector can carry an angularly indexed operator field through
  four real Pauli-component profiles;
* the closed-sphere integration-by-parts step is represented by
  self-adjointness of the angular Laplacian pairing;
* overlapping memory-controlled emission steps must be composed in temporal
  order;
* noncommutativity does not destroy norm preservation or invertibility when
  every ordered step is independently certified;
* charge conservation follows for the ordered product only when every step
  is certified to commute with the same charge;
* no hard-radiation purification, coherent-information increase, or
  Page-curve turnover is proved.
-/

/--
Finite Pauli-component representation of an angularly indexed Hermitian
operator field on one soft qubit.

The four real functions are the coefficients of the identity and the three
Pauli matrices. A two-dimensional Hilbert space therefore permits
angle-dependent operator coefficients, while retaining only four operator
directions at each angle.
-/
structure FiniteQubitAngularMemoryField
    (AngularPoint : Type*) where
  identityProfile : AngularPoint → ℝ
  xProfile : AngularPoint → ℝ
  yProfile : AngularPoint → ℝ
  zProfile : AngularPoint → ℝ

/--
A soft-memory field is phase sensitive when an off-diagonal Pauli component
is nonzero somewhere.
-/
def FiniteQubitAngularMemoryField.PhaseSensitive
    {AngularPoint : Type*}
    (field :
      FiniteQubitAngularMemoryField AngularPoint) :
    Prop :=
  (∃ point, field.xProfile point ≠ 0) ∨
    (∃ point, field.yProfile point ≠ 0)

/--
The fixed-profile number-operator model.

This carrier has no `x` or `y` component, so it can encode occupation of a
fixed angular profile but not qubit phase coherence.
-/
def finiteFixedNumberProfileMemory
    {AngularPoint : Type*}
    (profile : AngularPoint → ℝ) :
    FiniteQubitAngularMemoryField AngularPoint where
  identityProfile :=
    fun point => profile point / 2
  xProfile :=
    fun _ => 0
  yProfile :=
    fun _ => 0
  zProfile :=
    fun point => -(profile point / 2)

/--
Abstract closed-sphere Laplacian and overlap pairing.

The field `selfAdjoint` is the corrected integration-by-parts statement.
There is no boundary contribution because the intended manifold is closed.
-/
structure ClosedAngularLaplacianPairing
    (AngularField : Type*) where
  laplacian : AngularField → AngularField
  overlap : AngularField → AngularField → ℝ
  selfAdjoint :
    ∀ left right,
      overlap (laplacian left) right =
        overlap left (laplacian right)

theorem closedAngularLaplacian_transfer
    {AngularField : Type*}
    (pairing :
      ClosedAngularLaplacianPairing AngularField)
    (memoryProfile radiationProfile : AngularField) :
    pairing.overlap
          (pairing.laplacian memoryProfile)
          radiationProfile =
      pairing.overlap
          memoryProfile
          (pairing.laplacian radiationProfile) :=
  pairing.selfAdjoint
    memoryProfile
    radiationProfile

/--
One memory-controlled evolution step.

The evolution is supplied together with its inverse, norm-preservation
certificate, and charge-commutation certificate. This avoids assuming that
an unspecified operator exponential is automatically well-defined.
-/
structure FiniteMemoryControlledUnitaryStep
    (State : Type*)
    [NormedAddCommGroup State]
    [NormedSpace ℂ State]
    (charge : State →ₗ[ℂ] State) where
  evolution : State →ₗ[ℂ] State
  inverse : State →ₗ[ℂ] State
  leftInverse :
    ∀ state,
      inverse (evolution state) = state
  rightInverse :
    ∀ state,
      evolution (inverse state) = state
  normPreserving :
    ∀ state,
      ‖evolution state‖ = ‖state‖
  chargeCommuting :
    ∀ state,
      evolution (charge state) =
        charge (evolution state)

/--
Temporally ordered evolution.

For a list `[U₁, U₂, ..., Uₙ]`, this applies `U₁` first and `Uₙ` last:

`Uₙ ∘ ... ∘ U₂ ∘ U₁`.
-/
def finiteOrderedMemoryEvolution
    {State : Type*}
    [NormedAddCommGroup State]
    [NormedSpace ℂ State]
    {charge : State →ₗ[ℂ] State} :
    List
      (FiniteMemoryControlledUnitaryStep
        State
        charge) →
      State →ₗ[ℂ] State
  | [] =>
      LinearMap.id
  | step :: rest =>
      (finiteOrderedMemoryEvolution rest).comp
        step.evolution

/--
Inverse of the temporally ordered evolution, applied in reverse order.
-/
def finiteOrderedMemoryInverse
    {State : Type*}
    [NormedAddCommGroup State]
    [NormedSpace ℂ State]
    {charge : State →ₗ[ℂ] State} :
    List
      (FiniteMemoryControlledUnitaryStep
        State
        charge) →
      State →ₗ[ℂ] State
  | [] =>
      LinearMap.id
  | step :: rest =>
      step.inverse.comp
        (finiteOrderedMemoryInverse rest)

theorem finiteOrderedMemoryEvolution_norm
    {State : Type*}
    [NormedAddCommGroup State]
    [NormedSpace ℂ State]
    {charge : State →ₗ[ℂ] State}
    (steps :
      List
        (FiniteMemoryControlledUnitaryStep
          State
          charge))
    (state : State) :
    ‖finiteOrderedMemoryEvolution steps state‖ =
      ‖state‖ := by
  induction steps generalizing state with
  | nil =>
      rfl
  | cons step rest ih =>
      change
        ‖finiteOrderedMemoryEvolution
            rest
            (step.evolution state)‖ =
          ‖state‖
      rw [ih]
      exact step.normPreserving state

theorem finiteOrderedMemoryInverse_left
    {State : Type*}
    [NormedAddCommGroup State]
    [NormedSpace ℂ State]
    {charge : State →ₗ[ℂ] State}
    (steps :
      List
        (FiniteMemoryControlledUnitaryStep
          State
          charge))
    (state : State) :
    finiteOrderedMemoryInverse
          steps
          (finiteOrderedMemoryEvolution
            steps
            state) =
      state := by
  induction steps generalizing state with
  | nil =>
      rfl
  | cons step rest ih =>
      change
        step.inverse
            (finiteOrderedMemoryInverse
              rest
              (finiteOrderedMemoryEvolution
                rest
                (step.evolution state))) =
          state
      rw [ih]
      exact step.leftInverse state

theorem finiteOrderedMemoryInverse_right
    {State : Type*}
    [NormedAddCommGroup State]
    [NormedSpace ℂ State]
    {charge : State →ₗ[ℂ] State}
    (steps :
      List
        (FiniteMemoryControlledUnitaryStep
          State
          charge))
    (state : State) :
    finiteOrderedMemoryEvolution
          steps
          (finiteOrderedMemoryInverse
            steps
            state) =
      state := by
  induction steps generalizing state with
  | nil =>
      rfl
  | cons step rest ih =>
      change
        finiteOrderedMemoryEvolution
            rest
            (step.evolution
              (step.inverse
                (finiteOrderedMemoryInverse
                  rest
                  state))) =
          state
      rw [step.rightInverse]
      exact ih state

/--
Charge conservation for the complete ordered evolution.

No pairwise commutativity between distinct evolution steps is required.
Each step must commute with the same total charge.
-/
theorem finiteOrderedMemoryEvolution_charge
    {State : Type*}
    [NormedAddCommGroup State]
    [NormedSpace ℂ State]
    {charge : State →ₗ[ℂ] State}
    (steps :
      List
        (FiniteMemoryControlledUnitaryStep
          State
          charge))
    (state : State) :
    finiteOrderedMemoryEvolution
          steps
          (charge state) =
      charge
        (finiteOrderedMemoryEvolution
          steps
          state) := by
  induction steps generalizing state with
  | nil =>
      rfl
  | cons step rest ih =>
      change
        finiteOrderedMemoryEvolution
            rest
            (step.evolution
              (charge state)) =
          charge
            (finiteOrderedMemoryEvolution
              rest
              (step.evolution state))
      rw [step.chargeCommuting]
      exact ih (step.evolution state)

/--
Pointwise formulation of whether two evolution generators commute.

The ordered-evolution theorems above do not assume this proposition.
-/
def finiteEvolutionOperatorsCommute
    {State : Type*}
    [NormedAddCommGroup State]
    [NormedSpace ℂ State]
    (left right : State →ₗ[ℂ] State) :
    Prop :=
  left.comp right =
    right.comp left

/--
Abstract carrier for the hard-only reduced state.

No partial-trace construction or entropy theorem is supplied here.
-/
structure FiniteHardOnlyReductionCarrier
    (GlobalState HardState : Type*) where
  initialState : GlobalState
  evolvedState : Nat → GlobalState
  reducedHardState : Nat → HardState

/--
A certificate that would be sufficient to establish one strict entropy
turnover step.

No inhabitant is constructed in this module.
-/
structure FiniteHardEntropyTurnoverCertificate
    (HardState : Type*) where
  entropy : HardState → ℝ
  reducedHardState : Nat → HardState
  turnoverBin : Nat
  turnover :
    entropy
          (reducedHardState
            (turnoverBin + 1)) <
      entropy
        (reducedHardState turnoverBin)

def finiteSoftMemoryBackreactionStatus : String :=
  "FINITE_SOFT_MEMORY_ORDERED_EVOLUTION_CORRECTED"

def finiteSoftMemoryBackreactionProved : String :=
  "ORDERED_CERTIFIED_STEPS_PRESERVE_NORM_HAVE_TWO_SIDED_INVERSE_AND_CONSERVE_CERTIFIED_CHARGE"

def finiteSoftMemoryBackreactionBoundary : String :=
  "NO_HAMILTONIAN_EXPONENTIAL_CONSTRUCTION_NO_CHARGE_COMPENSATION_NO_HARD_REDUCED_STATE_CALCULATION_NO_PAGE_TURNOVER_CERTIFICATE"

end

end Chronos.Frontier
