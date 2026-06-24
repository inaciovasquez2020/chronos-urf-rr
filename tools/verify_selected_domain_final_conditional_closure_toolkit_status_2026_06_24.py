from pathlib import Path

artifact = Path("artifacts/external_validation/selected_domain_final_conditional_closure_toolkit_status_2026_06_24.json").read_text()
doc = Path("docs/status/SELECTED_DOMAIN_FINAL_CONDITIONAL_CLOSURE_TOOLKIT_STATUS_2026_06_24.md").read_text()

assert Path("lean/Chronos/Frontier/SelectedDomainDefectTerminalClosureStack.lean").is_file()
assert Path("lean/Chronos/Frontier/SelectedDomainDefectTerminalClosureAssumptionDischarge.lean").is_file()
assert Path("lean/Chronos/Frontier/SelectedDomainDefectSemanticComponentTargets.lean").is_file()
assert Path("lean/Chronos/Frontier/SelectedDomainRepairDescentObligationInterface.lean").is_file()
assert Path("lean/Chronos/Frontier/SelectedDomainZeroDefectReentryObligationInterface.lean").is_file()
assert Path("lean/Chronos/Frontier/SelectedDomainUnrestrictedTerminalNormalizationObligationInterface.lean").is_file()
assert Path("lean/Chronos/Frontier/SelectedDomainFinalClosureObligationInterface.lean").is_file()
assert Path("lean/Chronos/Frontier/SelectedDomainUnrestrictedOblivionClosureObligationInterface.lean").is_file()
assert Path("lean/Chronos/Frontier/SelectedDomainDefectAtomsConstructionTarget.lean").is_file()
assert Path("lean/Chronos/Frontier/SelectedDomainFinalConditionalClosureBridge.lean").is_file()

assert "lean/Chronos/Frontier/SelectedDomainDefectTerminalClosureStack.lean" in artifact and "lean/Chronos/Frontier/SelectedDomainDefectTerminalClosureStack.lean" in doc
assert "lean/Chronos/Frontier/SelectedDomainDefectTerminalClosureAssumptionDischarge.lean" in artifact and "lean/Chronos/Frontier/SelectedDomainDefectTerminalClosureAssumptionDischarge.lean" in doc
assert "lean/Chronos/Frontier/SelectedDomainDefectSemanticComponentTargets.lean" in artifact and "lean/Chronos/Frontier/SelectedDomainDefectSemanticComponentTargets.lean" in doc
assert "lean/Chronos/Frontier/SelectedDomainRepairDescentObligationInterface.lean" in artifact and "lean/Chronos/Frontier/SelectedDomainRepairDescentObligationInterface.lean" in doc
assert "lean/Chronos/Frontier/SelectedDomainZeroDefectReentryObligationInterface.lean" in artifact and "lean/Chronos/Frontier/SelectedDomainZeroDefectReentryObligationInterface.lean" in doc
assert "lean/Chronos/Frontier/SelectedDomainUnrestrictedTerminalNormalizationObligationInterface.lean" in artifact and "lean/Chronos/Frontier/SelectedDomainUnrestrictedTerminalNormalizationObligationInterface.lean" in doc
assert "lean/Chronos/Frontier/SelectedDomainFinalClosureObligationInterface.lean" in artifact and "lean/Chronos/Frontier/SelectedDomainFinalClosureObligationInterface.lean" in doc
assert "lean/Chronos/Frontier/SelectedDomainUnrestrictedOblivionClosureObligationInterface.lean" in artifact and "lean/Chronos/Frontier/SelectedDomainUnrestrictedOblivionClosureObligationInterface.lean" in doc
assert "lean/Chronos/Frontier/SelectedDomainDefectAtomsConstructionTarget.lean" in artifact and "lean/Chronos/Frontier/SelectedDomainDefectAtomsConstructionTarget.lean" in doc
assert "lean/Chronos/Frontier/SelectedDomainFinalConditionalClosureBridge.lean" in artifact and "lean/Chronos/Frontier/SelectedDomainFinalConditionalClosureBridge.lean" in doc

assert "REQUEST_MET := bounded final bridge interface built and verifier-backed" in doc
assert "REQUEST_NOT_MET := unconditional unrestricted Oblivion Atom closure proof" in doc
assert "SelectedDomainFinalConditionalClosureBridge" in doc and "SelectedDomainFinalConditionalClosureBridge" in artifact
assert "SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix" in doc and "SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix" in artifact
assert "SelectedDomainDefectAtomsConstructionTarget" in doc and "SelectedDomainDefectAtomsConstructionTarget" in artifact
assert "SelectedDomainDefectSemanticComponentTargets" in doc and "SelectedDomainDefectSemanticComponentTargets" in artifact
assert "unrestricted_oblivion_atom_closure_statement_from_final_bridge" in doc and "unrestricted_oblivion_atom_closure_statement_from_final_bridge" in artifact
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in doc and "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in artifact
assert "unconditional_unrestricted_oblivion_atom_closure_solved" in doc and "unconditional_unrestricted_oblivion_atom_closure_solved" in artifact
assert "SELECTED_DOMAIN_FINAL_CONDITIONAL_CLOSURE_TOOLKIT_STATUS_2026_06_24_OK" in doc
assert "request_met" in artifact
assert "No unconditional unrestricted Oblivion Atom closure proof was claimed." in artifact
assert "toolkit_status_verified" in artifact

assert "3c8ec4a0" in artifact and "3c8ec4a0" in doc
assert "d10d949b" in artifact and "d10d949b" in doc
assert "3d43db21" in artifact and "3d43db21" in doc
assert "65b3906c" in artifact and "65b3906c" in doc
assert "1de76d56" in artifact and "1de76d56" in doc
assert "b9b852a5" in artifact and "b9b852a5" in doc
assert "16592125" in artifact and "16592125" in doc
assert "f0f447bf" in artifact and "f0f447bf" in doc
assert "6555961c" in artifact and "6555961c" in doc
assert "54098552" in artifact and "54098552" in doc
assert "ad3f2b9f" in artifact and "ad3f2b9f" in doc
assert "0ce64e0d" in artifact and "0ce64e0d" in doc

print("SELECTED_DOMAIN_FINAL_CONDITIONAL_CLOSURE_TOOLKIT_STATUS_2026_06_24_OK")
