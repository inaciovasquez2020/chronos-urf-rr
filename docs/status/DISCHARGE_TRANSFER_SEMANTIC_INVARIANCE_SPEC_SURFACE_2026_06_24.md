# DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_SPEC_SURFACE_2026_06_24

## Status

```text
REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY := spec_surface
DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE := closed_conditionally_by_spec
SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER := conditional
unrestricted_terminal_closure := conditional
final_closure_claim := stopped
Spec surface
REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY:
  ∀ w nf,
    terminal_unrestricted(w) ->
    selected_domain(nf) ->
    terminal_T(nf) ->
    represents_terminal(nf,w) ->
      discharge_semantics_selected(nf)
        =
      discharge_semantics_unrestricted(w)
Conditional derivation
DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE :=
  REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY
Meaning
This defines exactly when represents_terminal(nf,w) preserves discharge semantics:
the selected terminal representative nf and the unrestricted terminal witness w
must have equal discharge semantics under the representation relation.
Weakest missing proof
REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF:
  prove that the repository's represents_terminal relation satisfies
  REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY.
Boundary
BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF_proved
BOUNDARY := ¬ DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally
BOUNDARY := ¬ SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_proved_nonconditionally
BOUNDARY := ¬ unrestricted_terminal_closure_proved_nonconditionally
BOUNDARY := ¬ final_closure_claim_proved
