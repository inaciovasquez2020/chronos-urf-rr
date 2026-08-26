import Chronos.Frontier.DFMMKCNewtonianGaugeQuasiLocalGeometry

namespace Chronos.Frontier

/-- Dimensionless size of the first-order Newtonian areal-radius perturbation. -/
def dfmMkcNewtonianGaugeRelativeRadiusPerturbation
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) : ℝ :=
  |P.epsilon| * |P.newtonianSpatialPotential|

/-- The relative perturbation size is nonnegative. -/
theorem dfmMkcNewtonianGaugeRelativeRadiusPerturbation_nonnegative
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) :
    0 ≤ dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P := by
  unfold dfmMkcNewtonianGaugeRelativeRadiusPerturbation
  positivity

/--
The exact first-order Newtonian radius satisfies the quantitative lower bound
`R_epsilon >= R * (1 - |epsilon| |Psi|)`.
-/
theorem perturbedAreaRadius_ge_newtonianLowerBound
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (A : DFMMKCNewtonianGaugeSphericalAreaRadiusBinding S x P) :
    S.areaRadius *
        (1 - dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P) ≤
      P.perturbedAreaRadius := by
  rw [perturbedAreaRadius_eq_newtonianSpatialPotential S x P A]
  apply mul_le_mul_of_nonneg_left _ (le_of_lt S.areaRadius_pos)
  unfold dfmMkcNewtonianGaugeRelativeRadiusPerturbation
  have hprod :
      P.epsilon * P.newtonianSpatialPotential ≤
        |P.epsilon| * |P.newtonianSpatialPotential| := by
    calc
      P.epsilon * P.newtonianSpatialPotential ≤
          |P.epsilon * P.newtonianSpatialPotential| := le_abs_self _
      _ = |P.epsilon| * |P.newtonianSpatialPotential| := abs_mul _ _
  linarith

/--
If the relative Newtonian radial perturbation is strictly smaller than one,
the lower bound is strictly positive.  This includes the nonzero-correction
case and is the quantitative denominator control needed by the gate estimate.
-/
theorem perturbedAreaRadius_has_positive_newtonianLowerBound
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (A : DFMMKCNewtonianGaugeSphericalAreaRadiusBinding S x P)
    (hsmall :
      dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P < 1) :
    0 <
        S.areaRadius *
          (1 - dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P) ∧
      S.areaRadius *
          (1 - dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P) ≤
        P.perturbedAreaRadius := by
  constructor
  · exact mul_pos S.areaRadius_pos (sub_pos.mpr hsmall)
  · exact perturbedAreaRadius_ge_newtonianLowerBound S x P A

end Chronos.Frontier
