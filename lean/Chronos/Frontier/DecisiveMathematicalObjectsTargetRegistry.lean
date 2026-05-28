import Mathlib

namespace Chronos.Frontier

inductive DecisiveMathematicalObjectKind where
  | rankEntropyGapLemma
  | finiteToUniformUpgradeLemma
  | lowerBoundInequality
  | compactnessTheorem
  | realNumericalPredictionVectorRun
deriving DecidableEq, Repr

structure DecisiveMathematicalObjectTarget where
  kind : DecisiveMathematicalObjectKind
  canonicalName : String
  weakestSufficientObject : String
  status : String
  doesNotProve : List String
deriving Repr

def RankEntropyGapLemmaTarget : DecisiveMathematicalObjectTarget :=
  { kind := DecisiveMathematicalObjectKind.rankEntropyGapLemma,
    canonicalName := "RankEntropyGapLemma",
    weakestSufficientObject :=
      "a theorem converting registered rank/fiber growth into a uniform positive entropy gap",
    status := "OPEN_TARGET_NOT_PROVED",
    doesNotProve :=
      [ "unrestricted UniversalFiberEntropyGap",
        "unrestricted Chronos-RR",
        "unrestricted H4.1/FGL",
        "P vs NP",
        "any Clay problem" ] }

def FiniteToUniformUpgradeLemmaTarget : DecisiveMathematicalObjectTarget :=
  { kind := DecisiveMathematicalObjectKind.finiteToUniformUpgradeLemma,
    canonicalName := "FiniteToUniformUpgradeLemma",
    weakestSufficientObject :=
      "a compactness, monotonicity, or coercivity theorem upgrading finite verified witnesses to a uniform family-level lower bound",
    status := "OPEN_TARGET_NOT_PROVED",
    doesNotProve :=
      [ "unrestricted finite-support lift",
        "unrestricted UniversalFiberEntropyGap",
        "unrestricted Chronos-RR",
        "P vs NP",
        "any Clay problem" ] }

def LowerBoundInequalityTarget : DecisiveMathematicalObjectTarget :=
  { kind := DecisiveMathematicalObjectKind.lowerBoundInequality,
    canonicalName := "LowerBoundInequality",
    weakestSufficientObject :=
      "a nonzero quantitative lower bound showing that nontrivial registered structure cannot collapse to zero cost",
    status := "OPEN_TARGET_NOT_PROVED",
    doesNotProve :=
      [ "rank-to-entropy bridge",
        "unrestricted UniversalFiberEntropyGap",
        "unrestricted Chronos-RR",
        "P vs NP",
        "any Clay problem" ] }

def CompactnessTheoremTarget : DecisiveMathematicalObjectTarget :=
  { kind := DecisiveMathematicalObjectKind.compactnessTheorem,
    canonicalName := "CompactnessTheorem",
    weakestSufficientObject :=
      "a compactness theorem preserving positive quantitative gap data along admissible limiting families",
    status := "OPEN_TARGET_NOT_PROVED",
    doesNotProve :=
      [ "finite-to-uniform upgrade",
        "unrestricted gravity closure",
        "Cosmic Censorship",
        "Hoop Conjecture",
        "any Clay problem" ] }

def RealNumericalPredictionVectorRunTarget : DecisiveMathematicalObjectTarget :=
  { kind := DecisiveMathematicalObjectKind.realNumericalPredictionVectorRun,
    canonicalName := "RealNumericalPredictionVectorRun",
    weakestSufficientObject :=
      "a hash-locked finite-output numerical prediction-vector run from an executable DFM-MKC solver or trusted external solver",
    status := "OPEN_TARGET_NOT_EXECUTED",
    doesNotProve :=
      [ "DFM-MKC empirical validation",
        "Lambda-CDM failure",
        "dark matter replacement",
        "dark matter is liquid",
        "dark matter is solid",
        "dark matter is a phase",
        "any Clay problem" ] }

def decisiveMathematicalObjectTargets : List DecisiveMathematicalObjectTarget :=
  [ RankEntropyGapLemmaTarget,
    FiniteToUniformUpgradeLemmaTarget,
    LowerBoundInequalityTarget,
    CompactnessTheoremTarget,
    RealNumericalPredictionVectorRunTarget ]

theorem decisiveMathematicalObjectTargets_length :
    decisiveMathematicalObjectTargets.length = 5 := by
  native_decide

def centralMathematicalSlogan : String :=
  "Nontrivial registered structure forces a nonzero quantitative gap."

def decisiveTargetRegistryStatus : String :=
  "OPEN_TARGET_REGISTRY_ONLY_NO_MATHEMATICAL_CLOSURE"

end Chronos.Frontier
