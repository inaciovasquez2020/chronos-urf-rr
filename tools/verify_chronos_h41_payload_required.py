from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
lean = ROOT / "Chronos/Frontier/H41ExternalSourceCertificate.lean"

text = lean.read_text()

required = [
    "import Chronos.Frontier.H41CertifiedFamily",
    "abbrev H41LocalIndistinguishabilityStatement : Prop",
    "structure ExternalH41SourceCertificate",
    "source_id : String",
    "source_title : String",
    "localIndistinguishability : H41LocalIndistinguishabilityStatement.{u}",
    "def CONDITIONAL_H41_PAYLOAD_REQUIRED : Prop",
    "theorem H41_LocalIndistinguishability_payload_required",
    "theorem H41_LocalIndistinguishability_restricted",
]

for token in required:
    if token not in text:
        print(f"missing Lean token: {token}", file=sys.stderr)
        raise SystemExit(1)

for forbidden in ["axiom ", "admit", "sorry"]:
    if forbidden in text:
        print(f"forbidden Lean token: {forbidden}", file=sys.stderr)
        raise SystemExit(1)

print("Chronos H4.1 payload-required layer verified: CONDITIONAL_H41_PAYLOAD_REQUIRED")
