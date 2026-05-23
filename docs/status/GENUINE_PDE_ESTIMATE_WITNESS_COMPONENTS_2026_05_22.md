# GENUINE_PDE_ESTIMATE_WITNESS_COMPONENTS_2026_05_22

Status: FOUR_COMPONENT_ASSEMBLY_CLOSED_PDE_COMPONENT_PROOFS_OPEN.

Repository:
- chronos-urf-rr

Lean module:
- Chronos.Frontier.GenuinePDEEstimateWitnessComponents

Four required components:
1. constraint_propagation
2. energy_condition_preservation
3. continuation_up_to_collapse_threshold
4. collapse_criterion_from_restricted_seed

Closed results:
- genuinePDEEstimateWitness_from_components
- analyticEstimatePackageExists_from_genuinePDEComponents
- bootstrapKernel_from_genuinePDEComponents
- collapseGate_from_genuinePDEComponents

Remaining missing object:
- GENUINE_PDE_ESTIMATE_WITNESS_COMPONENTS_EXIST

Boundary:
This proves assembly from the four PDE components. It does not prove the PDE components themselves.

Does not prove:
- genuine Einstein-matter PDE existence
- genuine Einstein-matter PDE regularity
- genuine Einstein-matter PDE continuation
- unconditional gravity closure
- unrestricted gravity closure
- cosmic censorship
- hoop conjecture
- four-dimensional collapse theorem
- unrestricted QL_CollapseGate
- unrestricted UniversalBoundaryCompactness
- Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem
