namespace Chronos
namespace Frontier
namespace SemanticRankDefectControlsEntropyDefectFrontier

structure NonPropRankEntropyData where
  fiberSize : ℕ
  imageSize : ℕ
  rankDefect : Rat
  entropyDefect : Rat
  fiber_nonzero : 0 < fiberSize
  image_nonzero : 0 < imageSize
  rank_defect_nonneg : 0 ≤ rankDefect
  entropy_defect_nonneg : 0 ≤ entropyDefect

def GenuineRankRateGapOn (P : NonPropRankEntropyData → Prop) : Prop :=
  ∃ δ : Rat,
    0 < δ ∧
    ∀ d : NonPropRankEntropyData,
      P d →
      δ ≤ d.rankDefect

def GenuineFiberEntropyGapOn (P : NonPropRankEntropyData → Prop) : Prop :=
  ∃ ε : Rat,
    0 < ε ∧
    ∀ d : NonPropRankEntropyData,
      P d →
      ε ≤ d.entropyDefect

def RankEntropySoundnessOn (P : NonPropRankEntropyData → Prop) : Prop :=
  ∃ C : Rat,
    0 < C ∧
    ∀ d : NonPropRankEntropyData,
      P d →
      d.rankDefect ≤ C * d.entropyDefect

def SemanticRankDefectControlsEntropyDefectOn
    (P : NonPropRankEntropyData → Prop) : Prop :=
  RankEntropySoundnessOn P

def WeakestMissingTheoremLevelInput
    (P : NonPropRankEntropyData → Prop) : Prop :=
  SemanticRankDefectControlsEntropyDefectOn P

theorem semantic_rank_defect_controls_entropy_defect_is_soundness
    (P : NonPropRankEntropyData → Prop) :
    SemanticRankDefectControlsEntropyDefectOn P ↔
      RankEntropySoundnessOn P := by
  rfl

theorem weakest_missing_theorem_level_input_is_semantic_control
    (P : NonPropRankEntropyData → Prop) :
    WeakestMissingTheoremLevelInput P ↔
      SemanticRankDefectControlsEntropyDefectOn P := by
  rfl

def DirectRankEntropyTransferOn (P : NonPropRankEntropyData → Prop) : Prop :=
  GenuineRankRateGapOn P → GenuineFiberEntropyGapOn P

def ConditionalBridgeClosedOn (P : NonPropRankEntropyData → Prop) : Prop :=
  SemanticRankDefectControlsEntropyDefectOn P →
    DirectRankEntropyTransferOn P

def WeakestExecutableClosureInput
    (P : NonPropRankEntropyData → Prop) : Prop :=
  DirectRankEntropyTransferOn P

theorem weakest_executable_closure_input_is_direct_transfer
    (P : NonPropRankEntropyData → Prop) :
    WeakestExecutableClosureInput P ↔
      DirectRankEntropyTransferOn P := by
  rfl

theorem conditional_rank_rate_gap_to_fiber_entropy_gap_from_direct_transfer
    (P : NonPropRankEntropyData → Prop)
    (hGap : GenuineRankRateGapOn P)
    (hTransfer : DirectRankEntropyTransferOn P) :
    GenuineFiberEntropyGapOn P :=
  hTransfer hGap

end SemanticRankDefectControlsEntropyDefectFrontier
end Frontier
end Chronos
