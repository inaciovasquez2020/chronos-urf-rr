namespace Chronos.Frontier

structure RestrictedStationaryGravityEstimateCandidate where
  id : String
  status : String
  restricted_regime : String
  selected_surface : String
  restricted_energy : String
  restricted_flux : String
  candidate_estimate : String
  known_ingredient_route : List String
  missing_lemmas : List String
  malformed_shape_test : String
  boundary : List String
deriving Repr, DecidableEq

def restrictedStationaryGravityEstimateCandidateV1 :
    RestrictedStationaryGravityEstimateCandidate :=
  { id := "RESTRICTED_STATIONARY_GRAVITY_ESTIMATE_CANDIDATE_V1"
    status := "RESTRICTED_CANDIDATE_LEMMA_ONLY_NO_GRAVITY_ESTIMATE_PROOF"
    restricted_regime :=
      "static-or-axisymmetric asymptotically flat Einstein-matter data with rotationally symmetric quasi-local surface S of area-radius r > 2M"
    selected_surface :=
      "rotationally symmetric quasi-local surface S in a spacelike slice"
    restricted_energy :=
      "ADM mass, or Bondi mass in an asymptotically flat end, with matter term integral int_Sigma mu_0 dV"
    restricted_flux :=
      "Komar-type boundary integral or Hawking quasi-local mass term on S, subject to positivity/sign and decay hypotheses"
    candidate_estimate :=
      "QL_gate(data; S) <= C(r, M) * (int_Sigma mu_0 dV + O(r^-3)) + Flux_infty^(0)(r)"
    known_ingredient_route :=
      [ "restrict to stationary symmetry",
        "choose rotationally symmetric quasi-local surface",
        "instantiate E_grav(data) by ADM/Bondi mass plus matter-energy density",
        "instantiate Flux_boundary(data; S) by Komar/Hawking boundary quantity",
        "test whether the general coercive-estimate orientation survives in the restricted model" ]
    missing_lemmas :=
      [ "RestrictedStationarySurfaceAdmissibility",
        "RestrictedKomarHawkingFluxSign",
        "RestrictedAsymptoticDecayErrorBound",
        "RestrictedQLGateMassControl" ]
    malformed_shape_test :=
      "Failure of the restricted candidate estimate under these symmetry, sign, and decay hypotheses flags the unrestricted ConcreteGravityCoerciveEstimate shape as malformed or incorrectly oriented."
    boundary :=
      [ "restricted candidate lemma only",
        "no restricted estimate proof",
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

theorem restrictedStationaryGravityEstimateCandidateV1_status :
    restrictedStationaryGravityEstimateCandidateV1.status =
      "RESTRICTED_CANDIDATE_LEMMA_ONLY_NO_GRAVITY_ESTIMATE_PROOF" := rfl

theorem restrictedStationaryGravityEstimateCandidateV1_candidate :
    restrictedStationaryGravityEstimateCandidateV1.candidate_estimate =
      "QL_gate(data; S) <= C(r, M) * (int_Sigma mu_0 dV + O(r^-3)) + Flux_infty^(0)(r)" := rfl

theorem restrictedStationaryGravityEstimateCandidateV1_boundary :
    "no restricted estimate proof" ∈
      restrictedStationaryGravityEstimateCandidateV1.boundary := by
  simp [restrictedStationaryGravityEstimateCandidateV1]

end Chronos.Frontier
