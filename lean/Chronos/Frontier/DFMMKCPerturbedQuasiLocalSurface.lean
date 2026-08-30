import Chronos.Frontier.ConcreteGravityCoerciveEstimateProofObligation

namespace Chronos.Frontier

/--
First-order DFM-MKC quasi-local surface carrier over the already-proved
flat-FLRW spherical background layer.

The perturbation coordinates mirror the repository's Newtonian-gauge linear
sector: lapse/spatial metric potentials, scalar and longitudinal-vector modes,
matter density/velocity modes, plus the charge-reduced phase perturbation used
by the action-derived stress-energy formulas.  The geometric fields are kept
explicit because the repository does not yet derive quasi-local surface
geometry from those Newtonian-gauge perturbations.

This is a carrier only.  In particular, it does not assert a perturbed Hawking
formula, a perturbed Misner-Sharp formula, or any stability estimate.
-/
structure DFMMKCPerturbedQuasiLocalSurfaceCarrier
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (_x : RestrictedDFMMKCEnergyState) where
  epsilon : ℝ
  epsilon_abs_le_one : |epsilon| ≤ 1
  waveNumberSquared : ℝ
  waveNumberSquared_nonnegative : 0 ≤ waveNumberSquared
  newtonianLapsePotential : ℝ
  newtonianSpatialPotential : ℝ
  deltaScalarField : ℝ
  deltaScalarFieldPrime : ℝ
  deltaPhaseField : ℝ
  deltaPhaseFieldPrime : ℝ
  deltaTemporalVector : ℝ
  deltaLongitudinalVector : ℝ
  deltaMatterDensityContrast : ℝ
  matterVelocityDivergence : ℝ
  areaRadiusCorrection : ℝ
  outgoingExpansionCorrection : ℝ
  ingoingExpansionCorrection : ℝ
  arealGradientNormSqCorrection : ℝ
  perturbedAreaRadius : ℝ
  perturbedAreaRadius_eq :
    perturbedAreaRadius = S.areaRadius + epsilon * areaRadiusCorrection
  perturbedAreaRadius_pos : 0 < perturbedAreaRadius
  perturbedOutgoingExpansion : ℝ
  perturbedIngoingExpansion : ℝ
  perturbedHawkingMass : ℝ
  perturbedArealGradientNormSq : ℝ
  perturbedMisnerSharpMass : ℝ

/--
Areal-gradient scalar reconstructed from real spherical null expansions in the
fixed `g(l,n) = -2` normalization.
-/
noncomputable def sphericalArealGradientNormSqFromExpansions
    (areaRadius outgoingExpansion ingoingExpansion : ℝ) : ℝ :=
  -(areaRadius ^ 2 * outgoingExpansion * ingoingExpansion / 4)

/-- First variation of `r_A^2 * theta_+ * theta_- / 4`. -/
noncomputable def sphericalExpansionProductFirstVariation
    (areaRadius outgoingExpansion ingoingExpansion
      areaRadiusCorrection outgoingExpansionCorrection
      ingoingExpansionCorrection : ℝ) : ℝ :=
  areaRadius * areaRadiusCorrection * outgoingExpansion * ingoingExpansion / 2
    + areaRadius ^ 2 *
      (outgoingExpansionCorrection * ingoingExpansion
        + outgoingExpansion * ingoingExpansionCorrection) / 4

/--
First variation of the round-sphere Hawking mass
`m_H = r_A/2 + r_A^3 theta_+ theta_- / 8`.
-/
noncomputable def sphericalHawkingMassFirstVariation
    (areaRadius outgoingExpansion ingoingExpansion
      areaRadiusCorrection outgoingExpansionCorrection
      ingoingExpansionCorrection : ℝ) : ℝ :=
  areaRadiusCorrection / 2
    + (3 * areaRadius ^ 2 * areaRadiusCorrection *
        outgoingExpansion * ingoingExpansion
      + areaRadius ^ 3 *
        (outgoingExpansionCorrection * ingoingExpansion
          + outgoingExpansion * ingoingExpansionCorrection)) / 8

/--
First-order spherical Hawking/areal-geometry binding for a DFM-MKC perturbation.
The perturbed quantities are the linear truncations about the already-bound
round background surface.  This does not assert that the Newtonian-gauge field
variables determine the correction coefficients; that map remains a separate
geometric obligation.
-/
structure DFMMKCFirstOrderSphericalHawkingGeometryBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) where
  perturbedOutgoingExpansion_eq :
    P.perturbedOutgoingExpansion =
      B.outgoingExpansion + P.epsilon * P.outgoingExpansionCorrection
  perturbedIngoingExpansion_eq :
    P.perturbedIngoingExpansion =
      B.ingoingExpansion + P.epsilon * P.ingoingExpansionCorrection
  arealGradientNormSqCorrection_eq :
    P.arealGradientNormSqCorrection =
      -sphericalExpansionProductFirstVariation
        S.areaRadius B.outgoingExpansion B.ingoingExpansion
        P.areaRadiusCorrection P.outgoingExpansionCorrection
        P.ingoingExpansionCorrection
  perturbedArealGradientNormSq_eq :
    P.perturbedArealGradientNormSq =
      sphericalArealGradientNormSqFromExpansions
          S.areaRadius B.outgoingExpansion B.ingoingExpansion
        + P.epsilon * P.arealGradientNormSqCorrection
  perturbedHawkingMass_eq :
    P.perturbedHawkingMass =
      S.hawkingMass + P.epsilon *
        sphericalHawkingMassFirstVariation
          S.areaRadius B.outgoingExpansion B.ingoingExpansion
          P.areaRadiusCorrection P.outgoingExpansionCorrection
          P.ingoingExpansionCorrection

/-- First variation of `m_MS = r_A/2 * (1 - grad(r_A)^2)`. -/
def sphericalMisnerSharpMassFirstVariation
    (areaRadius arealGradientNormSq
      areaRadiusCorrection arealGradientNormSqCorrection : ℝ) : ℝ :=
  areaRadiusCorrection / 2 * (1 - arealGradientNormSq)
    - areaRadius / 2 * arealGradientNormSqCorrection

/--
The Hawking formula and the Misner-Sharp formula agree when the areal-gradient
scalar is reconstructed from the same normalized spherical expansion product.
-/
theorem sphericalHawkingMass_eq_misnerSharp_from_expansions
    (areaRadius outgoingExpansion ingoingExpansion : ℝ) :
    sphericalHawkingMassGlnNegTwo
        areaRadius outgoingExpansion ingoingExpansion =
      sphericalMisnerSharpMassFromArealGradient
        areaRadius
        (sphericalArealGradientNormSqFromExpansions
          areaRadius outgoingExpansion ingoingExpansion) := by
  unfold sphericalHawkingMassGlnNegTwo
    sphericalMisnerSharpMassFromArealGradient
    sphericalArealGradientNormSqFromExpansions
  ring

/--
The first variation of the Hawking formula is exactly the first variation of
the Misner-Sharp formula when the linearized expansion-product/areal-gradient
relation is used.
-/
theorem sphericalHawkingMassFirstVariation_eq_misnerSharp
    (areaRadius outgoingExpansion ingoingExpansion
      areaRadiusCorrection outgoingExpansionCorrection
      ingoingExpansionCorrection : ℝ) :
    sphericalHawkingMassFirstVariation
        areaRadius outgoingExpansion ingoingExpansion
        areaRadiusCorrection outgoingExpansionCorrection
        ingoingExpansionCorrection =
      sphericalMisnerSharpMassFirstVariation
        areaRadius
        (sphericalArealGradientNormSqFromExpansions
          areaRadius outgoingExpansion ingoingExpansion)
        areaRadiusCorrection
        (-sphericalExpansionProductFirstVariation
          areaRadius outgoingExpansion ingoingExpansion
          areaRadiusCorrection outgoingExpansionCorrection
          ingoingExpansionCorrection) := by
  unfold sphericalHawkingMassFirstVariation
    sphericalMisnerSharpMassFirstVariation
    sphericalArealGradientNormSqFromExpansions
    sphericalExpansionProductFirstVariation
  ring

/--
First-order Misner-Sharp binding using the same areal-gradient correction as the
Hawking geometry binding.  It remains a spherical linearized object.
-/
structure DFMMKCFirstOrderSphericalMisnerSharpGeometryBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (_H : DFMMKCFirstOrderSphericalHawkingGeometryBinding
      S x roundSymmetrySphere B P) where
  perturbedMisnerSharpMass_eq :
    P.perturbedMisnerSharpMass =
      sphericalMisnerSharpMassFromArealGradient
          S.areaRadius
          (sphericalArealGradientNormSqFromExpansions
            S.areaRadius B.outgoingExpansion B.ingoingExpansion)
        + P.epsilon *
          sphericalMisnerSharpMassFirstVariation
            S.areaRadius
            (sphericalArealGradientNormSqFromExpansions
              S.areaRadius B.outgoingExpansion B.ingoingExpansion)
            P.areaRadiusCorrection P.arealGradientNormSqCorrection

/--
The two first-order spherical mass constructions agree exactly.
-/
theorem firstOrderPerturbedHawkingMass_eq_misnerSharp
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (H : DFMMKCFirstOrderSphericalHawkingGeometryBinding
      S x roundSymmetrySphere B P)
    (M : DFMMKCFirstOrderSphericalMisnerSharpGeometryBinding
      S x roundSymmetrySphere B P H) :
    P.perturbedHawkingMass = P.perturbedMisnerSharpMass := by
  rw [H.perturbedHawkingMass_eq, M.perturbedMisnerSharpMass_eq]
  rw [B.hawkingMass_eq]
  rw [sphericalHawkingMass_eq_misnerSharp_from_expansions]
  rw [H.arealGradientNormSqCorrection_eq]
  rw [sphericalHawkingMassFirstVariation_eq_misnerSharp]

/--
Exact first-order stability identity: the Hawking-mass displacement is
`|epsilon|` times the absolute first variation.
-/
theorem firstOrderPerturbedHawkingMass_stability_eq
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (H : DFMMKCFirstOrderSphericalHawkingGeometryBinding
      S x roundSymmetrySphere B P) :
    |P.perturbedHawkingMass - S.hawkingMass| =
      |P.epsilon| *
        |sphericalHawkingMassFirstVariation
          S.areaRadius B.outgoingExpansion B.ingoingExpansion
          P.areaRadiusCorrection P.outgoingExpansionCorrection
          P.ingoingExpansionCorrection| := by
  have hdiff :
      P.perturbedHawkingMass - S.hawkingMass =
        P.epsilon *
          sphericalHawkingMassFirstVariation
            S.areaRadius B.outgoingExpansion B.ingoingExpansion
            P.areaRadiusCorrection P.outgoingExpansionCorrection
            P.ingoingExpansionCorrection := by
    rw [H.perturbedHawkingMass_eq]
    ring
  rw [hdiff, abs_mul]

/--
Because the carrier restricts `|epsilon| <= 1`, the first-order mass departure
is bounded by the absolute first-variation coefficient itself.
-/
theorem firstOrderPerturbedHawkingMass_stability_le
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (H : DFMMKCFirstOrderSphericalHawkingGeometryBinding
      S x roundSymmetrySphere B P) :
    |P.perturbedHawkingMass - S.hawkingMass| ≤
      |sphericalHawkingMassFirstVariation
        S.areaRadius B.outgoingExpansion B.ingoingExpansion
        P.areaRadiusCorrection P.outgoingExpansionCorrection
        P.ingoingExpansionCorrection| := by
  rw [firstOrderPerturbedHawkingMass_stability_eq
    S x roundSymmetrySphere B P H]
  exact mul_le_mul_of_nonneg_right
    P.epsilon_abs_le_one
    (abs_nonneg _)

/-- First-order quasi-local gate carried by the perturbed spherical surface. -/
def DFMMKCPerturbedQLGate
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) : ℝ :=
  2 * P.perturbedHawkingMass / P.perturbedAreaRadius

/--
Perturbative coercive estimate with an explicit first-order error term.  This is
kept separate from `ConcreteGravityCoerciveEstimate`, whose surface argument is
an unperturbed `AdmissibleQuasiLocalSurface`.
-/
def DFMMKCPerturbedCoerciveEstimate
    {data : SelectedEinsteinMatterCauchyData}
    (C error : ℝ)
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) : Prop :=
  DFMMKCPerturbedQLGate S x P ≤
    C * E_grav data + Flux_boundary data S + error

/--
Gate-level error generated by the exact first-order Hawking-mass stability
identity when the areal radius is held fixed.
-/
def dfmMkcFirstOrderHawkingGateError
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x) : ℝ :=
  2 * |P.epsilon| *
      |sphericalHawkingMassFirstVariation
        S.areaRadius B.outgoingExpansion B.ingoingExpansion
        P.areaRadiusCorrection P.outgoingExpansionCorrection
        P.ingoingExpansionCorrection| / S.areaRadius

/--
For a fixed-areal-radius first-order perturbation, the perturbed gate is bounded
by the background gate plus the explicit Hawking-mass stability error.
-/
theorem firstOrderPerturbedQLGate_le_background_add_error_of_fixedAreaRadius
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (H : DFMMKCFirstOrderSphericalHawkingGeometryBinding
      S x roundSymmetrySphere B P)
    (hfixed : P.areaRadiusCorrection = 0) :
    DFMMKCPerturbedQLGate S x P ≤
      QL_gate data S +
        dfmMkcFirstOrderHawkingGateError
          S x roundSymmetrySphere B P := by
  have hRadius : P.perturbedAreaRadius = S.areaRadius := by
    simpa [hfixed] using P.perturbedAreaRadius_eq
  have hstab :=
    firstOrderPerturbedHawkingMass_stability_eq
      S x roundSymmetrySphere B P H
  have hmassDiff :
      P.perturbedHawkingMass - S.hawkingMass ≤
        |P.epsilon| *
          |sphericalHawkingMassFirstVariation
            S.areaRadius B.outgoingExpansion B.ingoingExpansion
            P.areaRadiusCorrection P.outgoingExpansionCorrection
            P.ingoingExpansionCorrection| := by
    calc
      P.perturbedHawkingMass - S.hawkingMass ≤
          |P.perturbedHawkingMass - S.hawkingMass| := le_abs_self _
      _ = _ := hstab
  have hmass :
      P.perturbedHawkingMass ≤
        S.hawkingMass +
          |P.epsilon| *
            |sphericalHawkingMassFirstVariation
              S.areaRadius B.outgoingExpansion B.ingoingExpansion
              P.areaRadiusCorrection P.outgoingExpansionCorrection
              P.ingoingExpansionCorrection| := by
    linarith
  have hnum :
      2 * P.perturbedHawkingMass ≤
        2 *
          (S.hawkingMass +
            |P.epsilon| *
              |sphericalHawkingMassFirstVariation
                S.areaRadius B.outgoingExpansion B.ingoingExpansion
                P.areaRadiusCorrection P.outgoingExpansionCorrection
                P.ingoingExpansionCorrection|) := by
    linarith
  unfold DFMMKCPerturbedQLGate QL_gate
  rw [hRadius]
  unfold dfmMkcFirstOrderHawkingGateError
  have hdiv :
      2 * P.perturbedHawkingMass / S.areaRadius ≤
        2 *
          (S.hawkingMass +
            |P.epsilon| *
              |sphericalHawkingMassFirstVariation
                S.areaRadius B.outgoingExpansion B.ingoingExpansion
                P.areaRadiusCorrection P.outgoingExpansionCorrection
                P.ingoingExpansionCorrection|) / S.areaRadius := by
    apply (div_le_iff₀ S.areaRadius_pos).2
    calc
      2 * P.perturbedHawkingMass ≤
          2 *
            (S.hawkingMass +
              |P.epsilon| *
                |sphericalHawkingMassFirstVariation
                  S.areaRadius B.outgoingExpansion B.ingoingExpansion
                  P.areaRadiusCorrection P.outgoingExpansionCorrection
                  P.ingoingExpansionCorrection|) := hnum
      _ =
          (2 *
            (S.hawkingMass +
              |P.epsilon| *
                |sphericalHawkingMassFirstVariation
                  S.areaRadius B.outgoingExpansion B.ingoingExpansion
                  P.areaRadiusCorrection P.outgoingExpansionCorrection
                  P.ingoingExpansionCorrection|) / S.areaRadius) *
            S.areaRadius := by
        field_simp [ne_of_gt S.areaRadius_pos]
  calc
    2 * P.perturbedHawkingMass / S.areaRadius ≤
        2 *
          (S.hawkingMass +
            |P.epsilon| *
              |sphericalHawkingMassFirstVariation
                S.areaRadius B.outgoingExpansion B.ingoingExpansion
                P.areaRadiusCorrection P.outgoingExpansionCorrection
                P.ingoingExpansionCorrection|) / S.areaRadius := hdiv
    _ =
        2 * S.hawkingMass / S.areaRadius +
          2 * |P.epsilon| *
            |sphericalHawkingMassFirstVariation
              S.areaRadius B.outgoingExpansion B.ingoingExpansion
              P.areaRadiusCorrection P.outgoingExpansionCorrection
              P.ingoingExpansionCorrection| / S.areaRadius := by
      ring

/--
Propagation of the already-proved DFM-MKC class coefficient `C_**` through the
first-order Hawking/Misner-Sharp stability layer, on fixed-areal-radius
spherical perturbations.  The same background coefficient is retained and the
perturbation appears only as an explicit `O(|epsilon|)` gate error.
-/
theorem dfmMkcPerturbedCoerciveEstimate_of_hubbleFloor_fixedAreaRadius
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (G : FlatFLRWSphericalExpansionBinding
      S x spatiallyFlatFLRW roundSymmetrySphere B)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (H : DFMMKCFirstOrderSphericalHawkingGeometryBinding
      S x roundSymmetrySphere B P)
    (HStar : ℝ)
    (hfloor : DFMMKCHubbleFloor HStar x)
    (hsub : ExpandingFlatFLRWSubHubbleSphere
      S x spatiallyFlatFLRW roundSymmetrySphere B G)
    (hrestricted :
      RestrictedDFMMKCHawkingComparisonHypotheses
        data S x spatiallyFlatFLRW roundSymmetrySphere)
    (hfixed : P.areaRadiusCorrection = 0) :
    DFMMKCPerturbedCoerciveEstimate
      (dfmMkcHubbleFloorCStarStar HStar)
      (dfmMkcFirstOrderHawkingGateError
        S x roundSymmetrySphere B P)
      S x P := by
  have hgate :=
    firstOrderPerturbedQLGate_le_background_add_error_of_fixedAreaRadius
      S x roundSymmetrySphere B P H hfixed
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
      (dfmMkcFirstOrderHawkingGateError
        S x roundSymmetrySphere B P))

end Chronos.Frontier