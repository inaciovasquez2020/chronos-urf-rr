# DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL_TARGET_2026_06_24

## Status

```text
DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL := target
REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF := blocked
DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE := conditional
SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER := conditional
unrestricted_terminal_closure := conditional
final_closure_claim := stopped
Lemma target
DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL:
  ∀ w nf,
    terminal_unrestricted(w) ->
    selected_domain(nf) ->
    terminal_T(nf) ->
    represents_terminal(nf,w) ->
      discharge_semantics_selected(nf)
        =
      discharge_semantics_unrestricted(w)
Input hypotheses
terminal_unrestricted(w)
selected_domain(nf)
terminal_T(nf)
represents_terminal(nf,w)
Output conclusion
discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)
Weakest missing proof rule
REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE:
  the definition or proof rule saying represents_terminal is a congruence
  for discharge_semantics.
Boundary
BOUNDARY := ¬ REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_proved
BOUNDARY := ¬ DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL_proved
BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF_proved
BOUNDARY := ¬ DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally
BOUNDARY := ¬ unrestricted_terminal_closure_proved_nonconditionally
BOUNDARY := ¬ final_closure_claim_proved
