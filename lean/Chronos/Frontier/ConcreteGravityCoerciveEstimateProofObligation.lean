import Chronos.Frontier.SphericalCompactnessNullExpansionBridgeSurface

namespace Chronos.Frontier

/--
The current restricted DFM-MKC comparison package does not supply an upper
bound on `S.areaRadius`.  From any witness of the package, replacing only the
positive area-radius field by an arbitrarily large positive value preserves all
of the comparison hypotheses.

This blocks the specific route from the proved surface-dependent coefficient
`C(S) = (8*pi/3) * r_A^2` to a surface-independent constant unless an additional
radius-control hypothesis is added or a different estimate removes the radius
factor.
-/
theorem restrictedDFMMKCHawkingComparisonHypotheses_admits_arbitrarily_large_areaRadius
    (data : SelectedEinsteinMatterCauchyData)
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (hrestricted :
      RestrictedDFMMKCHawkingComparisonHypotheses
        data S x spatiallyFlatFLRW roundSymmetrySphere)
    (R : ℝ) :
    ∃ S' : AdmissibleQuasiLocalSurface data,
      RestrictedDFMMKCHawkingComparisonHypotheses
          data S' x spatiallyFlatFLRW roundSymmetrySphere ∧
        R < S'.areaRadius := by
  let r : ℝ := |R| + 1
  have hr : 0 < r := by
    dsimp [r]
    positivity
  let S' : AdmissibleQuasiLocalSurface data :=
    { S with
      areaRadius := r
      areaRadius_pos := hr }
  refine ⟨S', ?_, ?_⟩
  · simpa [RestrictedDFMMKCHawkingComparisonHypotheses, S'] using hrestricted
  · change R < r
    dsimp [r]
    have hRabs : R ≤ |R| := le_abs_self R
    linarith

/--
Physically selected bounded-surface subclass for the expanding flat-FLRW branch.
The DFM-MKC background uses the expanding Friedmann branch.  In the real
`g(l,n) = -2` spherical normalization, requiring the ingoing null expansion to
be nonpositive selects round spheres on or inside the flat-FLRW Hubble/apparent-
horizon scale.  No arbitrary external radius cap is introduced.
-/
def ExpandingFlatFLRWSubHubbleSphere
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (_G : FlatFLRWSphericalExpansionBinding
      S x spatiallyFlatFLRW roundSymmetrySphere B) : Prop :=
  0 < x.hubble ∧ B.ingoingExpansion ≤ 0

/--
On the expanding flat-FLRW spherical binding, `theta_- <= 0` gives the geometric
Hubble-radius cap `r_A <= 1/H`.
-/
theorem areaRadius_le_inv_hubble_of_expandingFlatFLRWSubHubbleSphere
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (G : FlatFLRWSphericalExpansionBinding
      S x spatiallyFlatFLRW roundSymmetrySphere B)
    (hsub : ExpandingFlatFLRWSubHubbleSphere
      S x spatiallyFlatFLRW roundSymmetrySphere B G) :
    S.areaRadius ≤ 1 / x.hubble := by
  rcases hsub with ⟨hH, htheta⟩
  rw [G.ingoing_eq] at htheta
  unfold normalizedSphericalIngoingExpansion at htheta
  have hscaled : 2 * (x.hubble * S.areaRadius - 1) ≤ 0 := by
    have h := (div_le_iff₀ S.areaRadius_pos).1 htheta
    simpa using h
  have hHr : x.hubble * S.areaRadius ≤ 1 := by
    nlinarith
  apply (le_div_iff₀ hH).2
  simpa [mul_comm] using hHr

/--
Surface-independent coefficient for a fixed expanding DFM-MKC FLRW state,
obtained from the geometric Hubble-radius cap `R_* = 1/H`.
-/
def dfmMkcExpandingFlatFLRWCStar
    (x : RestrictedDFMMKCEnergyState) : ℝ :=
  (8 * Real.pi / 3) * (1 / x.hubble) ^ 2

/--
For the expanding sub-Hubble spherical subclass, the previously proved
surface-dependent coefficient is bounded by the state-wise constant
`C_* = (8*pi/3) * H^-2`.  This is surface-independent for fixed `x`; no uniform
lower bound on `H` across all DFM-MKC states is asserted.
-/
theorem concreteGravityCoerciveEstimate_of_expandingFlatFLRWSubHubbleSphere
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW roundSymmetrySphere : Prop)
    (B : RealSphericalHawkingMassBinding S roundSymmetrySphere)
    (G : FlatFLRWSphericalExpansionBinding
      S x spatiallyFlatFLRW roundSymmetrySphere B)
    (hsub : ExpandingFlatFLRWSubHubbleSphere
      S x spatiallyFlatFLRW roundSymmetrySphere B G)
    (hrestricted :
      RestrictedDFMMKCHawkingComparisonHypotheses
        data S x spatiallyFlatFLRW roundSymmetrySphere) :
    ConcreteGravityCoerciveEstimate
      (dfmMkcExpandingFlatFLRWCStar x) data S := by
  have hrBound : S.areaRadius ≤ 1 / x.hubble :=
    areaRadius_le_inv_hubble_of_expandingFlatFLRWSubHubbleSphere
      S x spatiallyFlatFLRW roundSymmetrySphere B G hsub
  rcases hsub with ⟨hH, _⟩
  have hr0 : 0 ≤ S.areaRadius := le_of_lt S.areaRadius_pos
  have hInv0 : 0 ≤ 1 / x.hubble := by
    positivity
  have hsq : S.areaRadius ^ 2 ≤ (1 / x.hubble) ^ 2 := by
    have hprod :
        0 ≤ ((1 / x.hubble) - S.areaRadius) *
          ((1 / x.hubble) + S.areaRadius) :=
      mul_nonneg (sub_nonneg.mpr hrBound) (add_nonneg hInv0 hr0)
    nlinarith
  have hk : 0 ≤ (8 * Real.pi / 3 : ℝ) := by
    positivity
  have hC :
      (8 * Real.pi / 3) * S.areaRadius ^ 2 ≤
        dfmMkcExpandingFlatFLRWCStar x := by
    unfold dfmMkcExpandingFlatFLRWCStar
    exact mul_le_mul_of_nonneg_left hsq hk
  have hE : 0 ≤ E_grav data := by
    simpa [E_grav] using data.curvatureEnergyControl_nonnegative
  have hlocal :
      ConcreteGravityCoerciveEstimate
        ((8 * Real.pi / 3) * S.areaRadius ^ 2) data S :=
    concreteGravityCoerciveEstimate_of_flatFLRW_spherical_binding
      S x spatiallyFlatFLRW roundSymmetrySphere B G hrestricted
  unfold ConcreteGravityCoerciveEstimate at hlocal ⊢
  exact hlocal.trans
    (add_le_add_right
      (mul_le_mul_of_nonneg_right hC hE)
      (Flux_boundary data S))

structure ConcreteGravityCoerciveEstimateProofObligation where
  id : String
  status : String
  selected_data_class : String
  curvature_energy_norm : String
  quasi_local_collapse_functional : String
  boundary_flux_error : String
  estimate_shape : String
  proof_obligation : String
  boundary : List String
deriving Repr, DecidableEq

def concreteGravityCoerciveEstimateProofObligationV1 :
    ConcreteGravityCoerciveEstimateProofObligation :=
  { id := "CONCRETE_GRAVITY_COERCIVE_ESTIMATE_PROOF_OBLIGATION_V1"
    status := "PROOF_OBLIGATION_ONLY_NO_COERCIVE_ESTIMATE_PROOF"
    selected_data_class :=
      "Selected admissible Einstein-matter Cauchy data with fixed gauge, regularity threshold, finite curvature-energy norm, and controlled boundary flux."
    curvature_energy_norm :=
      "E_grav(data)"
    quasi_local_collapse_functional :=
      "QL_gate(data; S)"
    boundary_flux_error :=
      "Flux_boundary(data; S)"
    estimate_shape :=
      "QL_gate(data; S) <= C * E_grav(data) + Flux_boundary(data; S)"
    proof_obligation :=
      "Prove the coercive estimate for every selected admissible datum data and admissible quasi-local surface S, with an explicit constant C under the fixed gauge, regularity, energy, and boundary-flux hypotheses."
    boundary :=
      [ "proof obligation only",
        "no coercive estimate proof",
        "no analytic estimate proof",
        "no Einstein-matter theorem",
        "no collapse theorem",
        "no Cosmic Censorship",
        "no Hoop Conjecture",
        "no quantum gravity",
        "no unrestricted Chronos-RR",
        "no unrestricted H4.1/FGL",
        "no P vs NP",
        "no Clay problem" ] }

theorem concreteGravityCoerciveEstimateProofObligationV1_status :
    concreteGravityCoerciveEstimateProofObligationV1.status =
      "PROOF_OBLIGATION_ONLY_NO_COERCIVE_ESTIMATE_PROOF" := rfl

theorem concreteGravityCoerciveEstimateProofObligationV1_shape :
    concreteGravityCoerciveEstimateProofObligationV1.estimate_shape =
      "QL_gate(data; S) <= C * E_grav(data) + Flux_boundary(data; S)" := rfl

theorem concreteGravityCoerciveEstimateProofObligationV1_boundary :
    "no coercive estimate proof" ∈
      concreteGravityCoerciveEstimateProofObligationV1.boundary := by
  simp [concreteGravityCoerciveEstimateProofObligationV1]

end Chronos.Frontier
