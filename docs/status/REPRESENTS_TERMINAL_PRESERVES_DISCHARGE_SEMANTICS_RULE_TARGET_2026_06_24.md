# REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_TARGET_2026_06_24

## Status

```text
REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE := target
DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL := blocked
REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF := blocked
DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE := conditional
unrestricted_terminal_closure := conditional
final_closure_claim := stopped
Rule target
REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE:
  represents_terminal is a discharge-semantics congruence:
    terminal_unrestricted(w) ->
    selected_domain(nf) ->
    terminal_T(nf) ->
    represents_terminal(nf,w) ->
      discharge_semantics_selected(nf)
        =
      discharge_semantics_unrestricted(w)
Weakest missing object
REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT:
  show that the repository definition of represents_terminal includes or implies
  equality of selected and unrestricted discharge semantics.
Boundary
BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_proved
BOUNDARY := ¬ REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_proved
BOUNDARY := ¬ DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL_proved
BOUNDARY := ¬ DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally
BOUNDARY := ¬ unrestricted_terminal_closure_proved_nonconditionally
BOUNDARY := ¬ final_closure_claim_proved
