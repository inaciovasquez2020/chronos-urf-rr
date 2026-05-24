# Admissibility-Gated Bridge Ingredient Kernel

Status: `ADMISSIBILITY_GATED_BRIDGE_INGREDIENT_KERNEL_ADDED_THEOREM_TARGETS_OPEN`.

This packet adds the next admissible bridge ingredient after the unrestricted naive-promotion routes were refuted.

New bridge ingredient:

- `AdmissibilityGatedBridgeIngredientKernel`

The ingredient introduces one admissibility-gated bridge kernel per remaining lane:

- `R2AdmissibilityGatedBridgeIngredient`
- `R3AdmissibilityGatedBridgeIngredient`
- `NonFactorisationAdmissibilityGatedBridgeIngredient`

Each lane now has a gate requiring two explicit components:

- exclusion of the refuted naive-route counterexample class
- a positive invariant usable by a future theorem-target reduction

Closed kernel facts:

- `r2_gate_excludes_refuted_naive_route_class`
- `r2_gate_supplies_positive_invariant`
- `r3_gate_excludes_refuted_naive_route_class`
- `r3_gate_supplies_positive_invariant`
- `non_factorisation_gate_excludes_refuted_naive_route_class`
- `non_factorisation_gate_supplies_positive_invariant`

Still open:

- `DiameterSeparationFillingObstructionProofTarget`
- `UniformLocalTypeCapacityProofTarget`
- `NonFactorisationBridgeProofTarget`
- FourBridgesSourceSolved theorem closure

Does not prove:

- R2 theorem target closure
- R3 theorem target closure
- NON_FACTORISATION theorem target closure
- FourBridgesSourceSolved theorem closure
- `Chronos-RR`
- `H4.1/FGL`
- `P vs NP`
- any Clay problem
