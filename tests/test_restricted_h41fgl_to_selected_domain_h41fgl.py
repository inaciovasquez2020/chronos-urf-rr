from pathlib import Path
import json, subprocess
ROOT=Path(__file__).resolve().parents[1]
def test_verifier_passes():
    subprocess.run(['python3','tools/verify_restricted_h41fgl_to_selected_domain_h41fgl.py'],cwd=ROOT,check=True)
def test_artifact_status():
    art=json.loads((ROOT/'artifacts/chronos/restricted_h41fgl_to_selected_domain_h41fgl_2026_05_18.json').read_text())
    assert art['status']=='RESTRICTED_H41FGL_TO_SELECTED_DOMAIN_H41FGL_CLOSED'
    assert art['closed_theorem']=='selected_domain_h41fgl_from_restricted_h41_fgl'
    assert art['embedding_object']=='RestrictedH41FGLSelectedDomainEmbedding'
def test_lean_surface_and_boundaries():
    lean=(ROOT/'lean/Chronos/Frontier/RestrictedH41FGLToSelectedDomainH41FGL.lean').read_text()
    assert 'structure RestrictedH41FGLSelectedDomainEmbedding' in lean
    assert "carrier_gap : RestrictedCarrierFiberEntropyGap rankRate fiberMass" in lean
    assert 'theorem selected_domain_h41fgl_from_restricted_h41_fgl' in lean
    assert 'SelectedDomainH41FGL rankRate fiberMass' in lean
    assert 'selected_domain_universal_gap_from_restricted_carrier' in lean
    assert 'admit' not in lean
    assert 'sorry' not in lean
    assert 'axiom' not in lean
    assert 'theorem unrestricted_chronos_rr ' not in lean
    assert 'theorem unrestricted_h41_fgl' not in lean
