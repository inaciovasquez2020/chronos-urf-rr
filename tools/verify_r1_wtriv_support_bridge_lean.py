#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN_FILE = ROOT / "lean/Chronos/Frontier/R1WtrivSupportBridge.lean"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

text = LEAN_FILE.read_text()
root_imports = ROOT_IMPORT.read_text()

required = [
    "def R1WtrivSupportGenerationBridge",
    "structure R1ExactWtrivSupportBridgeInputs",
    "theorem R1WtrivSupportGenerationBridge_from_semantic_inputs",
    "theorem R1_exactWtriv_support_statement_from_R1a_R1b_R1c_bridge",
    "R1LongChordExclusionTheorem D",
    "CONDITIONAL_SEMANTIC_BRIDGE_ONLY_NOT_R1_NATIVE_CLOSURE",
    "Does not prove native R1 geometry",
]

for needle in required:
    assert needle in text, needle

for forbidden in [
    "axiom ",
    "opaque ",
    "sorry",
    "admit",
    "R1 solved",
    "FGL solved",
    "scientific closure achieved",
]:
    assert forbidden not in text, forbidden

assert "def LongChordExclusionProofTarget : Prop := True" not in text
assert "import Chronos.Frontier.R1WtrivSupportBridge" in root_imports

print("R1_WTRIV_SUPPORT_BRIDGE_LEAN_OK")
