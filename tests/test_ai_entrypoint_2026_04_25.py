from pathlib import Path


AGENTS = Path("AGENTS.md")
ENTRY = Path("docs/status/AI_ENTRYPOINT_2026_04_25.md")


def test_agents_file_exists_and_locks_claim_boundary():
    text = AGENTS.read_text(encoding="utf-8")

    assert "AI-NAVIGATION ENTRYPOINT" in text
    assert "Do not infer theorem completion from README language alone." in text
    assert "must not say" in text
    assert "The full theorem layer is complete." in text
    assert "External/general theorem-layer obligations" in text


def test_ai_entrypoint_exists_and_is_machine_readable():
    text = ENTRY.read_text(encoding="utf-8")

    assert "CANONICAL AI ENTRYPOINT" in text
    assert '"ai_entrypoint": true' in text
    assert '"full_theorem_layer_complete": false' in text
    assert '"claim_boundary_required": true' in text
