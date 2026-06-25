# SELECTED_DOMAIN_DEFECT_BASIS_2026_06_24

FULL_SOLVE_PERCENT := ≈73%

A7k_TERMINAL_CLOSURE_selected := 100%

closed:
- H41_VALID_STEP_CLASSIFIER
- H41_STEP_NORMAL_FORM
- H41_STEP_GENERATOR_COVERAGE
- H41_CERTIFICATE_STEPS_ARE_TERMINAL_REALIZABLE
- CERTIFICATE_STEP_SOUNDNESS
- CERTIFICATE_SOUNDNESS
- XpT_discharge_reflects
- A7k_terminal_bridge_selected

unrestricted_terminal_closure := blocked

first blocker:
SELECTED_DOMAIN_DEFECT_BASIS

BOUNDARY := ¬ SELECTED_DOMAIN_DEFECT_BASIS_defined
BOUNDARY := ¬ selected_domain_defect_defined
BOUNDARY := ¬ UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL_proved
BOUNDARY := ¬ unrestricted_terminal_closure_proved

This does not claim executable simulation, unrestricted terminal closure, final proof of terminal_closure, peer review, or external validation.

NEXT_ACTIONS :=
1. Define SelectedDomainDefect.
2. Define defect_atoms : W_unrestricted -> Finset SelectedDomainDefect.
3. Define selected_domain_defect(w) := (defect_atoms w).card.
4. Prove defect_zero_implies_selected_domain_representable.
5. Prove defect_positive_has_terminal_repair.
