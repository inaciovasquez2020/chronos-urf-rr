# SELECTED_DOMAIN_DEFECT_SEMANTIC_SPEC_2026_06_24

## Status

This records the semantic spec layer for selected-domain defect atoms.

## Parent status

```text
SELECTED_DOMAIN_DEFECT_INPUT_TARGET_2026_06_24
Defined specs
SelectedDomainDefect_zero_completeness_spec:
  ∀ w,
    terminal_unrestricted(w) ->
    selected_domain_defect(w) = 0 ->
      selected_domain_representable(w)
SelectedDomainDefect_positive_repair_spec:
  ∀ w,
    terminal_unrestricted(w) ->
    selected_domain_defect(w) ≠ 0 ->
      ∃ d ∈ defect_atoms(w),
        repairable_selected_domain_defect(w,d)
Derived targets
defect_zero_implies_selected_domain_representable :=
  closed by SelectedDomainDefect_zero_completeness_spec

defect_positive_has_terminal_repair :=
  closed by SelectedDomainDefect_positive_repair_spec

SELECTED_DOMAIN_DEFECT_BASIS :=
  conditionally closed by:
    SelectedDomainDefect
    defect_atoms
    selected_domain_defect(w) := (defect_atoms(w)).card
    SelectedDomainDefect_zero_completeness_spec
    SelectedDomainDefect_positive_repair_spec
Remaining blocker
defect_repair_decreases_selected_domain_defect:
  repairing a selected-domain defect atom strictly decreases selected_domain_defect
  while preserving terminality and discharge equivalence
Boundary
BOUNDARY := ¬ defect_repair_decreases_selected_domain_defect_proved
BOUNDARY := ¬ UNRESTRICTED_TERMINAL_NORMALIZATION_STEP_RULE_proved
BOUNDARY := ¬ UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL_proved
BOUNDARY := ¬ unrestricted_terminal_closure_proved
NEXT_ACTIONS :=
Prove defect_repair_decreases_selected_domain_defect.
Derive UNRESTRICTED_TERMINAL_NORMALIZATION_STEP_RULE.
Derive UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL by well-founded induction.
Define UNRESTRICTED_TERMINAL_NORMAL_FORM_CONSTRUCTOR.
Resume unrestricted terminal closure.
