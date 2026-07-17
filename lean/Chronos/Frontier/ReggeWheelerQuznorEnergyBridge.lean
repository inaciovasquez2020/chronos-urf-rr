import Mathlib

namespace Chronos.Frontier

noncomputable section

/-!
# Regge–Wheeler–Quznor energy bridge

This module separates the proved algebraic content from the remaining
geometric and analytic assumptions.

Corrections encoded here:

* the Regge–Wheeler flux is `-ψₜ ψₓ`, not an ordered pair;
* the potential used in the energy integral is explicitly a function of the
  tortoise coordinate;
* global energy conservation is derived only from an integrated balance law
  with zero accumulated boundary flux;
* equality with standard GR is conditional on uniqueness for the same
  equation and initial data;
* the Quznor scaling `C N = N * O N` is definitional and has no independent
  physical content;
* the Regge–Wheeler-to-soft relation remains an uninhabited calibration
  ansatz;
* gauge invariance does not establish that the energy is a scalar-curvature
  invariant.
-/

/-- Normalized `ℓ = 2` Regge–Wheeler potential. -/
def rwNormalizedL2Potential (x : ℝ) : ℝ :=
  6 * (x - 2) * (x - 1) / x ^ 4

/-- Exterior critical-radius candidate. -/
def rwPeakCandidate : ℝ :=
  (9 + Real.sqrt 17) / 4

/-- Non-exterior critical-radius candidate. -/
def rwInnerCriticalCandidate : ℝ :=
  (9 - Real.sqrt 17) / 4

private theorem sqrt17_sq :
    (Real.sqrt (17 : ℝ)) ^ 2 = 17 := by
  norm_num

private theorem sqrt17_gt_three :
    3 < Real.sqrt (17 : ℝ) := by
  have hsqrt_nonneg :
      0 ≤ Real.sqrt (17 : ℝ) :=
    Real.sqrt_nonneg 17
  nlinarith [sqrt17_sq]

theorem rwPeakCandidate_quadratic :
    2 * rwPeakCandidate ^ 2 -
        9 * rwPeakCandidate + 8 = 0 := by
  unfold rwPeakCandidate
  nlinarith [sqrt17_sq]

theorem rwInnerCriticalCandidate_quadratic :
    2 * rwInnerCriticalCandidate ^ 2 -
        9 * rwInnerCriticalCandidate + 8 = 0 := by
  unfold rwInnerCriticalCandidate
  nlinarith [sqrt17_sq]

theorem rwInnerCriticalCandidate_lt_two :
    rwInnerCriticalCandidate < 2 := by
  unfold rwInnerCriticalCandidate
  linarith [sqrt17_gt_three]

theorem rwPeakCandidate_gt_three :
    3 < rwPeakCandidate := by
  unfold rwPeakCandidate
  linarith [sqrt17_gt_three]

theorem rwPeakCandidate_gt_two :
    2 < rwPeakCandidate := by
  linarith [rwPeakCandidate_gt_three]

/--
Positive polynomial appearing in the exact difference between the potential
at the peak candidate and at an arbitrary exterior point.
-/
def rwPeakComparisonPolynomial (x : ℝ) : ℝ :=
  (3 * rwPeakCandidate - 4) * x ^ 2 +
    (19 * rwPeakCandidate - 24) * x +
    16 - 18 * rwPeakCandidate

theorem rwPeakComparisonPolynomial_decomposition
    (x : ℝ) :
    rwPeakComparisonPolynomial x =
      16 * (2 * rwPeakCandidate - 3) +
        (x - 2) *
          ((3 * rwPeakCandidate - 4) * (x + 2) +
            (19 * rwPeakCandidate - 24)) := by
  unfold rwPeakComparisonPolynomial
  ring

theorem rwPeakComparisonPolynomial_pos
    {x : ℝ}
    (hx : 2 < x) :
    0 < rwPeakComparisonPolynomial x := by
  have hPeak : 3 < rwPeakCandidate :=
    rwPeakCandidate_gt_three
  have hFirst : 0 < 2 * rwPeakCandidate - 3 := by
    linarith
  have hCoefficient : 0 < 3 * rwPeakCandidate - 4 := by
    linarith
  have hxPlus : 0 < x + 2 := by
    linarith
  have hProduct :
      0 <
        (3 * rwPeakCandidate - 4) * (x + 2) :=
    mul_pos hCoefficient hxPlus
  have hSecond : 0 < 19 * rwPeakCandidate - 24 := by
    linarith
  have hBracket :
      0 <
        (3 * rwPeakCandidate - 4) * (x + 2) +
          (19 * rwPeakCandidate - 24) :=
    add_pos hProduct hSecond
  have hxMinus : 0 < x - 2 := by
    linarith
  have hTail :
      0 <
        (x - 2) *
          ((3 * rwPeakCandidate - 4) * (x + 2) +
            (19 * rwPeakCandidate - 24)) :=
    mul_pos hxMinus hBracket
  rw [rwPeakComparisonPolynomial_decomposition]
  exact add_pos
    (mul_pos (by norm_num) hFirst)
    hTail

/--
Exact nonnegative factorization of the difference between the normalized
potential at the peak candidate and at an exterior point.
-/
theorem rwNormalizedL2Potential_peakDifference
    (x : ℝ)
    (hx : x ≠ 0) :
    rwNormalizedL2Potential rwPeakCandidate -
        rwNormalizedL2Potential x =
      3 * (x - rwPeakCandidate) ^ 2 *
          rwPeakComparisonPolynomial x /
        (rwPeakCandidate ^ 4 * x ^ 4) := by
  have hPeakNe : rwPeakCandidate ≠ 0 := by
    exact ne_of_gt (lt_trans (by norm_num) rwPeakCandidate_gt_three)
  have hzero :
      rwNormalizedL2Potential rwPeakCandidate -
          rwNormalizedL2Potential x -
          3 * (x - rwPeakCandidate) ^ 2 *
              rwPeakComparisonPolynomial x /
            (rwPeakCandidate ^ 4 * x ^ 4) = 0 := by
    calc
      rwNormalizedL2Potential rwPeakCandidate -
            rwNormalizedL2Potential x -
            3 * (x - rwPeakCandidate) ^ 2 *
                rwPeakComparisonPolynomial x /
              (rwPeakCandidate ^ 4 * x ^ 4) =
          3 * (x - rwPeakCandidate) *
              (2 * rwPeakCandidate ^ 2 -
                9 * rwPeakCandidate + 8) *
              (rwPeakCandidate * x ^ 2 -
                3 * rwPeakCandidate * x +
                2 * rwPeakCandidate +
                x ^ 3 + 3 * x ^ 2 - 2 * x) /
            (rwPeakCandidate ^ 4 * x ^ 4) := by
        unfold rwNormalizedL2Potential
        unfold rwPeakComparisonPolynomial
        field_simp [hPeakNe, hx]
        ring
      _ = 0 := by
        rw [rwPeakCandidate_quadratic]
        simp
  linarith

theorem rwNormalizedL2Potential_le_peak
    {x : ℝ}
    (hx : 2 < x) :
    rwNormalizedL2Potential x ≤
      rwNormalizedL2Potential rwPeakCandidate := by
  have hxPos : 0 < x := by
    linarith
  have hPeakPos : 0 < rwPeakCandidate := by
    linarith [rwPeakCandidate_gt_three]
  have hPolynomial :
      0 < rwPeakComparisonPolynomial x :=
    rwPeakComparisonPolynomial_pos hx
  have hNumerator :
      0 ≤
        3 * (x - rwPeakCandidate) ^ 2 *
          rwPeakComparisonPolynomial x :=
    mul_nonneg
      (mul_nonneg (by norm_num) (sq_nonneg _))
      (le_of_lt hPolynomial)
  have hDenominator :
      0 < rwPeakCandidate ^ 4 * x ^ 4 :=
    mul_pos
      (pow_pos hPeakPos 4)
      (pow_pos hxPos 4)
  have hFraction :
      0 ≤
        3 * (x - rwPeakCandidate) ^ 2 *
            rwPeakComparisonPolynomial x /
          (rwPeakCandidate ^ 4 * x ^ 4) :=
    div_nonneg hNumerator (le_of_lt hDenominator)
  have hDifference :=
    rwNormalizedL2Potential_peakDifference
      x
      (ne_of_gt hxPos)
  linarith

theorem rwNormalizedL2Potential_lt_peak_of_ne
    {x : ℝ}
    (hx : 2 < x)
    (hne : x ≠ rwPeakCandidate) :
    rwNormalizedL2Potential x <
      rwNormalizedL2Potential rwPeakCandidate := by
  have hxPos : 0 < x := by
    linarith
  have hPeakPos : 0 < rwPeakCandidate := by
    linarith [rwPeakCandidate_gt_three]
  have hPolynomial :
      0 < rwPeakComparisonPolynomial x :=
    rwPeakComparisonPolynomial_pos hx
  have hSquare :
      0 < (x - rwPeakCandidate) ^ 2 :=
    sq_pos_of_ne_zero (sub_ne_zero.mpr hne)
  have hNumerator :
      0 <
        3 * (x - rwPeakCandidate) ^ 2 *
          rwPeakComparisonPolynomial x :=
    mul_pos
      (mul_pos (by norm_num) hSquare)
      hPolynomial
  have hDenominator :
      0 < rwPeakCandidate ^ 4 * x ^ 4 :=
    mul_pos
      (pow_pos hPeakPos 4)
      (pow_pos hxPos 4)
  have hFraction :
      0 <
        3 * (x - rwPeakCandidate) ^ 2 *
            rwPeakComparisonPolynomial x /
          (rwPeakCandidate ^ 4 * x ^ 4) :=
    div_pos hNumerator hDenominator
  have hDifference :=
    rwNormalizedL2Potential_peakDifference
      x
      (ne_of_gt hxPos)
  linarith

/-- A point is the unique global maximizer of `f` on `domain`. -/
def IsUniqueGlobalMaximumOn
    (f : ℝ → ℝ)
    (domain : Set ℝ)
    (x₀ : ℝ) : Prop :=
  x₀ ∈ domain ∧
    ∀ x, x ∈ domain →
      f x ≤ f x₀ ∧
        (f x = f x₀ → x = x₀)

theorem rwNormalizedL2Potential_uniqueMaximum :
    IsUniqueGlobalMaximumOn
      rwNormalizedL2Potential
      (Set.Ioi 2)
      rwPeakCandidate := by
  constructor
  · exact rwPeakCandidate_gt_two
  · intro x hx
    constructor
    · exact rwNormalizedL2Potential_le_peak hx
    · intro heq
      by_contra hne
      have hlt :=
        rwNormalizedL2Potential_lt_peak_of_ne hx hne
      linarith

/--
Physical `ℓ = 2` potential, written as the normalized potential divided by
`M²`. This definition makes the scaling relation explicit.
-/
def reggeWheelerL2Potential
    (M r : ℝ) : ℝ :=
  rwNormalizedL2Potential (r / M) / M ^ 2

theorem reggeWheelerL2Potential_eq_closedForm
    {M r : ℝ}
    (hM : M ≠ 0)
    (hr : r ≠ 0) :
    reggeWheelerL2Potential M r =
      6 * (r - 2 * M) * (r - M) / r ^ 4 := by
  unfold reggeWheelerL2Potential
  unfold rwNormalizedL2Potential
  field_simp [hM, hr]

def rwPeakRadius (M : ℝ) : ℝ :=
  M * rwPeakCandidate

theorem rwRadiusOrdering
    {M : ℝ}
    (hM : 0 < M) :
    2 * M < 3 * M ∧
      3 * M < rwPeakRadius M := by
  constructor
  · nlinarith
  · unfold rwPeakRadius
    simpa [mul_comm] using
      (mul_lt_mul_of_pos_right
        rwPeakCandidate_gt_three
        hM)

theorem reggeWheelerL2Potential_uniqueMaximum
    (M : ℝ)
    (hM : 0 < M) :
    IsUniqueGlobalMaximumOn
      (reggeWheelerL2Potential M)
      (Set.Ioi (2 * M))
      (rwPeakRadius M) := by
  have hMNe : M ≠ 0 := ne_of_gt hM
  have hM2 : 0 < M ^ 2 := sq_pos_of_pos hM
  have hPeakRatio :
      rwPeakRadius M / M = rwPeakCandidate := by
    unfold rwPeakRadius
    field_simp [hMNe]
  constructor
  · have hScaled :=
      mul_lt_mul_of_pos_left
        rwPeakCandidate_gt_two
        hM
    simpa [rwPeakRadius, mul_comm] using hScaled
  · intro r hr
    have hx : 2 < r / M :=
      (lt_div_iff₀ hM).2 hr
    have hle :=
      rwNormalizedL2Potential_le_peak hx
    constructor
    · unfold reggeWheelerL2Potential
      rw [hPeakRatio]
      exact
        (div_le_div_iff_of_pos_right hM2).2 hle
    · intro heq
      by_contra hne
      have hxne : r / M ≠ rwPeakCandidate := by
        intro hratio
        apply hne
        have hrEq :
            r = rwPeakCandidate * M :=
          (div_eq_iff hMNe).mp hratio
        simpa [rwPeakRadius, mul_comm] using hrEq
      have hlt :=
        rwNormalizedL2Potential_lt_peak_of_ne
          hx
          hxne
      have hScaledLt :
          rwNormalizedL2Potential (r / M) / M ^ 2 <
            rwNormalizedL2Potential rwPeakCandidate / M ^ 2 :=
        (div_lt_div_iff_of_pos_right hM2).2 hlt
      unfold reggeWheelerL2Potential at heq
      rw [hPeakRatio] at heq
      linarith

/--
Pointwise odd-parity data sufficient to verify the algebraic gauge
cancellation. `radialH₂` represents `(rₐ / r) h₂`.
-/
structure OddParityGaugeJet where
  h : ℝ
  derivativeH₂ : ℝ
  radialH₂ : ℝ

/--
Pointwise gauge-parameter data. `radialLambda` represents
`(rₐ / r) Λ`.
-/
structure OddParityGaugeParameterJet where
  derivativeLambda : ℝ
  radialLambda : ℝ

def oddParityGaugeTransform
    (q : OddParityGaugeJet)
    (g : OddParityGaugeParameterJet) :
    OddParityGaugeJet where
  h :=
    q.h - g.derivativeLambda +
      2 * g.radialLambda
  derivativeH₂ :=
    q.derivativeH₂ -
      2 * g.derivativeLambda
  radialH₂ :=
    q.radialH₂ -
      2 * g.radialLambda

def oddParityInvariantCombination
    (q : OddParityGaugeJet) : ℝ :=
  q.h -
    (1 / 2 : ℝ) * q.derivativeH₂ +
    q.radialH₂

theorem oddParityInvariantCombination_gaugeInvariant
    (q : OddParityGaugeJet)
    (g : OddParityGaugeParameterJet) :
    oddParityInvariantCombination
        (oddParityGaugeTransform q g) =
      oddParityInvariantCombination q := by
  unfold oddParityInvariantCombination
  unfold oddParityGaugeTransform
  ring

/--
Any master-field constructor depending only on the invariant combination is
gauge invariant at this algebraic level.
-/
theorem oddMasterField_gaugeInvariant
    {Master : Type*}
    (master : ℝ → Master)
    (q : OddParityGaugeJet)
    (g : OddParityGaugeParameterJet) :
    master
        (oddParityInvariantCombination
          (oddParityGaugeTransform q g)) =
      master (oddParityInvariantCombination q) := by
  rw [oddParityInvariantCombination_gaugeInvariant]

/-- Regge–Wheeler energy density evaluated on a first-order jet. -/
def rwEnergyDensityJet
    (psiT psiX psi potential : ℝ) : ℝ :=
  (1 / 2 : ℝ) *
    (psiT ^ 2 +
      psiX ^ 2 +
      potential * psi ^ 2)

/-- Correct scalar energy flux `-ψₜ ψₓ`. -/
def rwEnergyFluxJet
    (psiT psiX : ℝ) : ℝ :=
  -(psiT * psiX)

def rwEnergyTimeDerivativeJet
    (psiT psiTT psiX psiXT psi potential : ℝ) : ℝ :=
  psiT * psiTT +
    psiX * psiXT +
    potential * psi * psiT

def rwEnergyFluxSpaceDerivativeJet
    (psiT psiXT psiX psiXX : ℝ) : ℝ :=
  -(psiXT * psiX + psiT * psiXX)

/--
Algebraic local energy identity for a time-independent potential.
-/
theorem rwLocalEnergyIdentity
    (psiT psiTT psiX psiXT psiXX psi potential : ℝ) :
    rwEnergyTimeDerivativeJet
        psiT psiTT psiX psiXT psi potential +
      rwEnergyFluxSpaceDerivativeJet
        psiT psiXT psiX psiXX =
      psiT * (psiTT - psiXX + potential * psi) := by
  unfold rwEnergyTimeDerivativeJet
  unfold rwEnergyFluxSpaceDerivativeJet
  ring

theorem rwLocalEnergyConservation_of_waveEquation
    (psiT psiTT psiX psiXT psiXX psi potential : ℝ)
    (hWave :
      psiTT - psiXX + potential * psi = 0) :
    rwEnergyTimeDerivativeJet
        psiT psiTT psiX psiXT psi potential +
      rwEnergyFluxSpaceDerivativeJet
        psiT psiXT psiX psiXX = 0 := by
  rw [rwLocalEnergyIdentity]
  rw [hWave]
  ring

/--
Integrated balance-law carrier. `accumulatedBoundaryFlux t` is the integrated
outgoing boundary contribution between time `0` and time `t`.
-/
structure ReggeWheelerIntegratedEnergyBalance where
  energy : ℝ → ℝ
  accumulatedBoundaryFlux : ℝ → ℝ
  balance :
    ∀ t,
      energy t - energy 0 =
        accumulatedBoundaryFlux t
  boundaryFlux_zero :
    ∀ t, accumulatedBoundaryFlux t = 0

theorem rwEnergy_conserved
    (B : ReggeWheelerIntegratedEnergyBalance)
    (t : ℝ) :
    B.energy t = B.energy 0 := by
  have hBalance := B.balance t
  have hBoundary := B.boundaryFlux_zero t
  linarith

/--
Initial Regge–Wheeler energy. `potentialStar` is already expressed as a
function of tortoise coordinate.
-/
noncomputable def rwInitialEnergy
    (potentialStar initialPosition initialVelocity
      initialSpatialDerivative : ℝ → ℝ) : ℝ :=
  ∫ x : ℝ,
    rwEnergyDensityJet
      (initialVelocity x)
      (initialSpatialDerivative x)
      (initialPosition x)
      (potentialStar x)

/--
Quznor profile and a separately supplied derivative of its real part.

The derivative field is data; its agreement with the analytic derivative of
`profile.re` remains a separate obligation.
-/
structure QuznorReggeWheelerInitialData where
  profile : ℝ → ℂ
  realSpatialDerivative : ℝ → ℝ

noncomputable def quznorReggeWheelerObservable
    (potentialStar : ℝ → ℝ)
    (Q : QuznorReggeWheelerInitialData) : ℝ :=
  rwInitialEnergy
    potentialStar
    (fun x => (Q.profile x).re)
    (fun _ => 0)
    Q.realSpatialDerivative

noncomputable def quznorReggeWheelerScaledCarrier
    (N : Nat)
    (potentialStar : ℝ → ℝ)
    (Q : QuznorReggeWheelerInitialData) : ℝ :=
  (N : ℝ) *
    quznorReggeWheelerObservable potentialStar Q

theorem quznorReggeWheelerScaledCarrier_div
    (N : Nat)
    (hN : 0 < N)
    (potentialStar : ℝ → ℝ)
    (Q : QuznorReggeWheelerInitialData) :
    quznorReggeWheelerScaledCarrier
        N potentialStar Q / (N : ℝ) =
      quznorReggeWheelerObservable
        potentialStar Q := by
  have hNNe : (N : ℝ) ≠ 0 := by
    exact_mod_cast Nat.ne_of_gt hN
  unfold quznorReggeWheelerScaledCarrier
  field_simp [hNNe]

/--
Abstract uniqueness package for two solutions of exactly the same
Regge–Wheeler initial-value problem.
-/
structure ReggeWheelerIVPUniqueness
    (Solution : Type*) where
  solvesEquation : Solution → Prop
  hasPrescribedInitialData : Solution → Prop
  uniqueness :
    ∀ {u v : Solution},
      solvesEquation u →
      hasPrescribedInitialData u →
      solvesEquation v →
      hasPrescribedInitialData v →
      u = v

theorem rwSolution_eq_standardGR
    {Solution : Type*}
    (P : ReggeWheelerIVPUniqueness Solution)
    {solution standardGR : Solution}
    (hSolutionEquation : P.solvesEquation solution)
    (hSolutionInitial :
      P.hasPrescribedInitialData solution)
    (hGREquation : P.solvesEquation standardGR)
    (hGRInitial :
      P.hasPrescribedInitialData standardGR) :
    solution = standardGR :=
  P.uniqueness
    hSolutionEquation
    hSolutionInitial
    hGREquation
    hGRInitial

/--
Every deterministic observable has zero deviation when uniqueness identifies
the two solutions.
-/
theorem rwFunctionalDeviation_zero
    {Solution : Type*}
    (P : ReggeWheelerIVPUniqueness Solution)
    {solution standardGR : Solution}
    (hSolutionEquation : P.solvesEquation solution)
    (hSolutionInitial :
      P.hasPrescribedInitialData solution)
    (hGREquation : P.solvesEquation standardGR)
    (hGRInitial :
      P.hasPrescribedInitialData standardGR)
    (observable : Solution → ℝ) :
    observable solution -
        observable standardGR = 0 := by
  rw [rwSolution_eq_standardGR
    P
    hSolutionEquation
    hSolutionInitial
    hGREquation
    hGRInitial]
  ring

/--
Unproved calibration ansatz connecting integrated Regge–Wheeler flux to a
finite family of soft-mode probabilities.

No inhabitant is constructed in this module.
-/
structure ReggeWheelerToSoftCalibrationAnsatz
    (N : Nat) where
  integratedFlux : Fin N → ℝ
  coupling : Fin N → ℝ
  softProbability : Fin N → ℝ
  integratedFlux_nonnegative :
    ∀ k, 0 ≤ integratedFlux k
  coupling_nonnegative :
    ∀ k, 0 ≤ coupling k
  calibrationLaw :
    ∀ k,
      softProbability k =
        coupling k * integratedFlux k

def reggeWheelerQuznorEnergyBridgeStatus : String :=
  "RW_PEAK_GAUGE_CANCELLATION_LOCAL_ENERGY_IDENTITY_AND_GR_EQUIVALENCE"

def reggeWheelerQuznorEnergyBridgeBoundary : String :=
  "NO_GEOMETRIC_MASTER_EQUATION_DERIVATION_NO_PDE_WELLPOSEDNESS_NO_SOFT_CALIBRATION_INHABITANT_NO_SCALAR_CURVATURE_INVARIANT"

end

end Chronos.Frontier
