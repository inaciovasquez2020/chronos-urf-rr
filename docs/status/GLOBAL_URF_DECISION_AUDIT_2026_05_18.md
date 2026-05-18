# Global URF Decision Audit

Status: `STATUS_SURFACE_ONLY`

Global verdict: `OPEN_WITH_EXPLICIT_SINK_LEMMAS`

## Normalized claim form

Each claim is normalized as:

```text
A_i => B_i
where A_i is the explicit assumption domain and B_i is the theorem-level conclusion.
Current claim table
Claim	A_i	B_i	Assumption status	Lean proof target	Countermodel target	Sink lemma	Verdict
finite_list_positive_uniform_floor	nonempty finite list of strictly positive real masses	there exists a strictly positive uniform lower floor	proved	Chronos.Frontier.FiniteListPositiveUniformFloor	none: list-coded finite positive support	none	proved_surface
finite_support_restricted_ufeg_to_restricted_chronos_rr	finite positive support plus restricted admissible domain	restricted UniversalFiberEntropyGap feeds restricted Chronos-RR	conditional	Chronos.Frontier.FiniteSupportRestrictedUFEGToRestrictedChronosRR	unrestricted arbitrary-fiber-mass data	uniform positivity or restricted-domain invariant	conditional_surface
unrestricted_universal_fiber_entropy_gap	arbitrary fiber-mass data	unrestricted UniversalFiberEntropyGap	open_frontier	none	zero or vanishing fiber-mass family	unrestricted uniform positivity/coercivity	countermodel_required
unrestricted_chronos_rr_h41_fgl_p_np_clay	unrestricted Chronos-RR/H4.1/FGL terminal hypotheses	P vs NP or Clay-level closure	open_frontier	none	boundary-overclaim audit	unrestricted UniversalFiberEntropyGap plus unrestricted DepthBridge	open_missing_lemma
Dependency DAG sinks
uniform positivity or restricted-domain invariant
unrestricted uniform positivity/coercivity
unrestricted UniversalFiberEntropyGap plus unrestricted DepthBridge
Boundary
Does not prove:
unrestricted UniversalFiberEntropyGap
unrestricted Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay problem
