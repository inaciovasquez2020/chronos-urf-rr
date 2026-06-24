# REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_TARGET_2026_06_24

## Status

```text
REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD := target
REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT := blocked
REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE := blocked
DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE := conditional
unrestricted_terminal_closure := conditional
final_closure_claim := stopped
Field target
REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD:
  a concrete field, lemma, or definitional clause inside represents_terminal
  recording:

    discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)
Required field contract
input_relation := represents_terminal(nf,w)
selected_side := discharge_semantics_selected(nf)
unrestricted_side := discharge_semantics_unrestricted(w)
required_equality := discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)
Weakest missing realization
REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION:
  locate or add the concrete repository-level field, lemma, or definitional
  clause carrying the discharge semantics equality.
Boundary
BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_proved
BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_proved
BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_proved
BOUNDARY := ¬ DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally
BOUNDARY := ¬ unrestricted_terminal_closure_proved_nonconditionally
BOUNDARY := ¬ final_closure_claim_proved
