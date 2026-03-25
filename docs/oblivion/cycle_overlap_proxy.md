Cycle Overlap Proxy

Implements a computable lower bound on cycle-overlap rank.

Definition:
local_cycle_rank(G,R) = rank of cycles contained in radius-R balls.

Properties validated:
- trees → rank 0
- cycles → rank ≥1 when R exceeds half-cycle length
- expanders → rank growth

Purpose:
empirical instrumentation for Oblivion Atom frontier.
