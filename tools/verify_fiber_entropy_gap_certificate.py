#!/usr/bin/env python3
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/fiber_entropy_gap_certificate.json"
DOC = ROOT / "docs/status/CHRONOS_FIBER_ENTROPY_GAP_CERTIFICATE_2026_05_08.md"
LEAN = ROOT / "Chronos/Frontier/FiberEntropyGapCertificate.lean"

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert data["status"] == "CERTIFICATE_INTERFACE_ONLY"
assert data["theorem_closure"] is False
assert data["chronos_rr_closure"] is False
assert data["h41_fgl_closure"] is False
assert data["p_vs_np_closure"] is False
assert data["missing_universal_object"] == "UniversalFiberEntropyGap"
assert data["proved_conditional"] == [
    "CertificateFiberEntropyGap implies CertificateRankImageBound"
]

for token in [
    "structure CertificateDepthBridgeInstance",
    "structure CertificateCarrierAdmissible",
    "structure CertificateFiberEntropyGap",
    "structure CertificateRankImageBound",
    "def certificateFiberEntropyGap_to_rankImageBound",
    "certified_gap",
    "certified_rank_bound := Cert.certified_gap",
]:
    assert token in lean

for token in [
    "status: CERTIFICATE_INTERFACE_ONLY",
    "CertificateFiberEntropyGap -> CertificateRankImageBound",
    "UniversalFiberEntropyGap",
    "does not prove universal FiberEntropyGap",
    "does not prove the Depth Bridge",
    "does not prove Chronos-RR closure",
    "does not prove H4.1/FGL closure",
    "does not prove P vs NP",
]:
    assert token in doc

for forbidden in [
    "theorem_closure: true",
    "Chronos-RR closure is proved",
    "H4.1/FGL closure is proved",
    "P vs NP is proved",
]:
    assert forbidden not in doc
    assert forbidden not in json.dumps(data)

if shutil.which("lake") is not None:
    subprocess.run(
        ["lake", "env", "lean", "Chronos/Frontier/FiberEntropyGapCertificate.lean"],
        cwd=ROOT,
        check=True,
    )

print("Fiber Entropy Gap certificate interface verified: CERTIFICATE_INTERFACE_ONLY")
