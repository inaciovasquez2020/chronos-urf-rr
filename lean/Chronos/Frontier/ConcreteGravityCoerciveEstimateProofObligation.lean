import Chronos.Frontier.ConcreteGravityAnalyticEstimateReadiness

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
