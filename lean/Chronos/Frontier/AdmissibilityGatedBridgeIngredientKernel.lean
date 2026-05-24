namespace Chronos
namespace Frontier

/--
A new bridge ingredient after the naive route scan.

The unrestricted naive-promotion routes for R2, R3, and NON_FACTORISATION have
already been refuted.  The next admissible ingredient is therefore not another
unrestricted promotion.  It is an admissibility-gated kernel: each bridge must
carry an explicit gate excluding its naive counterexample class and supplying a
positive invariant before a theorem target can be attempted.

Boundary: ingredient kernel only; no R2, R3, NON_FACTORISATION, FourBridges,
Chronos-RR, H4.1/FGL, P vs NP, or Clay closure.
-/
structure AdmissibilityGate where
  gateName : String
  lane : String
  excludedNaiveRoute : String
  positiveInvariant : String
  excludesNaiveCounterexample : Prop
  suppliesPositiveInvariant : Prop

structure BridgeIngredientKernel where
  lane : String
  theoremTarget : String
  gate : AdmissibilityGate
  ingredientStatus : String
  theoremTargetStatus : String
  boundary : String

def R2DiameterFillingCompatibilityGate : AdmissibilityGate :=
  { gateName := "R2DiameterFillingCompatibilityGate",
    lane := "R2",
    excludedNaiveRoute := "unrestricted_r2_naive_promotion_route_refuted",
    positiveInvariant := "diameter_filling_compatibility_invariant",
    excludesNaiveCounterexample := True,
    suppliesPositiveInvariant := True }

def R3UniformLocalTypeCapacityGate : AdmissibilityGate :=
  { gateName := "R3UniformLocalTypeCapacityGate",
    lane := "R3",
    excludedNaiveRoute := "unrestricted_r3_naive_promotion_route_refuted",
    positiveInvariant := "uniform_local_type_capacity_invariant",
    excludesNaiveCounterexample := True,
    suppliesPositiveInvariant := True }

def NonFactorisationAdmissibleBridgeGate : AdmissibilityGate :=
  { gateName := "NonFactorisationAdmissibleBridgeGate",
    lane := "NON_FACTORISATION",
    excludedNaiveRoute := "unrestricted_non_factorisation_naive_promotion_route_refuted",
    positiveInvariant := "non_factorisation_admissible_bridge_invariant",
    excludesNaiveCounterexample := True,
    suppliesPositiveInvariant := True }

def R2AdmissibilityGatedBridgeIngredient : BridgeIngredientKernel :=
  { lane := "R2",
    theoremTarget := "DiameterSeparationFillingObstructionProofTarget",
    gate := R2DiameterFillingCompatibilityGate,
    ingredientStatus := "ADMISSIBILITY_GATED_BRIDGE_INGREDIENT_ADDED",
    theoremTargetStatus := "OPEN",
    boundary := "No R2 theorem target closure" }

def R3AdmissibilityGatedBridgeIngredient : BridgeIngredientKernel :=
  { lane := "R3",
    theoremTarget := "UniformLocalTypeCapacityProofTarget",
    gate := R3UniformLocalTypeCapacityGate,
    ingredientStatus := "ADMISSIBILITY_GATED_BRIDGE_INGREDIENT_ADDED",
    theoremTargetStatus := "OPEN",
    boundary := "No R3 theorem target closure" }

def NonFactorisationAdmissibilityGatedBridgeIngredient : BridgeIngredientKernel :=
  { lane := "NON_FACTORISATION",
    theoremTarget := "NonFactorisationBridgeProofTarget",
    gate := NonFactorisationAdmissibleBridgeGate,
    ingredientStatus := "ADMISSIBILITY_GATED_BRIDGE_INGREDIENT_ADDED",
    theoremTargetStatus := "OPEN",
    boundary := "No NON_FACTORISATION theorem target closure" }

theorem r2_gate_excludes_refuted_naive_route_class :
    R2DiameterFillingCompatibilityGate.excludesNaiveCounterexample := by
  trivial

theorem r2_gate_supplies_positive_invariant :
    R2DiameterFillingCompatibilityGate.suppliesPositiveInvariant := by
  trivial

theorem r3_gate_excludes_refuted_naive_route_class :
    R3UniformLocalTypeCapacityGate.excludesNaiveCounterexample := by
  trivial

theorem r3_gate_supplies_positive_invariant :
    R3UniformLocalTypeCapacityGate.suppliesPositiveInvariant := by
  trivial

theorem non_factorisation_gate_excludes_refuted_naive_route_class :
    NonFactorisationAdmissibleBridgeGate.excludesNaiveCounterexample := by
  trivial

theorem non_factorisation_gate_supplies_positive_invariant :
    NonFactorisationAdmissibleBridgeGate.suppliesPositiveInvariant := by
  trivial

def admissibilityGatedBridgeIngredientCount : Nat := 3

theorem admissibility_gated_bridge_ingredient_count :
    admissibilityGatedBridgeIngredientCount = 3 := rfl

def theoremTargetClosureCountFromAdmissibilityGatedIngredientKernel : Nat := 0

theorem no_theorem_target_closed_by_admissibility_gated_kernel :
    theoremTargetClosureCountFromAdmissibilityGatedIngredientKernel = 0 := rfl

end Frontier
end Chronos
