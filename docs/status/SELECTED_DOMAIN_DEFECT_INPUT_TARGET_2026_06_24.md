# SELECTED_DOMAIN_DEFECT_INPUT_TARGET_2026_06_24

## Status

This records the selected-domain defect input target after the unrestricted witness carrier surface.

## Definitions

```text
SelectedDomainDefect :=
  input carrier for finite atoms measuring why an unrestricted terminal witness is not selected-domain representable

defect_atoms : W_unrestricted -> Finset SelectedDomainDefect

selected_domain_defect(w) :=
  (defect_atoms(w)).card
Blocked proof targets
defect_zero_implies_selected_domain_representable:
  ∀ w,
    terminal_unrestricted(w) ->
    selected_domain_defect(w) = 0 ->
      selected_domain_representable(w)

status := blocked
first_missing_object := SelectedDomainDefect_zero_completeness_spec
defect_positive_has_terminal_repair:
  ∀ w,
    terminal_unrestricted(w) ->
    selected_domain_defect(w) ≠ 0 ->
      ∃ d ∈ defect_atoms(w),
        repairable_selected_domain_defect(w,d)

status := blocked
first_missing_object := SelectedDomainDefect_positive_repair_spec
Weakest missing object
SELECTED_DOMAIN_DEFECT_SEMANTIC_SPEC :=
  finite defect atoms are complete for selected-domain representability at zero
  and repairable whenever nonzero
Boundary
BOUNDARY := ¬ defect_zero_implies_selected_domain_representable_proved
BOUNDARY := ¬ defect_positive_has_terminal_repair_proved
BOUNDARY := ¬ SELECTED_DOMAIN_DEFECT_BASIS_proved
BOUNDARY := ¬ unrestricted_terminal_closure_proved
NEXT_ACTIONS :=
Define SelectedDomainDefect_zero_completeness_spec.
Define SelectedDomainDefect_positive_repair_spec.
Derive defect_zero_implies_selected_domain_representable.
Derive defect_positive_has_terminal_repair.
Resume SELECTED_DOMAIN_DEFECT_BASIS.
