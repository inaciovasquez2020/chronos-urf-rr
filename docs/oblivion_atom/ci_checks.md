# Oblivion Atom — CI Checks

This document lists minimal repository checks ensuring
the Oblivion Atom module remains reproducible.

## File Presence Checks

Required scripts

toolkit/oblivion/scripts/geometry_signature_scan.py  
toolkit/oblivion/scripts/graph_geometry_plot.py  
toolkit/oblivion/scripts/FO_k_type_collision_detector.py  

Required results

toolkit/oblivion/results/geometry_rr_R12.png  
toolkit/oblivion/results/geometry_twolift_R12.png  

Required documentation

docs/oblivion_atom/README.md  
docs/oblivion_atom/theory_overview.md  
docs/oblivion_atom/formal_definitions.md  
docs/oblivion_atom/roadmap.md  

## Purpose

Ensure that

geometry diagnostics  
cycle diagnostics  
logical diagnostics  

remain present and reproducible.

## Suggested CI Test

test -f toolkit/oblivion/scripts/geometry_signature_scan.py  
test -f toolkit/oblivion/scripts/graph_geometry_plot.py  
test -f docs/oblivion_atom/theory_overview.md  

