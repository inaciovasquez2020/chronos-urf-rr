# Adaptive radius structural auditor

Status: COMPUTATION_PASS

Release base: 18d6ac45527d6604a83c931640e8ba5b56c1d6d4

Mathematical foundation:
URF-Core radiusCycles_eq_boundedSupportCycleSpace

Mathematical revision:
fe6be4410fa386fc157d3d1f7711e3f7a0fc4999

Command:
rat radius-audit graph.json --max-radius 8

Validation:
- 13,010 earlier exact comparisons across two reference methods.
- Combined toolkit regression recorded in release-regression.txt.
- Native real-graph replay passed.
- Seven existing benchmark files preserved.

The auditor operates over GF(2), with directed cycle
analysis performed separately.

Structural coverage is not factual accuracy,
semantic validity or proof of dependency completeness.

The real-graph receipt concerns the previously
extracted 20-module graph, not the expanded toolkit.

AI reasoning improvement, independent security
review and scholarly novelty remain open.

The auditor authorizes no repository mutation.
