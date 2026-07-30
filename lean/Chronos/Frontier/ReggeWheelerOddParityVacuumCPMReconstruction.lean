import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityMasterExtraction

namespace Chronos.Frontier

noncomputable section

/--
A pointwise first jet of the vacuum Cunningham–Price–Moncrief odd-parity
master function.

The normalization is fixed so that the repository's Regge–Wheeler master
amplitude satisfies

`Ψ_RW = (1 / 2) ∂ₜ Ψ_CPM`.

The fields are local scalar and first-derivative data. This carrier does not
yet prove the Regge–Wheeler equation or derive the jet from initial data.
-/
structure ReggeWheelerOddParityVacuumCPMFirstJet where
  background : ReggeWheelerSchwarzschildBackground
  ell : ℕ
  radiativeMode : 2 ≤ ell
  cpmAmplitude : ℝ
  cpmTimeDerivative : ℝ
  cpmRadialDerivative : ℝ

/--
The repository-normalized Regge–Wheeler amplitude reconstructed from the
vacuum CPM time derivative:

`Ψ_RW = (1 / 2) ∂ₜ Ψ_CPM`.
-/
def reggeWheelerOddParityVacuumCPMRWMaster
    (jet : ReggeWheelerOddParityVacuumCPMFirstJet) : ℝ :=
  jet.cpmTimeDerivative / 2

/--
The time-angular Regge–Wheeler-gauge coefficient reconstructed from the
vacuum CPM amplitude:

`h_t = (f / 2) ∂ᵣ(r Ψ_CPM)
     = (f / 2) (Ψ_CPM + r ∂ᵣΨ_CPM)`.
-/
def reggeWheelerOddParityVacuumCPMTimeCoefficient
    (jet : ReggeWheelerOddParityVacuumCPMFirstJet) : ℝ :=
  reggeWheelerSchwarzschildExteriorFactor jet.background / 2 *
    (
      jet.cpmAmplitude +
        jet.background.radius * jet.cpmRadialDerivative
    )

/--
The radial-angular coefficient reconstructed through the existing
Regge–Wheeler normalization:

`h_r = r Ψ_RW / f`
and
`Ψ_RW = (1 / 2) ∂ₜ Ψ_CPM`.
-/
def reggeWheelerOddParityVacuumCPMRadialCoefficient
    (jet : ReggeWheelerOddParityVacuumCPMFirstJet) : ℝ :=
  reggeWheelerOddParityRWRadialCoefficientFromMaster
    jet.background
    (reggeWheelerOddParityVacuumCPMRWMaster jet)

/--
Construct both nonzero Regge–Wheeler-gauge odd-parity metric coefficients
from one vacuum CPM first jet.

Unlike the earlier constructor, this definition does not accept an
independent freely supplied `hTimeAngular`.
-/
def reggeWheelerOddParityVacuumCPMMetricComponents
    (jet : ReggeWheelerOddParityVacuumCPMFirstJet) :
    ReggeWheelerOddParityRWGaugeMetricComponents :=
  reggeWheelerOddParityRWGaugeMetricComponentsOfMaster
    jet.background
    jet.ell
    jet.radiativeMode
    (reggeWheelerOddParityVacuumCPMTimeCoefficient jet)
    (reggeWheelerOddParityVacuumCPMRWMaster jet)

/--
The reconstructed time-angular coefficient is exactly the CPM radial
reconstruction formula.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricComponents_timeAngular
    (jet : ReggeWheelerOddParityVacuumCPMFirstJet) :
    (
      reggeWheelerOddParityVacuumCPMMetricComponents jet
    ).hTimeAngular =
      reggeWheelerOddParityVacuumCPMTimeCoefficient jet := by
  rfl

/--
The reconstructed radial-angular coefficient is exactly the existing
Regge–Wheeler radial reconstruction evaluated on half the CPM time
derivative.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricComponents_radialAngular
    (jet : ReggeWheelerOddParityVacuumCPMFirstJet) :
    (
      reggeWheelerOddParityVacuumCPMMetricComponents jet
    ).hRadialAngular =
      reggeWheelerOddParityVacuumCPMRadialCoefficient jet := by
  rfl

/--
The reconstructed odd tensor coefficient vanishes in Regge–Wheeler gauge.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricComponents_tensorAngular_zero
    (jet : ReggeWheelerOddParityVacuumCPMFirstJet) :
    (
      reggeWheelerOddParityVacuumCPMMetricComponents jet
    ).hTensorAngular =
      0 := by
  rfl

/--
Extracting the repository's Regge–Wheeler master amplitude from the
CPM-reconstructed metric returns half the CPM time derivative.
-/
theorem reggeWheelerOddParityVacuumCPMMetricComponents_master
    (jet : ReggeWheelerOddParityVacuumCPMFirstJet) :
    reggeWheelerOddParityRWMasterAmplitude
        (reggeWheelerOddParityVacuumCPMMetricComponents jet) =
      reggeWheelerOddParityVacuumCPMRWMaster jet := by
  unfold reggeWheelerOddParityVacuumCPMMetricComponents
  exact
    reggeWheelerOddParityRWGaugeMetricComponentsOfMaster_master
      jet.background
      jet.ell
      jet.radiativeMode
      (reggeWheelerOddParityVacuumCPMTimeCoefficient jet)
      (reggeWheelerOddParityVacuumCPMRWMaster jet)

/--
The reconstructed metric satisfies the vacuum CPM-to-Regge–Wheeler
time-derivative relation exactly:

`2 Ψ_RW = ∂ₜ Ψ_CPM`.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricComponents_masterTimeDerivative
    (jet : ReggeWheelerOddParityVacuumCPMFirstJet) :
    2 *
        reggeWheelerOddParityRWMasterAmplitude
          (reggeWheelerOddParityVacuumCPMMetricComponents jet) =
      jet.cpmTimeDerivative := by
  rw [reggeWheelerOddParityVacuumCPMMetricComponents_master]
  unfold reggeWheelerOddParityVacuumCPMRWMaster
  ring

/--
One CPM first jet simultaneously fixes:

* the time-angular coefficient;
* the radial-angular coefficient;
* the CPM-to-Regge–Wheeler master relation.

This removes the earlier independent `hTimeAngular` input at the local metric
reconstruction level.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricComponents_reconstructsBothCoefficients
    (jet : ReggeWheelerOddParityVacuumCPMFirstJet) :
    (
      reggeWheelerOddParityVacuumCPMMetricComponents jet
    ).hTimeAngular =
        reggeWheelerOddParityVacuumCPMTimeCoefficient jet ∧
    (
      reggeWheelerOddParityVacuumCPMMetricComponents jet
    ).hRadialAngular =
        reggeWheelerOddParityVacuumCPMRadialCoefficient jet ∧
    2 *
        reggeWheelerOddParityRWMasterAmplitude
          (reggeWheelerOddParityVacuumCPMMetricComponents jet) =
      jet.cpmTimeDerivative := by
  exact ⟨
    reggeWheelerOddParityVacuumCPMMetricComponents_timeAngular jet,
    reggeWheelerOddParityVacuumCPMMetricComponents_radialAngular jet,
    reggeWheelerOddParityVacuumCPMMetricComponents_masterTimeDerivative
      jet
  ⟩

def reggeWheelerOddParityVacuumCPMReconstructionBoundary : String :=
  "VACUUM_CPM_FIRST_JET_RECONSTRUCTS_BOTH_TIME_AND_RADIAL_RW_GAUGE_METRIC_COEFFICIENTS_AND_PROVES_TWO_TIMES_RW_MASTER_EQUALS_CPM_TIME_DERIVATIVE_CPM_JET_NOT_DERIVED_FROM_MASTER_WAVE_EVOLUTION_METRIC_PARTIALS_CONNECTION_PARTIALS_FREE_FALL_RESPONSE_AND_PHYSICAL_STRAIN_NOT_PROVED"

end

end Chronos.Frontier
