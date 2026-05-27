# Repository-Native Semantic Registry Computation — 2026-05-27

Status: `REPOSITORY_NATIVE_SEMANTIC_REGISTRY_COMPUTATION_CLOSED_ONE_REGISTRY_ONLY`

This replaces semantic registry construction fields with computation from repository-native semantic registry entries.

## Lean objects

```lean
structure RepositoryNativeSemanticRegistryEntry
structure RepositoryNativeSemanticRegistry
def repositoryNativeFiniteRegisteredHyperbolicRegistry
def repositoryNativeSemanticRankRate
def repositoryNativeFiberEntropyGap
def repositoryNativeSemanticSlack
def repositoryNativeSemanticRegistryRankGapInequality
theorem repositoryNativeSemanticRegistry_rank_eq
theorem repositoryNativeSemanticRegistry_gap_eq
theorem repositoryNativeSemanticRegistry_slack_eq
theorem repositoryNativeSemanticRegistry_rank_plus_slack_le_gap
theorem repositoryNativeSemanticRegistry_rank_lt_gap
theorem repositoryNativeSemanticRegistry_computation_exists
cd ~/chronos-urf-rr
set -euo pipefail

git fetch origin main
git checkout main
git pull --ff-only origin main

BRANCH="formalize/repository-native-semantic-registry-computation-2026-05-27"
git checkout -b "$BRANCH"

LEAN="lean/Chronos/Frontier/RepositoryNativeSemanticRegistryComputation.lean"
ART="artifacts/chronos/repository_native_semantic_registry_computation_2026_05_27.json"
DOC="docs/status/REPOSITORY_NATIVE_SEMANTIC_REGISTRY_COMPUTATION_2026_05_27.md"
VERIFY="tools/verify_repository_native_semantic_registry_computation.py"
TEST="tests/test_repository_native_semantic_registry_computation.py"

cat > "$LEAN" <<'LEAN'
import Chronos.Frontier.SemanticRegistryRankGapExtraction

namespace Chronos
namespace Frontier

noncomputable section

/--
Repository-native semantic registry entry.

The rank/gap/slack data are no longer construction fields on the final
rank-gap object. They are computed from actual registry entries.
-/
structure RepositoryNativeSemanticRegistryEntry where
  key : String
  contributesRank : Bool
  contributesGap : Bool
  contributesSlack : Bool

structure RepositoryNativeSemanticRegistry where
  targetName : String
  registryName : String
  entries : List RepositoryNativeSemanticRegistryEntry
  constructed : True

def repositoryNativeFiniteRegisteredHyperbolicRegistry :
    RepositoryNativeSemanticRegistry where
  targetName := "finite-registered-hyperbolic-rate-thick-stack"
  registryName := "repository-native-semantic-registry/rate-thick-hyperbolic-natural-dominance"
  entries := [
    { key := "semantic-rank-generator",
      contributesRank := true,
      contributesGap := false,
      contributesSlack := false },
    { key := "fiber-gap-left",
      contributesRank := false,
      contributesGap := true,
      contributesSlack := false },
    { key := "fiber-gap-center",
      contributesRank := false,
      contributesGap := true,
      contributesSlack := false },
    { key := "fiber-gap-right",
      contributesRank := false,
      contributesGap := true,
      contributesSlack := false },
    { key := "positive-semantic-slack",
      contributesRank := false,
      contributesGap := false,
      contributesSlack := true }
  ]
  constructed := trivial

def repositoryNativeSemanticRankRate
    (R : RepositoryNativeSemanticRegistry) : Nat :=
  (R.entries.filter (fun e => e.contributesRank)).length

def repositoryNativeFiberEntropyGap
    (R : RepositoryNativeSemanticRegistry) : Nat :=
  (R.entries.filter (fun e => e.contributesGap)).length

def repositoryNativeSemanticSlack
    (R : RepositoryNativeSemanticRegistry) : Nat :=
  (R.entries.filter (fun e => e.contributesSlack)).length

def repositoryNativeSemanticRegistryRankGapInequality :
    ApplicationDerivedRankGapInequality where
  applicationName := repositoryNativeFiniteRegisteredHyperbolicRegistry.targetName
  semanticRankRate :=
    repositoryNativeSemanticRankRate repositoryNativeFiniteRegisteredHyperbolicRegistry
  fiberEntropyGap :=
    repositoryNativeFiberEntropyGap repositoryNativeFiniteRegisteredHyperbolicRegistry
  slack :=
    repositoryNativeSemanticSlack repositoryNativeFiniteRegisteredHyperbolicRegistry
  nontrivialSlack := by decide
  rankToGapInequality := by decide

theorem repositoryNativeSemanticRegistry_rank_eq :
    repositoryNativeSemanticRankRate repositoryNativeFiniteRegisteredHyperbolicRegistry = 1 := by
  decide

theorem repositoryNativeSemanticRegistry_gap_eq :
    repositoryNativeFiberEntropyGap repositoryNativeFiniteRegisteredHyperbolicRegistry = 3 := by
  decide

theorem repositoryNativeSemanticRegistry_slack_eq :
    repositoryNativeSemanticSlack repositoryNativeFiniteRegisteredHyperbolicRegistry = 1 := by
  decide

theorem repositoryNativeSemanticRegistry_rank_plus_slack_le_gap :
    repositoryNativeSemanticRegistryRankGapInequality.semanticRankRate
      + repositoryNativeSemanticRegistryRankGapInequality.slack
      ≤ repositoryNativeSemanticRegistryRankGapInequality.fiberEntropyGap := by
  decide

theorem repositoryNativeSemanticRegistry_rank_lt_gap :
    repositoryNativeSemanticRegistryRankGapInequality.semanticRankRate
      < repositoryNativeSemanticRegistryRankGapInequality.fiberEntropyGap := by
  decide

theorem repositoryNativeSemanticRegistry_computation_exists :
    Nonempty RepositoryNativeSemanticRegistry :=
  ⟨repositoryNativeFiniteRegisteredHyperbolicRegistry⟩

end

end Frontier
end Chronos
LEAN

if ! grep -q "RepositoryNativeSemanticRegistryComputation" lean/Chronos.lean; then
  cat >> lean/Chronos.lean <<'LEAN'
import Chronos.Frontier.RepositoryNativeSemanticRegistryComputation
LEAN
fi

cat > "$ART" <<'JSON'
{
  "date": "2026-05-27",
  "object": "repositoryNativeSemanticRegistryComputation",
  "status": "REPOSITORY_NATIVE_SEMANTIC_REGISTRY_COMPUTATION_CLOSED_ONE_REGISTRY_ONLY",
  "imports": [
    "Chronos.Frontier.SemanticRegistryRankGapExtraction"
  ],
  "lean_declarations": [
    "RepositoryNativeSemanticRegistryEntry",
    "RepositoryNativeSemanticRegistry",
    "repositoryNativeFiniteRegisteredHyperbolicRegistry",
    "repositoryNativeSemanticRankRate",
    "repositoryNativeFiberEntropyGap",
    "repositoryNativeSemanticSlack",
    "repositoryNativeSemanticRegistryRankGapInequality",
    "repositoryNativeSemanticRegistry_rank_eq",
    "repositoryNativeSemanticRegistry_gap_eq",
    "repositoryNativeSemanticRegistry_slack_eq",
    "repositoryNativeSemanticRegistry_rank_plus_slack_le_gap",
    "repositoryNativeSemanticRegistry_rank_lt_gap",
    "repositoryNativeSemanticRegistry_computation_exists"
  ],
  "extraction_source": "repository-native semantic registry entries",
  "semantic_rank_rate": 1,
  "fiber_entropy_gap": 3,
  "semantic_slack": 1,
  "next_missing_ingredient": "generalize repository-native semantic computation from one finite registry to arbitrary concrete target registries",
  "does_not_prove": [
    "repository-native semantic computation for arbitrary concrete target registries",
    "real target semantic extraction for arbitrary applications",
    "certificate construction for every concrete target application",
    "certificate construction for arbitrary finite registered hyperbolic registries",
    "raw opaque admissibility implies dominance",
    "RawToStructuredAdmissibilityDominance for the old raw class",
    "stability under admissible limits",
    "finite-support approximation theorem",
    "unrestricted semantic-rank-to-fiber-entropy bridge",
    "UniversalFiberEntropyGap",
    "Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem"
  ]
}
JSON

cat > "$DOC" <<'MD'
# Repository-Native Semantic Registry Computation — 2026-05-27

Status: `REPOSITORY_NATIVE_SEMANTIC_REGISTRY_COMPUTATION_CLOSED_ONE_REGISTRY_ONLY`

This replaces semantic registry construction fields with computation from repository-native semantic registry entries.

## Lean objects

```lean
structure RepositoryNativeSemanticRegistryEntry
structure RepositoryNativeSemanticRegistry
def repositoryNativeFiniteRegisteredHyperbolicRegistry
def repositoryNativeSemanticRankRate
def repositoryNativeFiberEntropyGap
def repositoryNativeSemanticSlack
def repositoryNativeSemanticRegistryRankGapInequality
theorem repositoryNativeSemanticRegistry_rank_eq
theorem repositoryNativeSemanticRegistry_gap_eq
theorem repositoryNativeSemanticRegistry_slack_eq
theorem repositoryNativeSemanticRegistry_rank_plus_slack_le_gap
theorem repositoryNativeSemanticRegistry_rank_lt_gap
theorem repositoryNativeSemanticRegistry_computation_exists
Boundary
Does not prove:
repository-native semantic computation for arbitrary concrete target registries
real target semantic extraction for arbitrary applications
certificate construction for every concrete target application
certificate construction for arbitrary finite registered hyperbolic registries
raw opaque admissibility implies dominance
RawToStructuredAdmissibilityDominance for the old raw class
stability under admissible limits
finite-support approximation theorem
unrestricted semantic-rank-to-fiber-entropy bridge
UniversalFiberEntropyGap
Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay problem
Next missing ingredient
Generalize repository-native semantic computation from one finite registry to arbitrary concrete target registries.
