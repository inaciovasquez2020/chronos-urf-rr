# Cycle–Rank Rigidity Experimental Results

## Experiment

Batch experiments measuring the rank of the cycle–edge incidence matrix
in bounded-degree random graphs.

Script:

toolkit/oblivion/scripts/cycle_rank_batch.py

---

## Expected Result

For cycle count \(m\) and incidence matrix \(B\),

\[
\operatorname{rank}(B) = \Omega(m)
\]

so the ratio

\[
\frac{\operatorname{rank}(B)}{m}
\]

should converge to a positive constant.

---

## Data File

Results stored in:

toolkit/oblivion/results/cycle_rank_batch.json

---

## Interpretation

Empirical confirmation of the structural lemma:

CycleOverlap → CycleRankRigidity

which forms the first deterministic step in the Oblivion Atom chain.

\[
\text{COR}
\Rightarrow
\text{CycleRankRigidity}
\Rightarrow
\text{FO}^k\text{ Diversity}
\Rightarrow
\text{EntropyDepth}.
\]

