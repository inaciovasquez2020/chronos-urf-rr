from pathlib import Path

checks = {
    "lean/Chronos/Frontier.lean": [
        "import Chronos.Frontier.LongChordExclusionConcreteInputSurface",
        "import Chronos.Frontier.DiameterSeparationFillingConcreteInputSurface",
        "import Chronos.Frontier.UniformLocalTypeCapacityConcreteInputSurface",
        "import Chronos.Frontier.ConcreteR1R2R3InputSurfacesReceipt",
        "import Chronos.Frontier.NonFactorisationConcreteInputSurface",
        "import Chronos.Frontier.ConcreteR1R2R3NonFactorisationInputSurfacesReceipt",
    ],
    "lean/Chronos/Frontier/LongChordExclusionConcreteInputSurface.lean": [
        "def LongChordExclusionConcreteInputSurface",
        "LongChordNativeObject",
        "LongChordWitness",
        "NativeLongChordCoherence",
        "long_chord_witness_contradiction",
    ],
    "lean/Chronos/Frontier/DiameterSeparationFillingConcreteInputSurface.lean": [
        "def DiameterSeparationFillingConcreteInputSurface",
        "DiameterFillingNativeObject",
        "DiameterFillingCompatibility",
        "monotone_separation_lower_bound",
    ],
    "lean/Chronos/Frontier/UniformLocalTypeCapacityConcreteInputSurface.lean": [
        "def UniformLocalTypeCapacityConcreteInputSurface",
        "LocalTypeCapacityNativeObject",
        "ExplicitLocalTypeCapacityC",
        "Nat.zero_le",
    ],
    "lean/Chronos/Frontier/NonFactorisationConcreteInputSurface.lean": [
        "def NonFactorisationConcreteInputSurface",
        "RepositoryNativeNonFactorisationPromotionAllowed concreteNativeBindingSpec",
        "concrete_native_nonfactorisation_promotion_allowed",
    ],
    "lean/Chronos/Frontier/ConcreteR1R2R3NonFactorisationInputSurfacesReceipt.lean": [
        "def ConcreteR1R2R3NonFactorisationInputSurfacesReceipt",
        "theorem concrete_r1_r2_r3_nonfactorisation_input_surfaces_receipt",
        "ConcreteR1R2R3InputSurfacesReceipt",
        "NonFactorisationProofTarget",
        "NonFactorisationConcreteInputSurface",
    ],
}

for file_name, required in checks.items():
    path = Path(file_name)
    if not path.exists():
        raise SystemExit(f"MISSING_OBJECT := {file_name}")
    text = path.read_text()
    for item in required:
        if item not in text:
            raise SystemExit(f"MISSING_OBJECT := {file_name} :: {item}")

forbidden = [
    "unrestricted_R1_R2_R3_geometric_closure",
    "proves_unrestricted_r1_r2_r3",
    "global_nonfactorisation_theorem_closed",
]

repo_text = "\n".join(
    path.read_text()
    for path in Path("lean/Chronos/Frontier").glob("*.lean")
)

for item in forbidden:
    if item in repo_text:
        raise SystemExit(f"FORBIDDEN_CLAIM := {item}")

print("CONCRETE_INPUT_SURFACES_RECEIPT_OK")
