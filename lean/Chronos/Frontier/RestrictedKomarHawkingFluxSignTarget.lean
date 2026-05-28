namespace Chronos.Frontier

structure RestrictedKomarHawkingFluxSignTarget where
  id : String
  status : String
  parent_candidate : String
  target_lemma : String
  restricted_regime : String
  flux_object : String
  sign_claim_shape : String
  use_in_estimate : String
  missing_inputs : List String
  boundary : List String
deriving Repr, DecidableEq

def restrictedKomarHawkingFluxSignTargetV1 :
    RestrictedKomarHawkingFluxSignTarget :=
  { id := "RESTRICTED_KOMAR_HAWKING_FLUX_SIGN_TARGET_V1"
    status := "RESTRICTED_FLUX_SIGN_TARGET_ONLY_NO_SIGN_PROOF"
    parent_candidate := "RESTRICTED_STATIONARY_GRAVITY_ESTIMATE_CANDIDATE_V1"
    target_lemma := "RestrictedKomarHawkingFluxSign"
    restricted_regime :=
      "static-or-axisymmetric asymptotically flat Einstein-matter data with rotationally symmetric quasi-local surface S of area-radius r > 2M"
    flux_object :=
      "Komar-type boundary integral or Hawking quasi-local mass term on S"
    sign_claim_shape :=
      "Flux_boundary(data; S) >= 0 under the restricted stationary, energy, orientation, and decay hypotheses"
    use_in_estimate :=
      "Provides the nonnegative boundary-flux term needed by the restricted stationary candidate estimate."
    missing_inputs :=
      [ "orientation convention for S",
        "energy condition used for sign",
        "normalization of Komar/Hawking quantity",
        "asymptotic decay hypothesis",
        "surface admissibility hypothesis" ]
    boundary :=
      [ "target lemma only",
        "no flux sign proof",
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

theorem restrictedKomarHawkingFluxSignTargetV1_status :
    restrictedKomarHawkingFluxSignTargetV1.status =
      "RESTRICTED_FLUX_SIGN_TARGET_ONLY_NO_SIGN_PROOF" := rfl

theorem restrictedKomarHawkingFluxSignTargetV1_lemma :
    restrictedKomarHawkingFluxSignTargetV1.target_lemma =
      "RestrictedKomarHawkingFluxSign" := rfl

theorem restrictedKomarHawkingFluxSignTargetV1_boundary :
    "no flux sign proof" ∈ restrictedKomarHawkingFluxSignTargetV1.boundary := by
  simp [restrictedKomarHawkingFluxSignTargetV1]

end Chronos.Frontier
