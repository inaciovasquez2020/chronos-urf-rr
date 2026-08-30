import Chronos.Frontier.DFMMKCNewtonianGaugePerturbedRadiusBound

namespace Chronos.Frontier

/--
Exact correction from the background gate to the first-order Newtonian-gauge
perturbed gate after substituting
`R_epsilon = R (1 - epsilon Psi)` and
`m_epsilon = m + epsilon delta m`.
-/
noncomputable def dfmMkcNewtonianGaugeFirstOrderGateCorrection
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) : ℝ :=
  2 * P.epsilon *
      (sphericalHawkingMassFirstVariation
          S.areaRadius B.outgoingExpansion B.ingoingExpansion
          P.areaRadiusCorrection P.outgoingExpansionCorrection
          P.ingoingExpansionCorrection
        + S.hawkingMass * P.newtonianSpatialPotential) /
    (S.areaRadius * (1 - P.epsilon * P.newtonianSpatialPotential))

/-- Absolute gate error carried by the exact rational first-order correction. -/
def dfmMkcNewtonianGaugeFirstOrderGateStabilityError
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) : ℝ :=
  |dfmMkcNewtonianGaugeFirstOrderGateCorrection
      S x roundSymmetrySphere B P|

/--
Under the Newtonian areal-radius binding and the quantitative smallness
`|epsilon| |Psi| < 1`, the perturbed gate is exactly the background gate plus
one explicit rational correction.  No fixed-radius condition is used.
-/
theorem perturbedQLGate_eq_background_add_newtonianCorrection
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (A : DFMMKCNewtonianGaugeSphericalAreaRadiusBinding S x P)
    (H : DFMMKCFirstOrderSphericalHawkingGeometryBinding
      S x roundSymmetrySphere B P)
    (hsmall :
      dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P < 1) :
    DFMMKCPerturbedQLGate S x P =
      QL_gate data S +
        dfmMkcNewtonianGaugeFirstOrderGateCorrection
          S x roundSymmetrySphere B P := by
  have hsmall' :
      |P.epsilon| * |P.newtonianSpatialPotential| < 1 := by
    simpa [dfmMkcNewtonianGaugeRelativeRadiusPerturbation] using hsmall
  have hprod :
      P.epsilon * P.newtonianSpatialPotential ≤
        |P.epsilon| * |P.newtonianSpatialPotential| := by
    calc
      P.epsilon * P.newtonianSpatialPotential ≤
          |P.epsilon * P.newtonianSpatialPotential| := le_abs_self _
      _ = |P.epsilon| * |P.newtonianSpatialPotential| := abs_mul _ _
  have hfactor :
      0 < 1 - P.epsilon * P.newtonianSpatialPotential := by
    linarith
  unfold DFMMKCPerturbedQLGate QL_gate
  rw [H.perturbedHawkingMass_eq]
  rw [perturbedAreaRadius_eq_newtonianSpatialPotential S x P A]
  unfold dfmMkcNewtonianGaugeFirstOrderGateCorrection
  field_simp [ne_of_gt S.areaRadius_pos, ne_of_gt hfactor]
  <;> ring

/--
The exact correction is controlled above by its absolute value, giving the
first-order gate stability estimate for a genuinely perturbed areal radius.
-/
theorem perturbedQLGate_le_background_add_newtonianStabilityError
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (A : DFMMKCNewtonianGaugeSphericalAreaRadiusBinding S x P)
    (H : DFMMKCFirstOrderSphericalHawkingGeometryBinding
      S x roundSymmetrySphere B P)
    (hsmall :
      dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P < 1) :
    DFMMKCPerturbedQLGate S x P ≤
      QL_gate data S +
        dfmMkcNewtonianGaugeFirstOrderGateStabilityError
          S x roundSymmetrySphere B P := by
  rw [perturbedQLGate_eq_background_add_newtonianCorrection
    S x roundSymmetrySphere B P A H hsmall]
  unfold dfmMkcNewtonianGaugeFirstOrderGateStabilityError
  exact add_le_add_left
    (le_abs_self
      (dfmMkcNewtonianGaugeFirstOrderGateCorrection
        S x roundSymmetrySphere B P))
    (QL_gate data S)

/--
DFM-MKC `C_**` propagation for a nonzero Newtonian areal-radius perturbation.
The old `areaRadiusCorrection = 0` condition is replaced by the sharp
quantitative denominator condition `|epsilon| |Psi| < 1`.  The same proved
background `C_**` remains the principal coefficient; all first-order mass and
radius effects occur in the explicit additive stability error.

The null-expansion binding is required so the carrier's expansion corrections
used by the Hawking first variation are the derived Newtonian-gauge ones.
-/
theorem dfmMkcPerturbedCoerciveEstimate_of_hubbleFloor_newtonianGauge
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (G : FlatFLRWSphericalExpansionBinding
      S x spatiallyFlatFLRW roundSymmetrySphere B)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (A : DFMMKCNewtonianGaugeSphericalAreaRadiusBinding S x P)
    (D : DFMMKCNewtonianGaugeSphericalPotentialDerivatives)
    (_N : DFMMKCNewtonianGaugeSphericalNullExpansionBinding S x P A D)
    (H : DFMMKCFirstOrderSphericalHawkingGeometryBinding
      S x roundSymmetrySphere B P)
    (HStar : ℝ)
    (hfloor : DFMMKCHubbleFloor HStar x)
    (hsub : ExpandingFlatFLRWSubHubbleSphere
      S x spatiallyFlatFLRW roundSymmetrySphere B G)
    (hrestricted :
      RestrictedDFMMKCHawkingComparisonHypotheses
        data S x spatiallyFlatFLRW roundSymmetrySphere)
    (hsmall :
      dfmMkcNewtonianGaugeRelativeRadiusPerturbation S x P < 1) :
    DFMMKCPerturbedCoerciveEstimate
      (dfmMkcHubbleFloorCStarStar HStar)
      (dfmMkcNewtonianGaugeFirstOrderGateStabilityError
        S x roundSymmetrySphere B P)
      S x P := by
  have hgate :=
    perturbedQLGate_le_background_add_newtonianStabilityError
      S x roundSymmetrySphere B P A H hsmall
  have hbase :
      ConcreteGravityCoerciveEstimate
        (dfmMkcHubbleFloorCStarStar HStar) data S :=
    concreteGravityCoerciveEstimate_of_dfmMkcHubbleFloor
      S x spatiallyFlatFLRW roundSymmetrySphere B G HStar
      hfloor hsub hrestricted
  unfold ConcreteGravityCoerciveEstimate at hbase
  unfold DFMMKCPerturbedCoerciveEstimate
  exact hgate.trans
    (add_le_add_right hbase
      (dfmMkcNewtonianGaugeFirstOrderGateStabilityError
        S x roundSymmetrySphere B P))

end Chronos.Frontier
