import Chronos.Frontier.SphericalCollapseGateThresholdSurface
import Chronos.Frontier.SphericalNullExpansionCriterionSurface
import Chronos.Frontier.ConcreteGravityAnalyticEstimateReadiness

namespace Chronos
namespace Frontier

/--
Real-valued Hawking mass of a round symmetry sphere in the null-normal
normalization `g(l,n) = -2`.
-/
noncomputable def sphericalHawkingMassGlnNegTwo
    (areaRadius outgoingExpansion ingoingExpansion : ℝ) : ℝ :=
  areaRadius / 2 *
    (1 + areaRadius ^ 2 * outgoingExpansion * ingoingExpansion / 4)

/--
Binding from the previously free `S.hawkingMass` scalar to the real round-sphere
Hawking formula in the fixed `g(l,n) = -2` normalization.  This records the
chosen normalization and round-sphere formula only; it does not yet derive the
expansions from an areal-radius gradient.
-/
structure RealSphericalHawkingMassBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (roundSymmetrySphere : Prop) where
  outgoingExpansion : ℝ
  ingoingExpansion : ℝ
  round : roundSymmetrySphere
  hawkingMass_eq :
    S.hawkingMass =
      sphericalHawkingMassGlnNegTwo
        S.areaRadius outgoingExpansion ingoingExpansion

/-- Outgoing null expansion `theta_+ = 2 l(r_A) / r_A`. -/
noncomputable def normalizedSphericalOutgoingExpansion
    (areaRadius outgoingArealDerivative : ℝ) : ℝ :=
  2 * outgoingArealDerivative / areaRadius

/-- Ingoing null expansion `theta_- = 2 n(r_A) / r_A`. -/
noncomputable def normalizedSphericalIngoingExpansion
    (areaRadius ingoingArealDerivative : ℝ) : ℝ :=
  2 * ingoingArealDerivative / areaRadius

/--
Areal-radius gradient norm in the `g(l,n) = -2` null normalization:
`grad(r_A)^2 = - l(r_A) n(r_A)`.
-/
def normalizedSphericalArealGradientNormSq
    (outgoingArealDerivative ingoingArealDerivative : ℝ) : ℝ :=
  -(outgoingArealDerivative * ingoingArealDerivative)

/--
The normalized real null expansions recover the areal-radius gradient norm:
`r_A^2 * theta_+ * theta_- / 4 = - grad(r_A)^2`.
-/
theorem normalizedSphericalExpansionProduct_eq_neg_arealGradientNormSq
    (areaRadius outgoingArealDerivative ingoingArealDerivative : ℝ)
    (hr : areaRadius ≠ 0) :
    areaRadius ^ 2 *
        normalizedSphericalOutgoingExpansion
          areaRadius outgoingArealDerivative *
        normalizedSphericalIngoingExpansion
          areaRadius ingoingArealDerivative / 4 =
      - normalizedSphericalArealGradientNormSq
          outgoingArealDerivative ingoingArealDerivative := by
  unfold normalizedSphericalOutgoingExpansion
    normalizedSphericalIngoingExpansion
    normalizedSphericalArealGradientNormSq
  field_simp [hr]
  <;> ring

/-- Geometrized Misner-Sharp mass written through the areal-gradient norm. -/
def sphericalMisnerSharpMassFromArealGradient
    (areaRadius arealGradientNormSq : ℝ) : ℝ :=
  areaRadius / 2 * (1 - arealGradientNormSq)

/--
For normalized real spherical null derivatives, the round-sphere Hawking mass
formula equals the Misner-Sharp mass formula written through `grad(r_A)^2`.
-/
theorem sphericalHawkingMass_eq_misnerSharp_of_normalizedDerivatives
    (areaRadius outgoingArealDerivative ingoingArealDerivative : ℝ)
    (hr : areaRadius ≠ 0) :
    sphericalHawkingMassGlnNegTwo
        areaRadius
        (normalizedSphericalOutgoingExpansion
          areaRadius outgoingArealDerivative)
        (normalizedSphericalIngoingExpansion
          areaRadius ingoingArealDerivative) =
      sphericalMisnerSharpMassFromArealGradient
        areaRadius
        (normalizedSphericalArealGradientNormSq
          outgoingArealDerivative ingoingArealDerivative) := by
  unfold sphericalHawkingMassGlnNegTwo
    sphericalMisnerSharpMassFromArealGradient
  rw [normalizedSphericalExpansionProduct_eq_neg_arealGradientNormSq
    areaRadius outgoingArealDerivative ingoingArealDerivative hr]
  ring

/--
On the spatially flat FLRW branch, normalized radial null derivatives are
`H r_A + 1` and `H r_A - 1`, so `grad(r_A)^2 = 1 - H^2 r_A^2`.
-/
theorem normalizedSphericalArealGradientNormSq_flatFLRW
    (areaRadius hubble : ℝ) :
    normalizedSphericalArealGradientNormSq
        (hubble * areaRadius + 1)
        (hubble * areaRadius - 1) =
      1 - hubble ^ 2 * areaRadius ^ 2 := by
  unfold normalizedSphericalArealGradientNormSq
  ring

/--
The areal-gradient Misner-Sharp formula on the flat FLRW branch is exactly the
canonical DFM-MKC FLRW Misner-Sharp mass already proved from the Friedmann
sector.
-/
theorem sphericalMisnerSharpMassFromArealGradient_flatFLRW
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState) :
    sphericalMisnerSharpMassFromArealGradient
        S.areaRadius
        (normalizedSphericalArealGradientNormSq
          (x.hubble * S.areaRadius + 1)
          (x.hubble * S.areaRadius - 1)) =
      dfmMkcFLRWMisnerSharpMass S x := by
  unfold sphericalMisnerSharpMassFromArealGradient
    normalizedSphericalArealGradientNormSq
    dfmMkcFLRWMisnerSharpMass
  ring

/--
Concrete flat-FLRW binding for the real spherical null expansions.  It binds
the already-recorded Hawking surface expansions to the normalized radial null
derivatives of the flat FLRW areal radius; it does not assume Hawking =
Misner-Sharp.
-/
structure FlatFLRWSphericalExpansionBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW : Prop)
    (roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere) where
  flat : spatiallyFlatFLRW
  outgoing_eq :
    B.outgoingExpansion =
      normalizedSphericalOutgoingExpansion
        S.areaRadius (x.hubble * S.areaRadius + 1)
  ingoing_eq :
    B.ingoingExpansion =
      normalizedSphericalIngoingExpansion
        S.areaRadius (x.hubble * S.areaRadius - 1)

/--
The real Hawking binding plus the normalized flat-FLRW expansion binding proves
the previously external Hawking/Misner-Sharp spherical bridge for the canonical
DFM-MKC FLRW Misner-Sharp mass.
-/
theorem restrictedHawkingMisnerSharpSphericalBridge_of_flatFLRW_binding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (G : FlatFLRWSphericalExpansionBinding
      S x spatiallyFlatFLRW roundSymmetrySphere B) :
    RestrictedHawkingMisnerSharpSphericalBridge
      S (dfmMkcFLRWMisnerSharpMass S x) roundSymmetrySphere := by
  intro _
  calc
    S.hawkingMass =
        sphericalHawkingMassGlnNegTwo
          S.areaRadius B.outgoingExpansion B.ingoingExpansion :=
      B.hawkingMass_eq
    _ = sphericalHawkingMassGlnNegTwo
          S.areaRadius
          (normalizedSphericalOutgoingExpansion
            S.areaRadius (x.hubble * S.areaRadius + 1))
          (normalizedSphericalIngoingExpansion
            S.areaRadius (x.hubble * S.areaRadius - 1)) := by
      rw [G.outgoing_eq, G.ingoing_eq]
    _ = sphericalMisnerSharpMassFromArealGradient
          S.areaRadius
          (normalizedSphericalArealGradientNormSq
            (x.hubble * S.areaRadius + 1)
            (x.hubble * S.areaRadius - 1)) := by
      exact sphericalHawkingMass_eq_misnerSharp_of_normalizedDerivatives
        S.areaRadius
        (x.hubble * S.areaRadius + 1)
        (x.hubble * S.areaRadius - 1)
        (ne_of_gt S.areaRadius_pos)
    _ = dfmMkcFLRWMisnerSharpMass S x :=
      sphericalMisnerSharpMassFromArealGradient_flatFLRW S x

/--
Feeding the proved flat-FLRW Hawking/Misner-Sharp bridge and the already-proved
DFM-MKC FLRW Misner-Sharp energy identity into the verified composition yields
the restricted Hawking-mass/energy control.  The unrestricted coercive estimate
is not asserted here.
-/
theorem restrictedHawkingMassEnergyControl_of_flatFLRW_spherical_binding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (G : FlatFLRWSphericalExpansionBinding
      S x spatiallyFlatFLRW roundSymmetrySphere B) :
    RestrictedHawkingMassEnergyControl
      data S x spatiallyFlatFLRW roundSymmetrySphere := by
  exact restrictedHawkingMassEnergyControl_of_misnerSharp_bridges
    data S x spatiallyFlatFLRW roundSymmetrySphere
    (dfmMkcFLRWMisnerSharpMass S x)
    (restrictedHawkingMisnerSharpSphericalBridge_of_flatFLRW_binding
      S x spatiallyFlatFLRW roundSymmetrySphere B G)
    (restrictedDFMMKCFLRWMisnerSharpEnergyIdentity_for_canonicalMass
      S x spatiallyFlatFLRW)

/--
Under the concrete DFM-MKC flat-FLRW comparison package and the real spherical
bindings, Hawking mass is exactly the enclosed geometrized DFM-MKC energy of
the round sphere.
-/
theorem hawkingMass_eq_dfmMkcEnclosedEnergy_of_flatFLRW_spherical_binding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (G : FlatFLRWSphericalExpansionBinding
      S x spatiallyFlatFLRW roundSymmetrySphere B)
    (hrestricted :
      RestrictedDFMMKCHawkingComparisonHypotheses
        data S x spatiallyFlatFLRW roundSymmetrySphere) :
    S.hawkingMass =
      (4 * Real.pi / 3) * S.areaRadius ^ 3 * E_grav data := by
  rcases hrestricted with
    ⟨hflat, hround, hclosed, hcompact, hsmooth, hembedded, hfriedmann, henergy⟩
  have hhawking :
      S.hawkingMass = dfmMkcFLRWMisnerSharpMass S x :=
    restrictedHawkingMisnerSharpSphericalBridge_of_flatFLRW_binding
      S x spatiallyFlatFLRW roundSymmetrySphere B G hround
  have hmisnerSharp :
      dfmMkcFLRWMisnerSharpMass S x =
        (4 * Real.pi / 3) * S.areaRadius ^ 3 *
          dfmMkcGeometrizedTotalEnergyDensity x :=
    dfmMkcFLRWMisnerSharpMass_eq_enclosedEnergy S x hfriedmann
  calc
    S.hawkingMass = dfmMkcFLRWMisnerSharpMass S x := hhawking
    _ = (4 * Real.pi / 3) * S.areaRadius ^ 3 *
        dfmMkcGeometrizedTotalEnergyDensity x := hmisnerSharp
    _ = (4 * Real.pi / 3) * S.areaRadius ^ 3 * E_grav data := by
      rw [henergy]

/--
The restricted DFM-MKC flat-FLRW spherical branch has an exact quasi-local gate
identity.  This is stronger than the previously recorded one-sided mass
control, but the coefficient remains surface-dependent through `r_A^2`.
-/
theorem qlGate_eq_dfmMkcEnergy_of_flatFLRW_spherical_binding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (G : FlatFLRWSphericalExpansionBinding
      S x spatiallyFlatFLRW roundSymmetrySphere B)
    (hrestricted :
      RestrictedDFMMKCHawkingComparisonHypotheses
        data S x spatiallyFlatFLRW roundSymmetrySphere) :
    QL_gate data S =
      (8 * Real.pi / 3) * S.areaRadius ^ 2 * E_grav data := by
  unfold QL_gate
  rw [hawkingMass_eq_dfmMkcEnclosedEnergy_of_flatFLRW_spherical_binding
    S x spatiallyFlatFLRW roundSymmetrySphere B G hrestricted]
  field_simp [ne_of_gt S.areaRadius_pos]
  <;> ring

/--
Restricted proved instance of the concrete coercive inequality.  The coefficient
is `C(S) = (8*pi/3) r_A^2`; nonnegative boundary flux upgrades the exact gate
identity to the repository's `ConcreteGravityCoerciveEstimate` proposition.
This is not a uniform or unrestricted coercive estimate.
-/
theorem concreteGravityCoerciveEstimate_of_flatFLRW_spherical_binding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (G : FlatFLRWSphericalExpansionBinding
      S x spatiallyFlatFLRW roundSymmetrySphere B)
    (hrestricted :
      RestrictedDFMMKCHawkingComparisonHypotheses
        data S x spatiallyFlatFLRW roundSymmetrySphere) :
    ConcreteGravityCoerciveEstimate
      ((8 * Real.pi / 3) * S.areaRadius ^ 2) data S := by
  unfold ConcreteGravityCoerciveEstimate
  rw [qlGate_eq_dfmMkcEnergy_of_flatFLRW_spherical_binding
    S x spatiallyFlatFLRW roundSymmetrySphere B G hrestricted]
  have hflux : 0 ≤ Flux_boundary data S := by
    simpa [Flux_boundary] using data.boundaryFluxControl_nonnegative
  exact le_add_of_nonneg_right hflux

/--
Repository-native bridge input from the spherical compactness threshold
`arealRadius <= 2 * misnerSharpMass` to the null-expansion sign condition.

The bridge field is explicit: this file records the interface-level bridge and
does not derive the geometric threshold-to-expansion theorem from Einstein
geometry.
-/
structure SphericalCompactnessNullExpansionBridgeInput where
  thresholdInput : SphericalCollapseGateInput
  expansionInput : SphericalNullExpansionInput
  threshold_to_outer_marginal :
    SphericalCollapseGate thresholdInput ->
      FutureOuterMarginalSphericalSurface expansionInput

def SphericalCompactnessToNullExpansionBridge
    (B : SphericalCompactnessNullExpansionBridgeInput) : Prop :=
  SphericalCollapseGate B.thresholdInput ->
    FutureOuterMarginalSphericalSurface B.expansionInput

theorem spherical_compactness_threshold_implies_outer_marginal_by_bridge
    (B : SphericalCompactnessNullExpansionBridgeInput) :
    SphericalCompactnessToNullExpansionBridge B := by
  intro h
  exact B.threshold_to_outer_marginal h

theorem spherical_compactness_threshold_implies_trapped_or_marginal_by_bridge
    (B : SphericalCompactnessNullExpansionBridgeInput) :
    SphericalCollapseGate B.thresholdInput ->
      TrappedOrMarginalByNullExpansions B.expansionInput := by
  intro h
  exact marginal_spherical_null_expansions_imply_trapped_or_marginal
    B.expansionInput
    (B.threshold_to_outer_marginal h)

/--
Boundary marker.

This file closes only the repository-native conditional bridge interface from
the spherical compactness gate to the spherical null-expansion criterion.
It does not prove the geometric threshold-to-expansion theorem, nonspherical
collapse exclusion, Cosmic Censorship, the Hoop Conjecture, or unrestricted
UniversalBoundaryCompactness.
-/
def SphericalCompactnessNullExpansionBridgeBoundary : Prop := True

theorem spherical_compactness_null_expansion_bridge_boundary_verified :
    SphericalCompactnessNullExpansionBridgeBoundary := by
  trivial

end Frontier
end Chronos
