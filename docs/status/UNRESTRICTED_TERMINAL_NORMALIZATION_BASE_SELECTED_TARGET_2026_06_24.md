# UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED_TARGET_2026_06_24

## Target

```text
UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED:
  ∀ w,
    terminal_unrestricted(w) ->
    selected_domain_defect(w) = 0 ->
      ∃ nf : W_T,
        selected_domain(nf)
        ∧ terminal_T(nf)
        ∧ represents_terminal(nf,w)
        ∧ normalization_relation(w,nf)
First usable input
defect_zero_implies_selected_domain_representable:
  ∀ w,
    terminal_unrestricted(w) ->
    selected_domain_defect(w) = 0 ->
      selected_domain_representable(w)
Weakest missing object
SELECTED_REPRESENTABLE_HAS_TERMINAL_NORMAL_FORM:
  ∀ w,
    terminal_unrestricted(w) ->
    selected_domain_representable(w) ->
      ∃ nf : W_T,
        selected_domain(nf)
        ∧ terminal_T(nf)
        ∧ represents_terminal(nf,w)
        ∧ normalization_relation(w,nf)
Status
UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED := blocked
UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL := blocked
UNRESTRICTED_TERMINAL_NORMAL_FORM_CONSTRUCTOR := blocked
SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER := blocked
unrestricted_terminal_closure := blocked
Boundary
BOUNDARY := ¬ SELECTED_REPRESENTABLE_HAS_TERMINAL_NORMAL_FORM_proved
BOUNDARY := ¬ UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED_proved
BOUNDARY := ¬ UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL_proved
BOUNDARY := ¬ unrestricted_terminal_closure_proved
