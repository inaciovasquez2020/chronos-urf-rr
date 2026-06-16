#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN_FILE = ROOT / "lean/Chronos/Frontier/R1NativeInputBridge.lean"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

text = LEAN_FILE.read_text()
root_imports = ROOT_IMPORT.read_text()

required = [
    "def R1ExactWtrivSupportBridgeInputs_from_semantic_inputs",
    "theorem R1_exactWtriv_support_statement_from_semantic_inputs",
    "R1ExactWtrivSupportBridgeInputs D where",
    "R1LongChordExclusionTheorem D",
    "SEMANTIC_INPUT_BRIDGE_ONLY_NATIVE_GEOMETRIC_INPUTS_STILL_OPEN",
    "native construction of R1TheoremProofInputs",
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

assert "import Chronos.Frontier.R1NativeInputBridge" in root_imports

print("R1_NATIVE_INPUT_BRIDGE_LEAN_OK")
