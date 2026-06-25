# REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF_TARGET_2026_06_24

## Status

```text
REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF := target
DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE := conditional
SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER := conditional
unrestricted_terminal_closure := conditional
final_closure_claim := stopped
Proof target
REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF:
  prove that for all w nf,
    terminal_unrestricted(w) ->
    selected_domain(nf) ->
    terminal_T(nf) ->
    represents_terminal(nf,w) ->
      discharge_semantics_selected(nf)
        =
      discharge_semantics_unrestricted(w)
Bounded proof obligations
REPRESENTS_TERMINAL_DOMAIN_ALIGNMENT:
  represents_terminal(nf,w) aligns selected terminal representatives
  with unrestricted terminal witnesses.

DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL:
  discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)
  follows from represents_terminal(nf,w) and the terminal hypotheses.

SELECTED_UNRESTRICTED_TERMINAL_DISCHARGE_EQUIVALENCE:
  selected terminal discharge and unrestricted terminal discharge denote
  the same semantic condition under representation.
Weakest missing object
DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL:
  prove discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)
  from represents_terminal(nf,w) and the terminal hypotheses.
Boundary
BOUNDARY := ¬ DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL_proved
BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF_proved
BOUNDARY := ¬ DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally
BOUNDARY := ¬ unrestricted_terminal_closure_proved_nonconditionally
BOUNDARY := ¬ final_closure_claim_proved
