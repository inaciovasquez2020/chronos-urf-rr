# DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_TARGET_2026_06_24

## Status

```text
DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE := target
SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER := conditional
unrestricted_terminal_closure := conditional
final_closure_claim := stopped
Statement
DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE:
  ∀ w nf,
    terminal_unrestricted(w) ->
    selected_domain(nf) ->
    terminal_T(nf) ->
    represents_terminal(nf,w) ->
      discharge_semantics_selected(nf)
        =
      discharge_semantics_unrestricted(w)
Role
represents_terminal(nf,w) preserves discharge semantics from selected-domain
terminal witnesses to unrestricted terminal witnesses.
Blocked upgrades
SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_nonconditional := blocked
unrestricted_terminal_closure_nonconditional := blocked
final_closure_claim := stopped
Boundary
BOUNDARY := ¬ DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved
BOUNDARY := ¬ SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_proved_nonconditionally
BOUNDARY := ¬ unrestricted_terminal_closure_proved_nonconditionally
BOUNDARY := ¬ final_closure_claim_proved
