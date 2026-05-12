# Chronos Semantic Rank Defect Controls Entropy Defect Frontier — 2026-05-12

Status: FRONTIER_OPEN / WEAKEST_MISSING_QUANTITATIVE_LEMMA.

## Proved repository-native surface

The Lean file

`Chronos/Frontier/SemanticRankDefectControlsEntropyDefectFrontier.lean`

formalizes non-Prop rank-entropy data carrying:

- `fiberSize : ℕ`
- `imageSize : ℕ`
- `rankDefect : ℚ`
- `entropyDefect : ℚ`

and proves the conditional bridge:

```lean
theorem conditional_rank_rate_gap_to_fiber_entropy_gap_from_semantic_control
    (P : NonPropRankEntropyData → Prop)
    (hGap : GenuineRankRateGapOn P)
    (hControl : SemanticRankDefectControlsEntropyDefectOn P) :
    GenuineFiberEntropyGapOn P
Weakest missing theorem-level input
def SemanticRankDefectControlsEntropyDefectOn
    (P : NonPropRankEntropyData → Prop) : Prop :=
  ∃ C : ℚ,
    0 < C ∧
    ∀ d : NonPropRankEntropyData,
      P d →
      d.rankDefect ≤ C * d.entropyDefect
Equivalently:
def WeakestMissingTheoremLevelInput
    (P : NonPropRankEntropyData → Prop) : Prop :=
  SemanticRankDefectControlsEntropyDefectOn P
Boundary
This artifact proves only the conditional quantitative bridge from rank-rate gap to fiber-entropy gap assuming semantic rank-defect control by entropy defect.
It does not prove RankRateGap, SemanticRankRateToFiberEntropySoundness, CountingFiberSeparation, FiberMassBalance, UniversalFiberEntropyGap, Chronos-RR, H4.1/FGL, P vs NP, or any Clay-problem closure.
