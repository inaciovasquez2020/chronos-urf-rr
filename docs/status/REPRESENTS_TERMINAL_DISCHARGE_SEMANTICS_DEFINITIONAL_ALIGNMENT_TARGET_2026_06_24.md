# REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_TARGET_2026_06_24

## Status

```text
REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT := target
REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE := blocked
DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL := blocked
DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE := conditional
unrestricted_terminal_closure := conditional
final_closure_claim := stopped
Alignment target
REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT:
  show that the repository definition of represents_terminal includes or implies
  equality of selected and unrestricted discharge semantics.
Required definitional content
selected representative terminal semantics
unrestricted terminal witness semantics
discharge semantics equality
representation relation compatibility
Weakest missing object
REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD:
  a concrete field, lemma, or definitional clause inside represents_terminal
  that records:

    discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)
Boundary
BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_proved
BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_proved
BOUNDARY := ¬ REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_proved
BOUNDARY := ¬ DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally
BOUNDARY := ¬ unrestricted_terminal_closure_proved_nonconditionally
BOUNDARY := ¬ final_closure_claim_proved
