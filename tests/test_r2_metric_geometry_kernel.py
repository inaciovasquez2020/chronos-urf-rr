from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "lean/Chronos/Frontier/R2Geometry"
FRONTIER = ROOT / "lean/Chronos/Frontier.lean"

FILES = {
    "geometry": BASE / "R2MetricFillingGeometry.lean",
    "chain_complex": BASE / "R2ChainComplexGeometry.lean",
    "support": BASE / "R2BoundarySupportMonotonicity.lean",
    "kernel": BASE / "R2MetricDiameterObstructionKernel.lean",
    "closed_ball": BASE / "R2ClosedBallLocalization.lean",
    "overlap": BASE / "R2OverlappingFaceMetricBound.lean",
    "path": BASE / "R2FacePathMetricBound.lean",
    "localization": BASE / "R2AdmissibleSupportLocalization.lean",
}

FORBIDDEN_CODE_PATTERNS = (
    r"\bnative_decide\b",
    r"\bsorry\b",
    r"\badmit\b",
    r"\baxiom\b",
    r"\bopaque\b",
)


def read(name: str) -> str:
    path = FILES[name]
    assert path.is_file(), path
    return path.read_text()


def strip_lean_comments(text: str) -> str:
    output: list[str] = []
    index = 0
    block_depth = 0
    in_string = False

    while index < len(text):
        if block_depth > 0:
            if text.startswith("/-", index):
                block_depth += 1
                index += 2
            elif text.startswith("-/", index):
                block_depth -= 1
                index += 2
            else:
                if text[index] == "\n":
                    output.append("\n")
                index += 1
            continue

        if in_string:
            output.append(text[index])

            if text[index] == "\\" and index + 1 < len(text):
                output.append(text[index + 1])
                index += 2
                continue

            if text[index] == '"':
                in_string = False

            index += 1
            continue

        if text.startswith("/-", index):
            block_depth = 1
            index += 2
            continue

        if text.startswith("--", index):
            newline = text.find("\n", index)

            if newline == -1:
                break

            output.append("\n")
            index = newline + 1
            continue

        if text[index] == '"':
            in_string = True

        output.append(text[index])
        index += 1

    assert block_depth == 0, "unterminated Lean block comment"
    assert not in_string, "unterminated Lean string"

    return "".join(output)


def test_metric_geometry_defines_actual_filling_objects() -> None:
    text = read("geometry")

    required = (
        "structure R2FillingGeometry where",
        "Point : Type",
        "Face1 : Type",
        "Face2 : Type",
        "pointMetric : MetricSpace Point",
        "face1Support : Face1 → Set Point",
        "face2Support : Face2 → Set Point",
        "boundary2 : (Face2 →₀ F2) → Face1 →₀ F2",
        "def supp1",
        "def supp2",
        "def Fillable",
        "∃ F, G.boundary2 F = c ∧ Adm F",
        "def Separated",
        "D < dist xLeft xRight",
    )

    for token in required:
        assert token in text, token


def test_chain_complex_refines_actual_filling_geometry() -> None:
    text = read("chain_complex")

    required = (
        "structure R2ChainComplexGeometry where",
        "geometry : R2FillingGeometry",
        "Face0 : Type",
        "boundary1 :",
        "boundary2_zero",
        "boundary2_add",
        "boundary1_zero",
        "boundary1_add",
        "boundary_squared_zero",
        "def IsCycle",
        "theorem boundary2_isCycle",
        "theorem fillable_isCycle",
    )

    for token in required:
        assert token in text, token


def test_boundary_support_monotonicity_is_derived() -> None:
    text = read("support")

    required = (
        "theorem supp1_boundary_subset_supp2",
        "G.supp1 (G.boundary2 F) ⊆ G.supp2 F",
        "G.boundary_face_support F edge hEdgeBoundary",
    )

    for token in required:
        assert token in text, token


def test_metric_obstruction_kernel_uses_independent_hypotheses() -> None:
    text = read("kernel")

    required = (
        "def AdmissibleLocalized",
        "theorem diameter_separation_filling_obstruction",
        "hLoc : AdmissibleLocalized G Adm D",
        "hSep : G.Separated c D",
        "¬ G.Fillable Adm c",
        "supp1_boundary_subset_supp2 G F",
        "not_le.mpr hSeparated",
    )

    for token in required:
        assert token in text, token


def test_closed_ball_localization_is_derived() -> None:
    text = read("closed_ball")

    required = (
        "def AdmissibleContainedInClosedBall",
        "G.supp2 F ⊆ Metric.closedBall center R",
        "theorem admissibleLocalized_of_closedBall",
        "AdmissibleLocalized G Adm (2 * R)",
        "theorem diameter_separation_filling_obstruction_of_closedBall",
    )

    for token in required:
        assert token in text, token


def test_overlapping_face_metric_step_is_derived() -> None:
    text = read("overlap")

    required = (
        "def FaceDiameterBound",
        "def FacesOverlap",
        "theorem overlapping_faces_metric_bound",
        "dist x y ≤ 2 * ε",
        "dist_triangle x middle y",
    )

    for token in required:
        assert token in text, token


def test_face_path_metric_bound_is_general() -> None:
    text = read("path")

    required = (
        "inductive FacePath",
        "def FacePathMetricBound",
        "theorem face_path_metric_bound",
        "dist x y ≤ FacePathMetricBound ε length",
    )

    for token in required:
        assert token in text, token


def test_dual_path_bound_derives_global_localization() -> None:
    text = read("localization")

    required = (
        "def AdmissibleDualPathBound",
        "length ≤ N",
        "FacePath G first last length",
        "theorem admissibleLocalized_of_dualPathBound",
        "AdmissibleLocalized G Adm (FacePathMetricBound ε N)",
        "theorem diameter_separation_filling_obstruction_of_dualPathBound",
    )

    for token in required:
        assert token in text, token


def test_no_proof_escape_hatches_or_finite_enumeration() -> None:
    for name, path in FILES.items():
        code = strip_lean_comments(path.read_text())

        for pattern in FORBIDDEN_CODE_PATTERNS:
            assert re.search(pattern, code) is None, (
                f"{name}: forbidden code pattern {pattern!r}"
            )


def test_all_r2_geometry_modules_are_registered() -> None:
    assert FRONTIER.is_file(), FRONTIER
    text = FRONTIER.read_text()

    required_imports = (
        "import Chronos.Frontier.R2Geometry.R2MetricFillingGeometry",
        "import Chronos.Frontier.R2Geometry.R2ChainComplexGeometry",
        "import Chronos.Frontier.R2Geometry.R2BoundarySupportMonotonicity",
        "import Chronos.Frontier.R2Geometry.R2MetricDiameterObstructionKernel",
        "import Chronos.Frontier.R2Geometry.R2ClosedBallLocalization",
        "import Chronos.Frontier.R2Geometry.R2OverlappingFaceMetricBound",
        "import Chronos.Frontier.R2Geometry.R2FacePathMetricBound",
        "import Chronos.Frontier.R2Geometry.R2AdmissibleSupportLocalization",
    )

    for token in required_imports:
        assert token in text, token
