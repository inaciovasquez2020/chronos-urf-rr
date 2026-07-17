import Chronos.Frontier.ReggeWheelerQuznorEnergyBridge

namespace Chronos.Frontier

noncomputable section

/-!
# Finite hard/soft emission channel

This module contains a finite probability-level emission model and exact
finite-dimensional channel definitions.

The only dynamical probability theorem proved here is

`H N + S N = 1 - |A N|²`.

The amplitudes are real because the identity depends only on squared
magnitudes. No phase-sensitive Page-curve theorem is claimed.

The soft-dephasing and hard-partial-trace maps are defined exactly on finite
density matrices. Entanglement fidelity and hard-radiation entropy are kept
as separate derived quantities.

The Regge–Wheeler-to-soft relation is represented only by an uninhabited
calibration structure.
-/

/--
One finite emission step has residual, hard, and soft real amplitudes whose
squared magnitudes sum to one.
-/
structure FiniteHardSoftEmissionData where
  residualStepAmplitude : Nat → ℝ
  hardStepAmplitude : Nat → ℝ
  softStepAmplitude : Nat → ℝ
  localNormalization :
    ∀ k : Nat,
      residualStepAmplitude k ^ 2 +
          hardStepAmplitude k ^ 2 +
          softStepAmplitude k ^ 2 =
        1

/-- Residual horizon amplitude after `N` emission steps. -/
def finiteResidualAmplitude
    (E : FiniteHardSoftEmissionData) :
    Nat → ℝ
  | 0 => 1
  | n + 1 =>
      finiteResidualAmplitude E n *
        E.residualStepAmplitude n

/-- The real squared modulus `|A_N|²`. -/
def finiteResidualAmplitudeModulusSq
    (E : FiniteHardSoftEmissionData)
    (N : Nat) : ℝ :=
  finiteResidualAmplitude E N ^ 2

/-- Hard probability emitted in bin `k`. -/
def finiteHardEmissionWeight
    (E : FiniteHardSoftEmissionData)
    (k : Nat) : ℝ :=
  finiteResidualAmplitudeModulusSq E k *
    E.hardStepAmplitude k ^ 2

/-- Soft probability emitted in bin `k`. -/
def finiteSoftEmissionWeight
    (E : FiniteHardSoftEmissionData)
    (k : Nat) : ℝ :=
  finiteResidualAmplitudeModulusSq E k *
    E.softStepAmplitude k ^ 2

/-- Total hard probability emitted through the first `N` bins. -/
def finiteHardEmissionProbability
    (E : FiniteHardSoftEmissionData)
    (N : Nat) : ℝ :=
  Finset.sum (Finset.range N) fun k =>
    finiteHardEmissionWeight E k

/-- Total soft probability emitted through the first `N` bins. -/
def finiteSoftEmissionProbability
    (E : FiniteHardSoftEmissionData)
    (N : Nat) : ℝ :=
  Finset.sum (Finset.range N) fun k =>
    finiteSoftEmissionWeight E k

/-- Total emitted probability through the first `N` bins. -/
def finiteTotalEmissionProbability
    (E : FiniteHardSoftEmissionData)
    (N : Nat) : ℝ :=
  finiteHardEmissionProbability E N +
    finiteSoftEmissionProbability E N

/--
Finite telescoping identity

`H_N + S_N = 1 - |A_N|²`.
-/
theorem finiteHardSoftEmissionProbabilityIdentity
    (E : FiniteHardSoftEmissionData)
    (N : Nat) :
    finiteHardEmissionProbability E N +
        finiteSoftEmissionProbability E N =
      1 - finiteResidualAmplitudeModulusSq E N := by
  induction N with
  | zero =>
      simp [
        finiteHardEmissionProbability,
        finiteSoftEmissionProbability,
        finiteResidualAmplitudeModulusSq,
        finiteResidualAmplitude
      ]
  | succ n ih =>
      calc
        finiteHardEmissionProbability E (n + 1) +
              finiteSoftEmissionProbability E (n + 1) =
            (finiteHardEmissionProbability E n +
                finiteSoftEmissionProbability E n) +
              (finiteHardEmissionWeight E n +
                finiteSoftEmissionWeight E n) := by
          simp only [
            finiteHardEmissionProbability,
            finiteSoftEmissionProbability,
            Finset.sum_range_succ
          ]
          ac_rfl
        _ =
            1 -
              finiteResidualAmplitudeModulusSq E (n + 1) := by
          rw [ih]
          simp only [
            finiteHardEmissionWeight,
            finiteSoftEmissionWeight,
            finiteResidualAmplitudeModulusSq,
            finiteResidualAmplitude
          ]
          nlinarith [E.localNormalization n]

/--
Vacuum or one hard excitation in one of the `N` bins.
-/
abbrev FiniteHardBasis (N : Nat) :=
  Option (Fin N)

/--
Vacuum or one soft excitation in one of the `N` bins.
-/
abbrev FiniteSoftBasis (N : Nat) :=
  Option (Fin N)

/-- Tensor-product computational basis for hard and soft labels. -/
abbrev FiniteHardSoftBasis (N : Nat) :=
  FiniteHardBasis N × FiniteSoftBasis N

/-- Density-matrix carrier on the complete hard/soft finite basis. -/
abbrev FiniteHardSoftDensityMatrix (N : Nat) :=
  Matrix
    (FiniteHardSoftBasis N)
    (FiniteHardSoftBasis N)
    ℂ

/-- Density-matrix carrier after tracing out the soft factor. -/
abbrev FiniteHardDensityMatrix (N : Nat) :=
  Matrix
    (FiniteHardBasis N)
    (FiniteHardBasis N)
    ℂ

/--
Complete dephasing in the computational soft-label basis.

Hard coherences inside a fixed soft sector are retained. Matrix entries
between different soft labels are set to zero.
-/
def finiteSoftDephasingChannel
    {N : Nat}
    (ρ : FiniteHardSoftDensityMatrix N) :
    FiniteHardSoftDensityMatrix N :=
  fun p q =>
    if p.2 = q.2 then
      ρ p q
    else
      0

/--
Exact finite-dimensional partial trace over the soft basis.
-/
def finiteHardPartialTrace
    {N : Nat}
    (ρ : FiniteHardSoftDensityMatrix N) :
    FiniteHardDensityMatrix N :=
  fun h₁ h₂ =>
    ∑ s : FiniteSoftBasis N,
      ρ (h₁, s) (h₂, s)

/--
Hard-only channel obtained by soft dephasing followed by the exact soft
partial trace.
-/
def finiteHardOnlyChannel
    {N : Nat}
    (ρ : FiniteHardSoftDensityMatrix N) :
    FiniteHardDensityMatrix N :=
  finiteHardPartialTrace
    (finiteSoftDephasingChannel ρ)

/-- Logical-qubit density matrices. -/
abbrev FiniteLogicalDensityMatrix :=
  Matrix (Fin 2) (Fin 2) ℂ

/--
Hard survival fraction conditioned on emission.

When the denominator is zero, Lean's totalized division returns zero. The
physical conditional interpretation therefore requires
`finiteTotalEmissionProbability E N > 0`.
-/
def finiteHardConditionalFraction
    (E : FiniteHardSoftEmissionData)
    (N : Nat) : ℝ :=
  finiteHardEmissionProbability E N /
    finiteTotalEmissionProbability E N

/--
The decoded hard-only logical channel.

For a physical parameter `0 ≤ q ≤ 1`, this is the qubit
amplitude-damping channel with hard survival probability `q`.
-/
def finiteDecodedHardOnlyChannel
    (q : ℝ)
    (ρ : FiniteLogicalDensityMatrix) :
    FiniteLogicalDensityMatrix :=
  fun i j =>
    if i = 0 then
      if j = 0 then
        ρ 0 0 +
          ((1 - q : ℝ) : ℂ) * ρ 1 1
      else
        (Real.sqrt q : ℂ) * ρ 0 1
    else
      if j = 0 then
        (Real.sqrt q : ℂ) * ρ 1 0
      else
        (q : ℂ) * ρ 1 1

/--
Entanglement fidelity of the decoded amplitude-damping channel for the
maximally mixed logical input.

This is not the same quantity as the fidelity of the input state `|+⟩`.
-/
def finiteHardOnlyEntanglementFidelity
    (q : ℝ) : ℝ :=
  (1 + Real.sqrt q) ^ 2 / 4

/--
Entanglement fidelity derived from the finite hard fraction.
-/
def finiteEmissionEntanglementFidelity
    (E : FiniteHardSoftEmissionData)
    (N : Nat) : ℝ :=
  finiteHardOnlyEntanglementFidelity
    (finiteHardConditionalFraction E N)

/--
Reduced hard state on the two-dimensional subspace spanned by the hard vacuum
and the normalized coherent hard-excitation vector.
-/
def finiteReducedHardExcitedDensity
    (q : ℝ) :
    FiniteLogicalDensityMatrix :=
  fun i j =>
    if i = 0 then
      if j = 0 then
        ((1 - q : ℝ) : ℂ)
      else
        0
    else
      if j = 0 then
        0
      else
        (q : ℂ)

/--
Binary von Neumann entropy in natural-logarithm units.

Mathlib's totalized real logarithm supplies the endpoint convention
`0 * log 0 = 0`.
-/
def finiteBinaryEntropy
    (q : ℝ) : ℝ :=
  -(
    q * Real.log q +
      (1 - q) * Real.log (1 - q)
  )

/--
Entropy of the reduced hard radiation for the conditional emitted
single-excitation state.

This is an entropy of one reduced state, not a Page-curve theorem.
-/
def finiteHardRadiationEntropy
    (E : FiniteHardSoftEmissionData)
    (N : Nat) : ℝ :=
  finiteBinaryEntropy
    (finiteHardConditionalFraction E N)

/--
Unproved finite-bin calibration ansatz relating Regge–Wheeler bin energies to
soft-emission probabilities.

No inhabitant is constructed in this module.
-/
structure FiniteReggeWheelerToSoftCalibrationAnsatz
    (E : FiniteHardSoftEmissionData)
    (N : Nat) where
  reggeWheelerBinEnergy : Fin N → ℝ
  geometricCoupling : Fin N → ℝ
  reggeWheelerBinEnergy_nonnegative :
    ∀ k, 0 ≤ reggeWheelerBinEnergy k
  geometricCoupling_nonnegative :
    ∀ k, 0 ≤ geometricCoupling k
  calibrationLaw :
    ∀ k,
      E.softStepAmplitude k.1 ^ 2 =
        geometricCoupling k *
          reggeWheelerBinEnergy k

def finiteHardSoftEmissionChannelStatus : String :=
  "FINITE_HARD_SOFT_TELESCOPING_IDENTITY_AND_EXACT_CHANNEL_DEFINITIONS"

def finiteHardSoftEmissionChannelProved : String :=
  "H_N_PLUS_S_N_EQUALS_ONE_MINUS_RESIDUAL_AMPLITUDE_MODULUS_SQUARED"

def finiteHardSoftEmissionChannelBoundary : String :=
  "NO_REGGE_WHEELER_SOFT_CALIBRATION_INHABITANT_NO_PAGE_CURVE_THEOREM_NO_PHASE_COMPLETE_EMISSION_DYNAMICS"

end

end Chronos.Frontier
