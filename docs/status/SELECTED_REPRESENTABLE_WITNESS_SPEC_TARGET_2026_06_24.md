# SELECTED_REPRESENTABLE_WITNESS_SPEC_TARGET_2026_06_24

## Semantic spec

```text
selected_domain_representable_witness_spec:
  ∀ w,
    selected_domain_representable(w) ->
      ∃ nf : W_T,
        selected_domain(nf)
        ∧ terminal_T(nf)
        ∧ represents_terminal(nf,w)
        ∧ normalization_relation(w,nf)
Derived targets
SELECTED_REPRESENTABLE_HAS_TERMINAL_NORMAL_FORM :=
  closed conditionally by selected_domain_representable_witness_spec

UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED :=
  closed conditionally using:
    defect_zero_implies_selected_domain_representable
    selected_domain_representable_witness_spec

UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL :=
  closed conditionally by well-founded induction on selected_domain_defect

UNRESTRICTED_TERMINAL_NORMAL_FORM_CONSTRUCTOR :=
  closed conditionally by choice from relation total
Weakest missing object
SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER:
  ∀ w nf,
    terminal_unrestricted(w) ->
    selected_domain(nf) ->
    terminal_T(nf) ->
    represents_terminal(nf,w) ->
    discharged_T(nf) ->
      discharged_unrestricted(w)
Boundary
BOUNDARY := ¬ SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_proved
BOUNDARY := ¬ unrestricted_terminal_closure_proved
