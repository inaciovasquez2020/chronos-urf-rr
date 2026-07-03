from pathlib import Path

path = Path("lean/Chronos/Frontier/GaussianKKReductionSurface.lean")
text = path.read_text()

required = [
"def kkDegeneracy",
"theorem kkDegeneracy_zero",
"theorem kkDegeneracy_pos",
"structure GaussianKKReductionSurface",
"structure GaussianKKPartitionSurface",
"structure GaussianKKFiniteEntropyIdentity",
"def complexModeNoDoubleCountBoundary",
"theorem complexModeNoDoubleCountBoundary_holds",
]

missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"MISSING_OBJECT := {missing}")

print("GAUSSIAN_KK_REDUCTION_SURFACE_OK")
