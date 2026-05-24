#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/BlackHoleObservationalMotivationRegistry.lean"
ART = ROOT / "artifacts/chronos/black_hole_observational_motivation_registry_2026_05_24.json"
DOC = ROOT / "docs/status/BLACK_HOLE_OBSERVATIONAL_MOTIVATION_REGISTRY_2026_05_24.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

REQUIRED = [
    "OBSERVATIONAL_MOTIVATION_REGISTRY_ONLY_NO_THEOREM_PROMOTION",
    "NASA_NEOWISE_M31_2014_DS1_FAILED_SUPERNOVA_CONTEXT",
    "CHANDRA_SMBH_GROWTH_SLOWDOWN_CONTEXT",
    "J1007_EPISODIC_AGN_JET_CONTEXT",
    "ABELL_402_BCG_ULTRAMASSIVE_PAIR_CONTEXT",
    "AAS_SMBH_BLUE_NOTES_2026_VENUE_CONTEXT",
    "no analytic Einstein-matter bootstrap package",
    "no concrete analytic estimate proof",
    "no restricted collapse-gate trigger",
    "no unrestricted black-hole formation theorem",
    "no cosmic censorship",
    "no hoop conjecture",
    "no gravity closure",
    "no Chronos-RR",
    "no H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
]

LEAN_REQUIRED = [
    "BlackHoleObservationClass",
    "BlackHoleObservationalMotivation",
    "usableAsProofInput : Bool",
    "usableAsProofInput := false",
    "blackHoleObservationalMotivationRegistry_notProofInput",
    "OBSERVATIONAL_MOTIVATION_REGISTRY_ONLY_NO_THEOREM_PROMOTION",
]

URLS = [
    "https://science.nasa.gov/blogs/science-news/2026/02/12/archival-data-from-nasas-neowise-tracks-star-turning-into-black-hole/",
    "https://chandra.harvard.edu/photo/2026/bhgrowth/",
    "https://www.space.com/astronomy/black-holes/reborn-black-hole-seen-erupting-across-1-million-light-years-of-space-like-a-cosmic-volcano",
    "https://www.sciencenews.org/article/largest-pair-black-holes-collision",
    "https://aas.org/events/2025-09/supermassive-black-holes-and-blue-notes-international-conference",
]

def main() -> None:
    for p in [LEAN, ART, DOC, ROOT_IMPORT]:
        assert p.exists(), p

    lean = LEAN.read_text()
    art_text = ART.read_text()
    doc = DOC.read_text()
    root_import = ROOT_IMPORT.read_text()

    data = json.loads(ART.read_text())

    assert data["status"] == "OBSERVATIONAL_MOTIVATION_REGISTRY_ONLY_NO_THEOREM_PROMOTION"
    assert data["usable_as_proof_input"] is False
    assert len(data["records"]) == 5

    for token in LEAN_REQUIRED:
        assert token in lean, token

    for token in REQUIRED:
        assert token in art_text or token in doc, token

    for url in URLS:
        assert url in art_text, url

    assert "import Chronos.Frontier.BlackHoleObservationalMotivationRegistry" in root_import

    for record in data["records"]:
        assert "source_url" in record
        assert "observation_class" in record
        assert "gravity_motivation" in record

    print("black-hole observational motivation registry verified")

if __name__ == "__main__":
    main()
