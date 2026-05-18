#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'lean/Chronos/Frontier/RestrictedH41FGLToSelectedDomainH41FGL.lean'
DOC=ROOT/'docs/status/RESTRICTED_H41FGL_TO_SELECTED_DOMAIN_H41FGL_2026_05_18.md'
ART=ROOT/'artifacts/chronos/restricted_h41fgl_to_selected_domain_h41fgl_2026_05_18.json'
ROOT_IMPORT=ROOT/'lean/Chronos.lean'
for p in [LEAN,DOC,ART,ROOT_IMPORT]:
    if not p.exists():
        raise SystemExit(f'missing {p}')
lean=LEAN.read_text()
doc=DOC.read_text()
art_text=ART.read_text()
art=json.loads(art_text)
root_import=ROOT_IMPORT.read_text()
for tok in [
 'import Chronos.Frontier.RestrictedChronosRRToRestrictedH41FGL',
 'import Chronos.Frontier.SelectedDomainH41FGLFromChronosRR',
 'structure RestrictedH41FGLSelectedDomainEmbedding',
 'carrier_gap : RestrictedCarrierFiberEntropyGap rankRate fiberMass',
 'boundary_lock : UnrestrictedChronosRRFrontierOpen',
 'theorem selected_domain_h41fgl_from_restricted_h41_fgl',
 '_hRestricted : RestrictedH41FGL D',
 'SelectedDomainH41FGL rankRate fiberMass',
 'selected_domain_h41_fgl_from_chronos_rr',
 'selected_domain_chronos_rr_from_universal_gap',
 'selected_domain_universal_gap_from_restricted_carrier',
 'hEmbed.carrier_gap',
]:
    if tok not in lean:
        raise SystemExit(f'missing Lean token: {tok}')
for bad in ['admit','sorry','axiom','theorem unrestricted_chronos_rr ','theorem unrestricted_h41_fgl','def H41FGL','structure H41FGL']:
    if bad in lean:
        raise SystemExit(f'forbidden Lean token: {bad}')
if 'import Chronos.Frontier.RestrictedH41FGLToSelectedDomainH41FGL' not in root_import:
    raise SystemExit('missing root import')
if art.get('status')!='RESTRICTED_H41FGL_TO_SELECTED_DOMAIN_H41FGL_CLOSED':
    raise SystemExit('bad status')
if art.get('closed_theorem')!='selected_domain_h41fgl_from_restricted_h41_fgl':
    raise SystemExit('bad theorem')
combined='\n'.join([doc,art_text])
for tok in ['restricted-to-selected-domain bridge only','requires explicit selected-domain embedding data','does not construct the embedding','no unrestricted Chronos-RR','no unrestricted H4.1/FGL theorem-level closure','no Clay-problem closure']:
    if tok not in combined:
        raise SystemExit(f'missing boundary: {tok}')
for bad in ['unrestricted Chronos-RR is proved','unrestricted Chronos-RR closed','H4.1/FGL is solved','H4.1/FGL solved','unrestricted H4.1/FGL is proved','embedding is constructed','P vs NP is solved','Clay problem is solved']:
    if bad in combined or bad in lean:
        raise SystemExit(f'forbidden overclaim: {bad}')
print('Restricted H4.1/FGL to selected-domain H4.1/FGL verified.')
