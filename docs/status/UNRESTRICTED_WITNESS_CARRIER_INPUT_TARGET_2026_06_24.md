# UNRESTRICTED_WITNESS_CARRIER_INPUT_TARGET_2026_06_24

## Status

This records the unrestricted witness carrier interface needed before the selected-domain defect basis can be formalized.

## Carrier surface

```text
W_unrestricted
terminal_unrestricted
selected_domain_representable
normalization_relation
discharge_equivalent
discharged_unrestricted
Parent status
SELECTED_DOMAIN_DEFECT_BASIS_2026_06_24
Weakest missing object
SELECTED_DOMAIN_DEFECT_BASIS

∃ defect_atoms : W_unrestricted -> Finset SelectedDomainDefect,
  ∀ w : W_unrestricted,
    terminal_unrestricted(w) ->
      selected_domain_defect(w) = defect_atoms(w).card
      ∧ (selected_domain_defect(w) = 0 ->
          selected_domain_representable(w))
      ∧ (selected_domain_defect(w) ≠ 0 ->
          ∃ d ∈ defect_atoms(w),
            repairable_selected_domain_defect(w,d))
Boundary
BOUNDARY := ¬ SelectedDomainDefect_defined
BOUNDARY := ¬ defect_atoms_defined
BOUNDARY := ¬ selected_domain_defect_defined
BOUNDARY := ¬ SELECTED_DOMAIN_DEFECT_BASIS_proved
BOUNDARY := ¬ unrestricted_terminal_closure_proved
Claim boundary
This does not claim SelectedDomainDefect, defect_atoms, selected_domain_defect, SELECTED_DOMAIN_DEFECT_BASIS, or unrestricted terminal closure.
NEXT_ACTIONS :=
Define SelectedDomainDefect.
Define defect_atoms : W_unrestricted -> Finset SelectedDomainDefect.
Define selected_domain_defect(w) := (defect_atoms w).card.
Prove defect_zero_implies_selected_domain_representable.
Prove defect_positive_has_terminal_repair.
