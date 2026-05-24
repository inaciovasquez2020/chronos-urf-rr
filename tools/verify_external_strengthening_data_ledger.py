#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/ExternalStrengtheningDataLedger.lean"
ART = ROOT / "artifacts/chronos/external_strengthening_data_ledger_2026_05_24.json"
DOC = ROOT / "docs/status/EXTERNAL_STRENGTHENING_DATA_LEDGER_2026_05_24.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

STATUS = "EXTERNAL_STRENGTHENING_DATA_LEDGER_ONLY_NO_THEOREM_PROMOTION"

URLS = [
    "https://iopscience.iop.org/article/10.1149/2754-2726/ae525b",
    "https://www.researchgate.net/publication/404180923_An_Optimized_UVM-Based_Verification_Framework_for_Accelerating_Functional_Coverage_Convergence_in_ASIC_Front-End_Design",
    "https://www.goldstandard.org/news/five-methodologies-launched-for-consultation-april-2026",
    "https://www.undp.org/sites/g/files/zskgke326/files/2026-05/annex-irrf-2026-2029-revised.pdf",
    "https://upr-info.org/sites/default/files/general-document/2026-03/UPR_Info_Policy_Paper_March_2026.pdf",
    "https://iopscience.iop.org/article/10.1088/1748-0221/21/01/C01026",
]

LEAN_REQUIRED = [
    "ExternalStrengtheningSourceType",
    "ExternalStrengtheningTarget",
    "ExternalStrengtheningDataRecord",
    "usableAsProofInput : Bool",
    "usableAsProofInput := false",
    "externalStrengtheningDataNegativeControlRule",
    "externalStrengtheningDataLedger_notProofInput",
    STATUS,
]

BOUNDARY_REQUIRED = [
    "no theorem promotion",
    "no formal proof object supplied",
    "no certified mathematical dataset supplied",
    "no executable theorem verifier result supplied by the external source",
    "no UniversalFiberEntropyGap",
    "no Chronos-RR",
    "no H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
    "no gravity closure",
    "no cosmic censorship",
    "no hoop conjecture",
]

def main() -> None:
    for path in [LEAN, ART, DOC, ROOT_IMPORT]:
        assert path.exists(), path

    lean = LEAN.read_text()
    art_text = ART.read_text()
    doc = DOC.read_text()
    root_import = ROOT_IMPORT.read_text()
    data = json.loads(ART.read_text())

    assert data["status"] == STATUS
    assert data["usable_as_proof_input"] is False
    assert len(data["records"]) == 6

    for token in LEAN_REQUIRED:
        assert token in lean, token

    for url in URLS:
        assert url in art_text, url

    for token in BOUNDARY_REQUIRED:
        assert token in art_text, token
        assert token in doc, token

    assert "negative_control_rule" in data
    assert "formal proof object" in data["negative_control_rule"]
    assert "claim_mapping" in data
    assert "theorem truth" in data["claim_mapping"]["does_not_strengthen"]
    assert "verification discipline" in data["claim_mapping"]["strengthens"]

    for record in data["records"]:
        assert record["usable_as_proof_input"] is False
        assert 0 <= int(record["strength_score"]) <= 3
        assert record["source_url"].startswith("https://")
        assert record["what_it_strengthens"]

    assert "import Chronos.Frontier.ExternalStrengtheningDataLedger" in root_import

    print("external strengthening data ledger verified")

if __name__ == "__main__":
    main()
