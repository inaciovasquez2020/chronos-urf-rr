# REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_TARGET_2026_06_24

## Status

```text
REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE := target
REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION := blocked
REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE := blocked
DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE := conditional
unrestricted_terminal_closure := conditional
final_closure_claim := stopped
Source target
REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE:
  identify the existing repository object or add one minimal clause that supplies:

    discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)

  for:

    represents_terminal(nf,w)
Admissible source forms
existing represents_terminal structure field
existing lemma about represents_terminal semantic equality
new minimal definitional clause on represents_terminal
adapter lemma from representation semantics to discharge semantics equality
Required payload
relation := represents_terminal(nf,w)
selected_payload := discharge_semantics_selected(nf)
unrestricted_payload := discharge_semantics_unrestricted(w)
required_equality := discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)
Weakest missing location
REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_LOCATION:
  locate the concrete repo file/object where represents_terminal is defined
  or where its semantic payload can be minimally extended.
Boundary
BOUNDARY := ¬ REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_LOCATION_identified
BOUNDARY := ¬ REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_identified
BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_proved
BOUNDARY := ¬ DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally
BOUNDARY := ¬ unrestricted_terminal_closure_proved_nonconditionally
BOUNDARY := ¬ final_closure_claim_proved
