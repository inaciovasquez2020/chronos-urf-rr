from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGET = ROOT / "lean/Chronos/Frontier/R2GeneralCrossRootIncidenceTarget.lean"
INPUT = ROOT / "lean/Chronos/Frontier/R2GeneralCrossRootIncidenceInputSurface.lean"
CERTIFICATE = ROOT / "lean/Chronos/Frontier/R2PromotionProofObstructionCertificate.lean"
SUFFICIENCY = ROOT / "lean/Chronos/Frontier/R2DiameterFillingCompatibilitySufficiency.lean"
FRONTIER = ROOT / "lean/Chronos/Frontier.lean"


def test_general_interface_records_geometric_incidence_data():
    text = TARGET.read_text()

    for token in [
        "structure R2GeneralCrossRootIncidenceSystem where",
        "boundaryMatches : Chain → Prop",
        "contains : Face → Chain → Prop",
        "adjacent : Face → Face → Prop",
        "touchesRoot : Face → Root → Prop",
        "def CrossRootWitness",
        "def NonvacuousTarget",
    ]:
        assert token in text

    assert "(∃ chain : S.Chain, S.boundaryMatches chain) ∧" in text
    assert "leftRoot ≠ rightRoot" in text


def test_checked_packet_proves_nonvacuous_general_target():
    text = TARGET.read_text()

    for token in [
        "def r2IncidenceGeneralCrossRootSystem",
        "theorem r2_incidence_boundary_match_eq_all_faces",
        "theorem r2_incidence_all_faces_has_cross_root_witness",
        "theorem r2_incidence_general_cross_root_target",
    ]:
        assert token in text

    assert "native_decide" in text
    assert "sorry" not in text
    assert "admit" not in text
    assert "axiom" not in text
    assert "opaque" not in text


def test_general_target_constructs_real_obstruction_input_surface():
    text = INPUT.read_text()

    for token in [
        "def obstructionInputSurface",
        "obstruction := by",
        "theorem obstructionInputSurface_nonempty",
        "def r2IncidenceGeneralCrossRootInputSurface",
        "theorem general_cross_root_incidence_to_r2_native_obstruction_target",
        "theorem r2_incidence_packet_reaches_native_obstruction_target",
    ]:
        assert token in text


def test_elimination_certificate_is_universal_and_not_placeholder_closed():
    text = CERTIFICATE.read_text()

    assert "def R2PromotionProofObstructionEliminationCertificate : Prop :=" in text
    assert "∀ S : R2GeneralCrossRootIncidenceSystem" in text
    assert "S.NonvacuousTarget →" in text
    assert "R2PromotionProofTarget" in text

    assert (
        "theorem r2_promotion_proof_obstruction_elimination_certificate"
        not in text
    )
    assert (
        "def R2PromotionProofObstructionEliminationCertificate : Prop :=\n  False"
        not in text
    )
    assert (
        "def R2PromotionProofObstructionEliminationCertificate : Prop :=\n  True"
        not in text
    )


def test_r2_frontier_remains_honestly_open():
    text = SUFFICIENCY.read_text()

    assert "def R2DiameterFillingCompatibilitySufficiencyFrontierOpen" in text
    assert "R2DiameterFillingCompatibilitySufficiencyFrontierClosed" not in text
    assert (
        "theorem r2_cross_root_face_incidence_to_promotion_obstruction_elimination"
        not in text
    )
    assert (
        "theorem r2_diameter_filling_compatibility_sufficiency_frontier_closed"
        not in text
    )


def test_new_modules_are_registered_in_frontier():
    text = FRONTIER.read_text()

    assert "import Chronos.Frontier.R2GeneralCrossRootIncidenceTarget" in text
    assert "import Chronos.Frontier.R2GeneralCrossRootIncidenceInputSurface" in text
