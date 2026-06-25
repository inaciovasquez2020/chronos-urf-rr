# DEFECT_REPAIR_NORMALIZATION_TARGET_2026_06_24

## Status

This records the repair-descent target after `SELECTED_DOMAIN_DEFECT_SEMANTIC_SPEC_2026_06_24`.

## Repair descent

```text
defect_repair_decreases_selected_domain_defect:
  ∀ w d,
    terminal_unrestricted(w) ->
    d ∈ defect_atoms(w) ->
    repairable_selected_domain_defect(w,d) ->
      ∃ w',
        terminal_unrestricted(w')
        ∧ normalization_step(w,w')
        ∧ discharge_equivalent(w',w)
        ∧ selected_domain_defect(w') < selected_domain_defect(w)

status := closed_conditionally_by_repair_descent_spec
Derived normalization step
UNRESTRICTED_TERMINAL_NORMALIZATION_STEP_RULE :=
  closed conditionally using:
    defect_positive_has_terminal_repair
    defect_repair_decreases_selected_domain_defect
Blocked well-founded induction
UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL :=
  blocked

first_missing_object :=
  UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED
Weakest missing object
UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED:
  ∀ w,
    terminal_unrestricted(w) ->
    selected_domain_defect(w) = 0 ->
      ∃ nf : W_T,
        selected_domain(nf)
        ∧ terminal_T(nf)
        ∧ represents_terminal(nf,w)
        ∧ normalization_relation(w,nf)
Boundary
BOUNDARY := ¬ UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED_proved
BOUNDARY := ¬ UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL_proved
BOUNDARY := ¬ UNRESTRICTED_TERMINAL_NORMAL_FORM_CONSTRUCTOR_defined
BOUNDARY := ¬ unrestricted_terminal_closure_proved
NEXT_ACTIONS :=
Prove UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED.
Derive UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL by well-founded induction.
Define UNRESTRICTED_TERMINAL_NORMAL_FORM_CONSTRUCTOR.
Prove SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER.
Resume unrestricted terminal closure.
