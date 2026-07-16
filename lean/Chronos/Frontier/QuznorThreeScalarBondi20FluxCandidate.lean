import Mathlib
import Chronos.Frontier.QuznorD1D5ThreeModeVandermondeInversion

namespace Chronos.Frontier

open scoped BigOperators
open intervalIntegral

/-- Labels for a candidate covariant three-real-scalar carrier.

No theorem identifies these labels with the established abstract Quznor
coefficients `S₂`, `S₃`, and `S₄`. -/
inductive QuznorScalarLabel
  | q2
  | q3
  | q4
  deriving DecidableEq, Fintype

/-- Candidate three-real-scalar field content. -/
structure QuznorThreeRealScalarCandidate (Spacetime : Type*) where
  field : QuznorScalarLabel → Spacetime → ℝ
  kineticWeight : QuznorScalarLabel → ℝ
  kineticWeight_pos : ∀ j, 0 < kineticWeight j
  potential : (QuznorScalarLabel → ℝ) → ℝ
  sidfhInteraction : ℝ → (QuznorScalarLabel → ℝ) → ℝ

/-- Candidate covariant Lagrangian density after geometric kinetic
contractions have been supplied as real numbers. -/
noncomputable def quznorCandidateLagrangianDensity
    {Spacetime : Type*}
    (candidate : QuznorThreeRealScalarCandidate Spacetime)
    (sidfhValue : ℝ)
    (fieldValues kineticContractions : QuznorScalarLabel → ℝ) : ℝ :=
  -((1 / 2 : ℝ) *
      ∑ j : QuznorScalarLabel,
        candidate.kineticWeight j * kineticContractions j)
    - candidate.potential fieldValues
    - candidate.sidfhInteraction sidfhValue fieldValues

/-- Repository-native extraction of the stored `S₂`, `S₃`, and `S₄`
components from a `QuznorD1D5CoefficientCarrier` into the common
`QuznorScalarLabel → ℝ` coefficient surface.

This map only repackages the carrier fields; it makes no claim about the
candidate asymptotic coefficients. -/
def quznorD1D5CarrierAbstractCoefficients
    {D1 D2 D3 D4 D5 : Type*}
    (carrier : QuznorD1D5CoefficientCarrier D1 D2 D3 D4 D5) :
    QuznorScalarLabel → ℝ
  | .q2 => carrier.S2
  | .q3 => carrier.S3
  | .q4 => carrier.S4

/-- The repository-native extraction map returns exactly the three stored
carrier coefficients. -/
theorem quznorD1D5CarrierAbstractCoefficients_values
    {D1 D2 D3 D4 D5 : Type*}
    (carrier : QuznorD1D5CoefficientCarrier D1 D2 D3 D4 D5) :
    quznorD1D5CarrierAbstractCoefficients carrier .q2 = carrier.S2 ∧
      quznorD1D5CarrierAbstractCoefficients carrier .q3 = carrier.S3 ∧
      quznorD1D5CarrierAbstractCoefficients carrier .q4 = carrier.S4 := by
  simp [quznorD1D5CarrierAbstractCoefficients]

/-- Missing abstract-to-asymptotic bridge proposition. -/
def QuznorAbstractAsymptoticBridge
    (S Q : QuznorScalarLabel → ℝ) : Prop :=
  ∀ j, S j = Q j

/-- A typed carrier containing both the established abstract coefficient
surface and a candidate asymptotic coefficient surface.

The relation between them is supplied as an explicit proof field. This
structure does not construct that proof from either coefficient surface. -/
structure QuznorAbstractAsymptoticBridgeCarrier where
  abstractCoefficient : QuznorScalarLabel → ℝ
  asymptoticCoefficient : QuznorScalarLabel → ℝ
  bridge :
    QuznorAbstractAsymptoticBridge
      abstractCoefficient asymptoticCoefficient

/-- Pointwise coefficient transport obtained only from the carrier's
explicit bridge hypothesis. -/
theorem QuznorAbstractAsymptoticBridgeCarrier.coefficient_eq
    (carrier : QuznorAbstractAsymptoticBridgeCarrier)
    (j : QuznorScalarLabel) :
    carrier.abstractCoefficient j =
      carrier.asymptoticCoefficient j := by
  exact carrier.bridge j

/-- The explicit bridge also yields equality of the two coefficient
functions. -/
theorem QuznorAbstractAsymptoticBridgeCarrier.coefficient_fun_eq
    (carrier : QuznorAbstractAsymptoticBridgeCarrier) :
    carrier.abstractCoefficient =
      carrier.asymptoticCoefficient := by
  funext j
  exact carrier.coefficient_eq j

/--
A typed asymptotic coefficient extractor for three real scalar fields.

For supplied fields `φ₂`, `φ₃`, and `φ₄`, `extract φ₂ φ₃ φ₄ j`
represents the candidate asymptotic coefficient `Q_j[φ₂, φ₃, φ₄]`.
No field equation, asymptotic limit, or coefficient formula is imposed here.
-/
structure QuznorThreeScalarAsymptoticExtractor
    (Spacetime : Type*) where
  extract :
    (Spacetime → ℝ) →
      (Spacetime → ℝ) →
        (Spacetime → ℝ) →
          QuznorScalarLabel → ℝ


/--
The complete candidate asymptotic coefficient surface
`j ↦ Q_j[φ₂, φ₃, φ₄]`.
-/
def quznorThreeScalarAsymptoticCoefficients
    {Spacetime : Type*}
    (extractor : QuznorThreeScalarAsymptoticExtractor Spacetime)
    (φ2 φ3 φ4 : Spacetime → ℝ) :
    QuznorScalarLabel → ℝ :=
  extractor.extract φ2 φ3 φ4


/--
Minimal compatibility between the repository-native abstract coefficient
surface and the coefficients extracted from the three scalar fields.

This equality is an explicit hypothesis. Its derivation from D1–D5 data,
covariant evolution, or asymptotic limits remains outside this definition.
-/
def QuznorD1D5AsymptoticExtractorCompatible
    {D1 D2 D3 D4 D5 Spacetime : Type*}
    (carrier : QuznorD1D5CoefficientCarrier D1 D2 D3 D4 D5)
    (extractor : QuznorThreeScalarAsymptoticExtractor Spacetime)
    (φ2 φ3 φ4 : Spacetime → ℝ) : Prop :=
  quznorD1D5CarrierAbstractCoefficients carrier =
    quznorThreeScalarAsymptoticCoefficients extractor φ2 φ3 φ4


/--
The abstract-to-asymptotic bridge follows from the minimal compatibility
hypothesis alone.
-/
theorem quznorAbstractAsymptoticBridge_of_asymptoticExtractorCompatible
    {D1 D2 D3 D4 D5 Spacetime : Type*}
    (carrier : QuznorD1D5CoefficientCarrier D1 D2 D3 D4 D5)
    (extractor : QuznorThreeScalarAsymptoticExtractor Spacetime)
    (φ2 φ3 φ4 : Spacetime → ℝ)
    (hCompatible :
      QuznorD1D5AsymptoticExtractorCompatible
        carrier extractor φ2 φ3 φ4) :
    QuznorAbstractAsymptoticBridge
      (quznorD1D5CarrierAbstractCoefficients carrier)
      (quznorThreeScalarAsymptoticCoefficients
        extractor φ2 φ3 φ4) := by
  intro j
  exact congrFun hCompatible j


/--
The weakest typed carrier recording asymptotic coefficient limits for a
supplied solved three-scalar field configuration.

The carrier stores only the pointwise identification needed later to derive
`QuznorD1D5AsymptoticExtractorCompatible`. It does not derive the field
solution, existence of the asymptotic limits, or their values.
-/
structure QuznorSolvedThreeScalarAsymptoticLimitCarrier
    {D1 D2 D3 D4 D5 Spacetime : Type*}
    (carrier : QuznorD1D5CoefficientCarrier D1 D2 D3 D4 D5)
    (extractor : QuznorThreeScalarAsymptoticExtractor Spacetime)
    (φ2 φ3 φ4 : Spacetime → ℝ) where
  coefficientLimit :
    ∀ j,
      quznorD1D5CarrierAbstractCoefficients carrier j =
        quznorThreeScalarAsymptoticCoefficients
          extractor φ2 φ3 φ4 j


/--
A supplied solved-field asymptotic-limit carrier yields the minimal
abstract-to-asymptotic compatibility proposition.
-/
theorem quznorD1D5AsymptoticExtractorCompatible_of_solvedThreeScalarAsymptoticLimitCarrier
    {D1 D2 D3 D4 D5 Spacetime : Type*}
    (carrier : QuznorD1D5CoefficientCarrier D1 D2 D3 D4 D5)
    (extractor : QuznorThreeScalarAsymptoticExtractor Spacetime)
    (φ2 φ3 φ4 : Spacetime → ℝ)
    (hLimit :
      QuznorSolvedThreeScalarAsymptoticLimitCarrier
        carrier extractor φ2 φ3 φ4) :
    QuznorD1D5AsymptoticExtractorCompatible
      carrier extractor φ2 φ3 φ4 := by
  unfold QuznorD1D5AsymptoticExtractorCompatible
  exact funext hLimit.coefficientLimit


/--
A supplied solved-field asymptotic-limit carrier yields the complete typed
abstract-to-asymptotic bridge.
-/
theorem quznorAbstractAsymptoticBridge_of_solvedThreeScalarAsymptoticLimitCarrier
    {D1 D2 D3 D4 D5 Spacetime : Type*}
    (carrier : QuznorD1D5CoefficientCarrier D1 D2 D3 D4 D5)
    (extractor : QuznorThreeScalarAsymptoticExtractor Spacetime)
    (φ2 φ3 φ4 : Spacetime → ℝ)
    (hLimit :
      QuznorSolvedThreeScalarAsymptoticLimitCarrier
        carrier extractor φ2 φ3 φ4) :
    QuznorAbstractAsymptoticBridge
      (quznorD1D5CarrierAbstractCoefficients carrier)
      (quznorThreeScalarAsymptoticCoefficients
        extractor φ2 φ3 φ4) := by
  apply quznorAbstractAsymptoticBridge_of_asymptoticExtractorCompatible
  exact
    quznorD1D5AsymptoticExtractorCompatible_of_solvedThreeScalarAsymptoticLimitCarrier
      carrier extractor φ2 φ3 φ4 hLimit


/-- Axisymmetric real `Y₂₀` in the coordinate `x = cos θ`. -/
noncomputable def quznorY20Axisymmetric (x : ℝ) : ℝ :=
  (Real.sqrt 5 / (4 * Real.sqrt Real.pi)) * (3 * x ^ 2 - 1)

/-- Coordinate-reduced spherical Gaunt integral. -/
noncomputable def quznorGauntY20 : ℝ :=
  2 * Real.pi *
    ∫ x : ℝ in (-1)..1, (quznorY20Axisymmetric x) ^ 3

/-- Exact polynomial part of the `Y₂₀³` integral. -/
theorem quznor_legendre20_cube_integral :
    (∫ x : ℝ in (-1)..1, (3 * x ^ 2 - 1) ^ 3) =
      (32 / 35 : ℝ) := by
  have h27x6 :
      IntervalIntegrable
        (fun x : ℝ => 27 * x ^ 6)
        MeasureTheory.volume (-1) 1 :=
    ((continuous_const : Continuous fun _ : ℝ => (27 : ℝ)).mul
      (continuous_id.pow 6)).intervalIntegrable (-1) 1
  have h27x4 :
      IntervalIntegrable
        (fun x : ℝ => 27 * x ^ 4)
        MeasureTheory.volume (-1) 1 :=
    ((continuous_const : Continuous fun _ : ℝ => (27 : ℝ)).mul
      (continuous_id.pow 4)).intervalIntegrable (-1) 1
  have h9x2 :
      IntervalIntegrable
        (fun x : ℝ => 9 * x ^ 2)
        MeasureTheory.volume (-1) 1 :=
    ((continuous_const : Continuous fun _ : ℝ => (9 : ℝ)).mul
      (continuous_id.pow 2)).intervalIntegrable (-1) 1
  have hOne :
      IntervalIntegrable
        (fun _ : ℝ => (1 : ℝ))
        MeasureTheory.volume (-1) 1 :=
    (continuous_const : Continuous fun _ : ℝ => (1 : ℝ)).intervalIntegrable
      (-1) 1
  have hDifference :
      IntervalIntegrable
        (fun x : ℝ => 27 * x ^ 6 - 27 * x ^ 4)
        MeasureTheory.volume (-1) 1 :=
    h27x6.sub h27x4
  have hPolynomial :
      IntervalIntegrable
        (fun x : ℝ => 27 * x ^ 6 - 27 * x ^ 4 + 9 * x ^ 2)
        MeasureTheory.volume (-1) 1 :=
    hDifference.add h9x2
  calc
    (∫ x : ℝ in (-1)..1, (3 * x ^ 2 - 1) ^ 3) =
        ∫ x : ℝ in (-1)..1,
          (27 * x ^ 6 - 27 * x ^ 4 + 9 * x ^ 2 - 1) := by
      apply intervalIntegral.integral_congr
      intro x _
      ring
    _ =
        (∫ x : ℝ in (-1)..1,
          (27 * x ^ 6 - 27 * x ^ 4 + 9 * x ^ 2)) -
        ∫ x : ℝ in (-1)..1, (1 : ℝ) := by
      rw [intervalIntegral.integral_sub hPolynomial hOne]
    _ =
        ((∫ x : ℝ in (-1)..1,
            (27 * x ^ 6 - 27 * x ^ 4)) +
          ∫ x : ℝ in (-1)..1, 9 * x ^ 2) -
        ∫ x : ℝ in (-1)..1, (1 : ℝ) := by
      rw [intervalIntegral.integral_add hDifference h9x2]
    _ =
        (((∫ x : ℝ in (-1)..1, 27 * x ^ 6) -
            ∫ x : ℝ in (-1)..1, 27 * x ^ 4) +
          (∫ x : ℝ in (-1)..1, 9 * x ^ 2)) -
        ∫ x : ℝ in (-1)..1, (1 : ℝ) := by
      rw [intervalIntegral.integral_sub h27x6 h27x4]
    _ = (32 / 35 : ℝ) := by
      norm_num [
        intervalIntegral.integral_const_mul,
        integral_pow,
        integral_one
      ]

/-- Exact axisymmetric Gaunt identity. -/
theorem quznorGauntY20_exact :
    quznorGauntY20 =
      Real.sqrt 5 / (7 * Real.sqrt Real.pi) := by
  unfold quznorGauntY20 quznorY20Axisymmetric
  simp_rw [mul_pow]
  rw [intervalIntegral.integral_const_mul]
  rw [quznor_legendre20_cube_integral]
  have hsqrt5_sq : (Real.sqrt 5) ^ 2 = 5 := by
    norm_num
  have hsqrtPi_sq : (Real.sqrt Real.pi) ^ 2 = Real.pi :=
    Real.sq_sqrt (le_of_lt Real.pi_pos)
  have hsqrtPi_ne : Real.sqrt Real.pi ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.2 Real.pi_pos)
  field_simp [hsqrtPi_ne]
  nlinarith

/-- First-bin data for the candidate Quznor `(2,0)` flux. -/
structure QuznorBondi20FluxData where
  newtonG : ℝ
  epsilon : ℝ
  kineticWeight : QuznorScalarLabel → ℝ
  J02 : QuznorScalarLabel → ℝ
  J22 : QuznorScalarLabel → ℝ

/-- Candidate Quznor contribution. -/
noncomputable def quznorBondi20Flux
    (data : QuznorBondi20FluxData) : ℝ :=
  4 * Real.pi * data.newtonG *
    ∑ j : QuznorScalarLabel,
      data.kineticWeight j *
        (2 * data.epsilon * data.J02 j +
          data.epsilon ^ 2 * quznorGauntY20 * data.J22 j)

/-- Closed form after inserting the proved Gaunt coefficient. -/
theorem quznorBondi20Flux_closedForm
    (data : QuznorBondi20FluxData) :
    quznorBondi20Flux data =
      4 * Real.pi * data.newtonG *
        ∑ j : QuznorScalarLabel,
          data.kineticWeight j *
            (2 * data.epsilon * data.J02 j +
              data.epsilon ^ 2 *
                (Real.sqrt 5 / (7 * Real.sqrt Real.pi)) *
                  data.J22 j) := by
  simp [quznorBondi20Flux, quznorGauntY20_exact]

/-- Complete first-bin `(2,0)` Bondi source data. -/
structure Bondi20FirstBinData where
  deltaMass20 : ℝ
  gravitationalNews20 : ℝ
  sidfhFlux20 : ℝ
  quznorFluxData : QuznorBondi20FluxData

/-- Existing Bondi source extended by the candidate Quznor flux. -/
noncomputable def bondi20FirstBinSource
    (data : Bondi20FirstBinData) : ℝ :=
  data.deltaMass20 +
    data.gravitationalNews20 +
    data.sidfhFlux20 +
    quznorBondi20Flux data.quznorFluxData

/-- Exact packaging identity for the combined source. -/
theorem bondi20FirstBinSource_eq
    (data : Bondi20FirstBinData) :
    bondi20FirstBinSource data =
      data.deltaMass20 +
        data.gravitationalNews20 +
        data.sidfhFlux20 +
        quznorBondi20Flux data.quznorFluxData := by
  rfl


/--
Minimal carrier for three scalar fields already proved to solve a supplied
covariant evolution predicate.

No asymptotic coefficient equality is stored here. The first subsequent
mathematical obligation is to prove, from `solvesCovariantEvolution` and
controlled asymptotic analysis,

`∀ j, quznorD1D5CarrierAbstractCoefficients carrier j =
  quznorThreeScalarAsymptoticCoefficients extractor φ2 φ3 φ4 j`.
-/
structure QuznorCovariantThreeScalarSolutionCarrier
    (D1 D2 D3 D4 D5 Spacetime : Type*)
    (covariantSolution :
      (Spacetime → ℝ) →
        (Spacetime → ℝ) →
          (Spacetime → ℝ) → Prop) where
  carrier : QuznorD1D5CoefficientCarrier D1 D2 D3 D4 D5
  extractor : QuznorThreeScalarAsymptoticExtractor Spacetime
  φ2 : Spacetime → ℝ
  φ3 : Spacetime → ℝ
  φ4 : Spacetime → ℝ
  solvesCovariantEvolution : covariantSolution φ2 φ3 φ4

end Chronos.Frontier
