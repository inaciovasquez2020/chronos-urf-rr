# Selected Domain Repair Field Package Bridge — 2026-06-25

## Status

Verifier-backed boundary record for the selected-domain repair field-package bridge.

## Lean target

- `Chronos.Frontier.H4_1_FGL_SelectedDomainRestriction`

## Lean source

- `lean/Chronos/Frontier/H4_1_FGL_SelectedDomainRestriction.lean`

## Bridge theorem

- `selected_domain_defect_repair_target_from_field_package`

## Target boundary

- `SELECTED_DOMAIN_DEFECT_REPAIR_TO_REALIZABLE_NORMALIZATION_BOUNDARY`

## Field package

- `SelectedDomainDefectRepairTargetField`

Fields:

```lean
repaired : W_unrestricted
repaired_realizable : selected_domain_realizable repaired
repaired_terminal : terminal_unrestricted repaired
nf : W_T
nf_represents_original : represents_terminal nf w
original_normalizes_to_nf : normalization_relation w nf
Artifact
artifacts/external_validation/selected_domain_repair_field_package_bridge_2026_06_25.json
Verifier
tools/verify_selected_domain_repair_field_package_bridge_2026_06_25.py
Expected marker: SELECTED_DOMAIN_REPAIR_FIELD_PACKAGE_BRIDGE_2026_06_25_OK
Targeted pytest
tests/test_selected_domain_repair_field_package_bridge_2026_06_25.py
Validation commands
python3 -m pytest tests/test_selected_domain_repair_field_package_bridge_2026_06_25.py
python3 tools/verify_selected_domain_repair_field_package_bridge_2026_06_25.py
lake build Chronos.Frontier.H4_1_FGL_SelectedDomainRestriction
Non-claims
Does not construct a field-package provider.
Does not prove unrestricted repair existence.
Does not prove selected-domain representability.
Does not prove terminal closure from arbitrary input.
Does not prove normalization independently of the package.
Does not attempt SELECTED_REPRESENTABLE_HAS_TERMINAL_NORMAL_FORM.
