from pathlib import Path

def test_bridge_doc():
    p = Path("proofs/FOK_BRIDGE.md")
    assert p.exists()
    s = p.read_text()
    assert "EF game" in s
    assert "Type_{k,R}" in s
