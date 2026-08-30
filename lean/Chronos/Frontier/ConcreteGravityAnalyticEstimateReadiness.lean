import Mathlib

namespace Chronos.Frontier

/--
Typed interface for the selected Einstein-matter Cauchy data used by the
concrete gravity estimate program.
-/
structure SelectedEinsteinMatterCauchyData where
  point : Type
  spatialMetric : point → Fin 3 → Fin 3 → Real
  secondFundamentalForm : point → Fin 3 → Fin 3 → Real
  matterEnergyDensity : point → Real
  matterMomentumDensity : point → Fin 3 → Real
  gaugeFixed : Prop
  einsteinMatterConstraintsSatisfied : Prop
  regularityOrder : Nat
  requiredRegularity : Nat
  regularity_sufficient : requiredRegularity ≤ regularityOrder
  curvatureEnergyControl : Real
  curvatureEnergyControl_nonnegative : 0 ≤ curvatureEnergyControl
  boundaryFluxControl : Real
  boundaryFluxControl_nonnegative : 0 ≤ boundaryFluxControl

/--
Typed admissible quasi-local surface inside one selected Cauchy datum.
The Hawking mass and positive area-radius observables are recorded so that a
numerical compactness gate can be defined without adding extra arguments.
-/
structure AdmissibleQuasiLocalSurface
    (data : SelectedEinsteinMatterCauchyData) where
  surfacePoint : Type
  inclusion : surfacePoint → data.point
  closed : Prop
  compact : Prop
  smooth : Prop
  embedded : Prop
  twoDimensional : Prop
  spacelike : Prop
  hawkingMass : Real
  areaRadius : Real
  areaRadius_pos : 0 < areaRadius

/-- Dimensionless quasi-local compactness gate in the normalization `2 m_H / r_A`. -/
noncomputable def QL_gate
    (data : SelectedEinsteinMatterCauchyData)
    (S : AdmissibleQuasiLocalSurface data) : ℝ :=
  2 * S.hawkingMass / S.areaRadius

/-- Named curvature-energy control on the selected Einstein-matter data. -/
def E_grav (data : SelectedEinsteinMatterCauchyData) : ℝ :=
  data.curvatureEnergyControl

/-- Named nonnegative boundary-flux control for an admissible quasi-local surface. -/
def Flux_boundary
    (data : SelectedEinsteinMatterCauchyData)
    (_S : AdmissibleQuasiLocalSurface data) : ℝ :=
  data.boundaryFluxControl

/--
Typed proposition for the concrete gravity coercive estimate at constant `C`.
This states the analytic target only and supplies no proof of the inequality.
-/
def ConcreteGravityCoerciveEstimate
    (C : ℝ)
    (data : SelectedEinsteinMatterCauchyData)
    (S : AdmissibleQuasiLocalSurface data) : Prop :=
  QL_gate data S ≤ C * E_grav data + Flux_boundary data S

/--
Restricted quasi-local gate-to-mass control target.  The exact stationary,
asymptotic-flatness, symmetry, sign, and decay hypotheses remain abstract here
and must be supplied before any theorem can use this target.
-/
def RestrictedQLGateMassControl
    (restrictedHypotheses : Prop)
    (C : ℝ)
    (data : SelectedEinsteinMatterCauchyData)
    (S : AdmissibleQuasiLocalSurface data) : Prop :=
  restrictedHypotheses → QL_gate data S ≤ C * E_grav data

/--
Scalar Hawking-mass/area-radius bridge underlying the restricted gate control.
This is a target proposition only; no geometric or analytic proof is supplied.
-/
def RestrictedMassCompactnessBridge
    (restrictedHypotheses : Prop)
    (C : ℝ)
    (data : SelectedEinsteinMatterCauchyData)
    (S : AdmissibleQuasiLocalSurface data) : Prop :=
  restrictedHypotheses →
    2 * S.hawkingMass ≤ C * E_grav data * S.areaRadius

/--
Positive area-radius turns the scalar mass/compactness bridge into the
restricted quasi-local gate control by division by `S.areaRadius`.
-/
theorem restrictedQLGateMassControl_of_massCompactnessBridge
    (restrictedHypotheses : Prop)
    (C : ℝ)
    (data : SelectedEinsteinMatterCauchyData)
    (S : AdmissibleQuasiLocalSurface data)
    (hbridge : RestrictedMassCompactnessBridge restrictedHypotheses C data S) :
    RestrictedQLGateMassControl restrictedHypotheses C data S := by
  intro hrestricted
  change 2 * S.hawkingMass / S.areaRadius ≤ C * E_grav data
  exact (div_le_iff₀ S.areaRadius_pos).2 (hbridge hrestricted)

/--
At the geometric coefficient `2 / r_A`, a Hawking-mass bound by the selected
energy control is sufficient for the restricted scalar compactness bridge.
This is purely algebraic and does not prove the Hawking-mass bound itself.
-/
theorem restrictedMassCompactnessBridge_of_hawkingMass_le_energy
    (restrictedHypotheses : Prop)
    (data : SelectedEinsteinMatterCauchyData)
    (S : AdmissibleQuasiLocalSurface data)
    (hmass : restrictedHypotheses → S.hawkingMass ≤ E_grav data) :
    RestrictedMassCompactnessBridge
      restrictedHypotheses (2 / S.areaRadius) data S := by
  intro hrestricted
  calc
    2 * S.hawkingMass ≤ 2 * E_grav data := by
      exact mul_le_mul_of_nonneg_left (hmass hrestricted) (by norm_num)
    _ = (2 / S.areaRadius) * E_grav data * S.areaRadius := by
      field_simp [ne_of_gt S.areaRadius_pos]

/--
Charge-reduced DFM-MKC background state used only to identify the restricted
cosmological energy object.  The fields mirror the canonical DFM-MKC branch:
positive `alpha`, `beta`, and scale factor, with nonzero radial field `phi`.
-/
structure RestrictedDFMMKCEnergyState where
  alpha : ℝ
  beta : ℝ
  scaleFactor : ℝ
  phi : ℝ
  phiDot : ℝ
  qTheta : ℝ
  rhoStar : ℝ
  mPhiSquared : ℝ
  lambdaPhi : ℝ
  visibleEnergyDensity : ℝ
  cosmologicalConstant : ℝ
  newtonG : ℝ
  hubble : ℝ
  alpha_pos : 0 < alpha
  beta_pos : 0 < beta
  scaleFactor_pos : 0 < scaleFactor
  phi_ne_zero : phi ≠ 0
  newtonG_pos : 0 < newtonG

/-- Canonical DFM-MKC potential `U(phi)`. -/
def dfmMkcPotential (x : RestrictedDFMMKCEnergyState) : ℝ :=
  x.rhoStar
    + (1 / 2 : ℝ) * x.mPhiSquared * x.phi ^ 2
    + (1 / 4 : ℝ) * x.lambdaPhi * x.phi ^ 4

/--
Canonical charge-reduced DFM-MKC dark-sector energy density.
-/
def dfmMkcEnergyDensity (x : RestrictedDFMMKCEnergyState) : ℝ :=
  (1 / 2 : ℝ) * x.alpha * x.phiDot ^ 2
    + x.qTheta ^ 2 /
      (2 * x.beta * x.scaleFactor ^ 6 * x.phi ^ 2)
    + dfmMkcPotential x

/--
Geometrized total FLRW energy density used by the `2m/r` normalization:
`G * (rho_visible + rho_DFM-MKC) + Lambda/(8*pi)`.
This is the restricted meaning assigned to `E_grav`; it is not ADM or Bondi
mass and does not alter the general `E_grav` interface outside this branch.
-/
def dfmMkcGeometrizedTotalEnergyDensity
    (x : RestrictedDFMMKCEnergyState) : ℝ :=
  x.newtonG * (x.visibleEnergyDensity + dfmMkcEnergyDensity x)
    + x.cosmologicalConstant / (8 * Real.pi)

/--
Weakest concrete DFM-MKC/FLRW comparison package used here: the selected
surface is a round symmetry sphere in the spatially flat FLRW branch, the
DFM-MKC Friedmann equation holds, and the abstract `E_grav` control is
identified with the geometrized DFM-MKC total energy density above.
-/
def RestrictedDFMMKCHawkingComparisonHypotheses
    (data : SelectedEinsteinMatterCauchyData)
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW : Prop)
    (roundSymmetrySphere : Prop) : Prop :=
  spatiallyFlatFLRW ∧
    roundSymmetrySphere ∧
    S.closed ∧
    S.compact ∧
    S.smooth ∧
    S.embedded ∧
    x.hubble ^ 2 =
      x.cosmologicalConstant / 3
        + (8 * Real.pi * x.newtonG / 3) *
          (x.visibleEnergyDensity + dfmMkcEnergyDensity x) ∧
    E_grav data = dfmMkcGeometrizedTotalEnergyDensity x

/--
Exact external GR lemma still missing on the DFM-MKC route.  In spherical
symmetry the intended bridge is Hawking mass = Misner-Sharp mass, followed by
the spatially flat FLRW Misner-Sharp energy formula.  No theorem providing
that bridge exists in either repository at this checkpoint.

This target is deliberately an inequality, sufficient for the later gate
estimate, and does not prove `ConcreteGravityCoerciveEstimate`.
-/
def RestrictedHawkingMassEnergyControl
    (data : SelectedEinsteinMatterCauchyData)
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW : Prop)
    (roundSymmetrySphere : Prop) : Prop :=
  RestrictedDFMMKCHawkingComparisonHypotheses
      data S x spatiallyFlatFLRW roundSymmetrySphere →
    S.hawkingMass ≤
      (4 * Real.pi / 3) * S.areaRadius ^ 3 * E_grav data

/--
External spherical-geometry bridge: on a round symmetry sphere, the Hawking
mass agrees with a selected Misner-Sharp mass.  This proposition is typed only;
no proof of the GR identity is supplied here.
-/
def RestrictedHawkingMisnerSharpSphericalBridge
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (misnerSharpMass : ℝ)
    (roundSymmetrySphere : Prop) : Prop :=
  roundSymmetrySphere → S.hawkingMass = misnerSharpMass

/--
External DFM-MKC FLRW bridge: spatial flatness plus the repository's
charge-reduced Friedmann equation identifies the selected Misner-Sharp mass
with the enclosed geometrized DFM-MKC total energy of the round sphere.
This proposition is typed only; its geometric derivation is not supplied.
-/
def RestrictedDFMMKCFLRWMisnerSharpEnergyIdentity
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (misnerSharpMass : ℝ)
    (spatiallyFlatFLRW : Prop) : Prop :=
  spatiallyFlatFLRW →
    x.hubble ^ 2 =
      x.cosmologicalConstant / 3
        + (8 * Real.pi * x.newtonG / 3) *
          (x.visibleEnergyDensity + dfmMkcEnergyDensity x) →
    misnerSharpMass =
      (4 * Real.pi / 3) * S.areaRadius ^ 3 *
        dfmMkcGeometrizedTotalEnergyDensity x

/--
Canonical geometrized Misner-Sharp mass for a round sphere on the spatially
flat FLRW branch, `m_MS = r_A^3 H^2 / 2`.
-/
def dfmMkcFLRWMisnerSharpMass
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState) : ℝ :=
  (1 / 2 : ℝ) * S.areaRadius ^ 3 * x.hubble ^ 2

/--
For the canonical flat-FLRW Misner-Sharp mass, the DFM-MKC Friedmann equation
proves the enclosed-energy identity exactly.  This is the algebraic FLRW step;
it does not prove the Hawking/Misner-Sharp spherical geometry identity.
-/
theorem dfmMkcFLRWMisnerSharpMass_eq_enclosedEnergy
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (hfriedmann :
      x.hubble ^ 2 =
        x.cosmologicalConstant / 3
          + (8 * Real.pi * x.newtonG / 3) *
            (x.visibleEnergyDensity + dfmMkcEnergyDensity x)) :
    dfmMkcFLRWMisnerSharpMass S x =
      (4 * Real.pi / 3) * S.areaRadius ^ 3 *
        dfmMkcGeometrizedTotalEnergyDensity x := by
  simp only [dfmMkcFLRWMisnerSharpMass, hfriedmann,
    dfmMkcGeometrizedTotalEnergyDensity]
  field_simp [Real.pi_ne_zero]
  <;> ring

/--
The canonical flat-FLRW mass therefore supplies the previously abstract
DFM-MKC Misner-Sharp energy bridge whenever spatial flatness is assumed.
-/
theorem restrictedDFMMKCFLRWMisnerSharpEnergyIdentity_for_canonicalMass
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW : Prop) :
    RestrictedDFMMKCFLRWMisnerSharpEnergyIdentity
      S x (dfmMkcFLRWMisnerSharpMass S x) spatiallyFlatFLRW := by
  intro _ hfriedmann
  exact dfmMkcFLRWMisnerSharpMass_eq_enclosedEnergy S x hfriedmann

/--
Composition theorem only: if the Hawking/Misner-Sharp spherical bridge and the
DFM-MKC FLRW Misner-Sharp energy identity are available, then the restricted
Hawking-mass/energy control follows.  This proves only the logical composition;
it does not prove either external bridge and does not prove the unrestricted
coercive estimate.
-/
theorem restrictedHawkingMassEnergyControl_of_misnerSharp_bridges
    (data : SelectedEinsteinMatterCauchyData)
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (spatiallyFlatFLRW : Prop)
    (roundSymmetrySphere : Prop)
    (misnerSharpMass : ℝ)
    (hHawking :
      RestrictedHawkingMisnerSharpSphericalBridge
        S misnerSharpMass roundSymmetrySphere)
    (hMisnerSharp :
      RestrictedDFMMKCFLRWMisnerSharpEnergyIdentity
        S x misnerSharpMass spatiallyFlatFLRW) :
    RestrictedHawkingMassEnergyControl
      data S x spatiallyFlatFLRW roundSymmetrySphere := by
  intro hrestricted
  rcases hrestricted with
    ⟨hflat, hround, hclosed, hcompact, hsmooth, hembedded, hfriedmann, henergy⟩
  have hhawkingMass : S.hawkingMass = misnerSharpMass := hHawking hround
  have hmisnerSharpEnergy :
      misnerSharpMass =
        (4 * Real.pi / 3) * S.areaRadius ^ 3 *
          dfmMkcGeometrizedTotalEnergyDensity x :=
    hMisnerSharp hflat hfriedmann
  calc
    S.hawkingMass = misnerSharpMass := hhawkingMass
    _ = (4 * Real.pi / 3) * S.areaRadius ^ 3 *
        dfmMkcGeometrizedTotalEnergyDensity x := hmisnerSharpEnergy
    _ = (4 * Real.pi / 3) * S.areaRadius ^ 3 * E_grav data := by
      rw [henergy]
    _ ≤ (4 * Real.pi / 3) * S.areaRadius ^ 3 * E_grav data := le_rfl

structure ConcreteGravityAnalyticEstimateReadiness where
  id : String
  status : String
  target : String
  selected_data_class : String
  curvature_energy_norm : String
  quasi_local_collapse_functional : String
  boundary_flux_error : String
  readiness_items : List String
  missing_proof : String
  boundary : List String
deriving Repr, DecidableEq

def concreteGravityAnalyticEstimateReadinessV1 :
    ConcreteGravityAnalyticEstimateReadiness :=
  { id := "CONCRETE_GRAVITY_ANALYTIC_ESTIMATE_READINESS_V1"
    status := "ANALYTIC_ESTIMATE_READINESS_PACKAGE_ONLY_NO_ESTIMATE_PROOF"
    target :=
      "Prepare the concrete object dictionary needed to attempt ConcreteGravityCoerciveEstimate."
    selected_data_class :=
      "Selected admissible Einstein-matter Cauchy data with fixed gauge, regularity threshold, finite curvature-energy norm, and controlled boundary flux."
    curvature_energy_norm :=
      "A named curvature-energy control quantity E_grav(data) intended to dominate the selected curvature and matter-energy components used by the quasi-local collapse gate."
    quasi_local_collapse_functional :=
      "A named quasi-local collapse functional QL_gate(data; S) measuring selected trapped-surface or compactness-gate deficit on admissible quasi-local surfaces S."
    boundary_flux_error :=
      "A named nonnegative boundary term Flux_boundary(data; S) controlling leakage across the selected quasi-local boundary."
    readiness_items :=
      [ "selected data class named",
        "curvature-energy norm named",
        "quasi-local collapse functional named",
        "boundary-flux error term named",
        "coercive estimate shape named",
        "missing proof isolated" ]
    missing_proof :=
      "ConcreteGravityCoerciveEstimate: prove QL_gate(data; S) <= C * E_grav(data) + Flux_boundary(data; S), or the project-specific stronger orientation of this inequality, for the selected admissible Einstein-matter data class."
    boundary :=
      [ "readiness package only",
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

theorem concreteGravityAnalyticEstimateReadinessV1_status :
    concreteGravityAnalyticEstimateReadinessV1.status =
      "ANALYTIC_ESTIMATE_READINESS_PACKAGE_ONLY_NO_ESTIMATE_PROOF" := rfl

theorem concreteGravityAnalyticEstimateReadinessV1_has_selected_data_class :
    concreteGravityAnalyticEstimateReadinessV1.selected_data_class =
      "Selected admissible Einstein-matter Cauchy data with fixed gauge, regularity threshold, finite curvature-energy norm, and controlled boundary flux." := rfl

theorem concreteGravityAnalyticEstimateReadinessV1_missing_proof :
    concreteGravityAnalyticEstimateReadinessV1.missing_proof =
      "ConcreteGravityCoerciveEstimate: prove QL_gate(data; S) <= C * E_grav(data) + Flux_boundary(data; S), or the project-specific stronger orientation of this inequality, for the selected admissible Einstein-matter data class." := rfl

theorem concreteGravityAnalyticEstimateReadinessV1_boundary :
    "no analytic estimate proof" ∈
      concreteGravityAnalyticEstimateReadinessV1.boundary := by
  simp [concreteGravityAnalyticEstimateReadinessV1]

end Chronos.Frontier