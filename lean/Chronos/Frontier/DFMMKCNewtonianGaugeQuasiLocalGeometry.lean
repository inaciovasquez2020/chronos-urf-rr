import Chronos.Frontier.DFMMKCPerturbedQuasiLocalSurface

namespace Chronos.Frontier

/--
Cosmic-time conformal-Newtonian convention used by the spherical perturbative
bridge:

`ds^2 = -(1 + 2 epsilon Phi) dt^2
       + a^2 (1 - 2 epsilon Psi) (dchi^2 + chi^2 dOmega^2)`.

For a background round sphere of areal radius `R`, the angular metric
coefficient is therefore `R^2 (1 - 2 epsilon Psi)` at first order.
-/
def dfmMkcNewtonianGaugeAreaRadiusCorrection
    (areaRadius spatialPotential : ℝ) : ℝ :=
  -areaRadius * spatialPotential

/--
The correction `delta R = -R Psi` has exactly the angular-metric first
variation required by the Newtonian spatial factor `1 - 2 epsilon Psi`:
`delta(R^2) = 2 R delta R = -2 R^2 Psi`.
-/
theorem dfmMkcNewtonianGaugeAreaRadiusCorrection_linearizes_angularMetric
    (areaRadius spatialPotential : ℝ) :
    2 * areaRadius *
        dfmMkcNewtonianGaugeAreaRadiusCorrection
          areaRadius spatialPotential =
      -2 * areaRadius ^ 2 * spatialPotential := by
  unfold dfmMkcNewtonianGaugeAreaRadiusCorrection
  ring

/--
Binding of the carrier's previously free areal-radius correction to the
Newtonian-gauge angular geometry.  This is spherical and first-order only.
-/
structure DFMMKCNewtonianGaugeSphericalAreaRadiusBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) where
  areaRadiusCorrection_eq :
    P.areaRadiusCorrection =
      dfmMkcNewtonianGaugeAreaRadiusCorrection
        S.areaRadius P.newtonianSpatialPotential

/--
After the Newtonian-gauge angular binding, the carrier radius is the first-order
areal radius `R_epsilon = R (1 - epsilon Psi)`.
-/
theorem perturbedAreaRadius_eq_newtonianSpatialPotential
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (A : DFMMKCNewtonianGaugeSphericalAreaRadiusBinding S x P) :
    P.perturbedAreaRadius =
      S.areaRadius * (1 - P.epsilon * P.newtonianSpatialPotential) := by
  rw [P.perturbedAreaRadius_eq, A.areaRadiusCorrection_eq]
  unfold dfmMkcNewtonianGaugeAreaRadiusCorrection
  ring

end Chronos.Frontier
