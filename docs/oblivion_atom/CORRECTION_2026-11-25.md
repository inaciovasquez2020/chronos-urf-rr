# Cycle-local rigidity correction — 2026-11-25

Status: REFUTED AS WRITTEN. Base: `657042fb9d1acdb6ee996ed60588d9e9785671dc`.

For even m >= 6, let G = C_m square C_m. Coordinate translations act transitively, so all rooted radius-r balls are isomorphic for any r and all FO^k local types agree. Thus T_r(G)=1. The graph is connected, simple, and degree four, with m^2 vertices. Select squares with lower-left coordinates (2i,2j), 0 <= i,j < m/2. Their boundaries have disjoint supports and each lies in an induced radius-two ball. Hence C_2(G) >= m^2/4 over F_2. This refutes the asserted constant cycle-packing bound and type-divergence implication for R=2 and alpha=1/4. Isomorphic abstract local cycle spaces do not imply identical embedded subspaces.

For the packing conjecture, a disjoint union of N triangles is degree two and vertex-transitive. For every R >= 1 it has N pairwise disjoint radius-R balls containing cycles, while its type diversity is one. If R=0 is permitted the antecedent with positive packing threshold is vacuous, not a nontrivial rigidity result. A definable separator requires both kinds of patches actually occur.

## Affected historical sources
- docs/oblivion_atom/theory/cycle_local_rigidity_main.tex
- docs/oblivion_atom/theory/cycle_local_rigidity_master.tex
- manuscripts/cycle_local_rigidity/main.tex
- docs/oblivion_atom/theory/cycle_packing_bound.tex
- toolkit/oblivion/proofs/cycle_packing_to_type_divergence.tex

These sources are retained with conspicuous notices. No unrelated Chronos theorem, Lean declaration, or computation is reclassified solely by association. Further downstream dependencies require individual auditing. This is a paper counterexample, not a Lean verification receipt.
