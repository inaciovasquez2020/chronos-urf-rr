# Ball-volume acyclicity status — 2026-04-27

Status: Conditional at Lean-theorem level; executable finite certificate verified.

The old local claim

\[
\operatorname{cycle\_length}(C)\le 2R
\]

for a cycle contained in a radius-\(R\) ball is not admissible for general graphs.

Correct replacement:

\[
\operatorname{girth}(G)>|B_G(v,R)|
\Longrightarrow
G[B_G(v,R)]\text{ is acyclic}.
\]

Bounded-degree corollary:

\[
|B_G(v,R)|
\le
1+\Delta\sum_{j=0}^{R-1}(\Delta-1)^j.
\]

Therefore:

\[
\operatorname{girth}(G)>
1+\Delta\sum_{j=0}^{R-1}(\Delta-1)^j
\Longrightarrow
G[B_G(v,R)]\text{ is acyclic}.
\]

Degree cases:
- \(\Delta=0\): \(|B_G(v,R)|\le 1\).
- \(\Delta=1\): \(|B_G(v,R)|\le 2\) for \(R\ge1\).
- \(\Delta=2\): \(|B_G(v,R)|\le 1+2R\).
- \(\Delta>2\): \(|B_G(v,R)|\le 1+\Delta((\Delta-1)^R-1)/(\Delta-2)\).

Current Lean-side obligation:
quarantine `cycle_length_le_twoR_of_subgraph_ball_quarantined`.

Mathematical correction:
`cycle_length_le_twoR_of_subgraph_ball_quarantined` is false for general graphs.

Executable replacement already verified:
`tools/verify_ball_volume_acyclicity.py`

Replacement theorem:
`girth(G) > |B_G(v,R)| -> Acyclic(G[B_G(v,R)])`

Bounded-degree corollary:
`girth(G) > 1 + Δ * sum_{j=0}^{R-1} (Δ-1)^j -> Acyclic(G[B_G(v,R)])`

Status:
The old `2R` bound must remain quarantined.
It must not be used as a theorem-level dependency.


## Dependent theorem quarantine

The following theorem currently depends on the quarantined `2R` cycle-length bound:

- `lean/Oblivion/CycloneSignedLift.lean`:
  `girth_gt_twoR_implies_ball_acyclic_quarantined`

Reason:
the proof calls `ball_cycle_length_bound_quarantined`, which calls the quarantined axiom
`cycle_length_le_twoR_of_subgraph_ball_quarantined`.

Status:
`girth_gt_twoR_implies_ball_acyclic_quarantined` is Conditional/Quarantined until rewritten using the bounded-volume girth-radius acyclicity theorem.

Replacement target:

`girth(G) > |B_G(v,R)| -> Acyclic(ball G v R)`

or, under bounded degree:

`girth(G) > 1 + Δ * sum_{j=0}^{R-1} (Δ-1)^j -> Acyclic(ball G v R)`

