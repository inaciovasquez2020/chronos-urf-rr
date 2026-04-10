from pathlib import Path

def test_component_indicator_basis_tokens():
    s = Path("URF/Lean/Graph/ComponentIndicatorBasis.lean").read_text()
    required = [
        "structure ComponentIndicator",
        "structure ComponentFamily",
        "theorem component_indicators_in_kernel",
        "theorem component_indicators_span_kernel",
        "theorem component_indicators_independent",
    ]
    for token in required:
        assert token in s, f"missing token: {token}"
