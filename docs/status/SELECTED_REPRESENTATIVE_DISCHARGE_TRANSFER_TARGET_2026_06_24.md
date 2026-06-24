# SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_TARGET_2026_06_24

## Transfer spec

```text
SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER:
  ∀ w nf,
    terminal_unrestricted(w) ->
    selected_domain(nf) ->
    terminal_T(nf) ->
    represents_terminal(nf,w) ->
    discharged_T(nf) ->
      discharged_unrestricted(w)
Conditional derivation
A7k_TERMINAL_CLOSURE_selected applied to nf:
  selected_domain(nf) ∧ terminal_T(nf)
    -> discharged_T(nf)

Transfer:
  discharged_T(nf)
    -> discharged_unrestricted(w)

unrestricted_terminal_closure :=
  conditional on SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER
Stop boundary
Do not claim final unrestricted terminal closure unless the transfer spec is proved
from non-transfer assumptions.
Weakest missing object
DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE:
  represents_terminal(nf,w) preserves discharge semantics from selected-domain
  terminal witnesses to unrestricted terminal witnesses
Boundary
BOUNDARY := ¬ DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved
BOUNDARY := ¬ SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_proved_nonconditionally
BOUNDARY := ¬ unrestricted_terminal_closure_proved_nonconditionally
