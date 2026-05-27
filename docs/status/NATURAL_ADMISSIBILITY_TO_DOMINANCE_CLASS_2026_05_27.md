# Natural Admissibility to Dominance Class — 2026-05-27

Status: `NATURAL_ADMISSIBILITY_TO_DOMINANCE_CLASS_INTERFACE`

This connects target-facing admissibility data to `DominanceAdmissibleComputableClass`.

## Core interface

```lean
structure NaturalAdmissibilityDominanceCertificate
    (X : ComputableFiniteAdmissibleClass) where
  admissible_witness : X.admissible
  rank_entropy_dominance :
    SemanticRankRate X <= FiberEntropyGap X
set -euo pipefail

cd ~/chronos-urf-rr

BRANCH="formalize/natural-admissibility-to-dominance-class-2026-05-27"
LEAN="lean/Chronos/Frontier/NaturalAdmissibilityToDominanceClass.lean"
ART="artifacts/chronos/natural_admissibility_to_dominance_class_2026_05_27.json"
DOC="docs/status/NATURAL_ADMISSIBILITY_TO_DOMINANCE_CLASS_2026_05_27.md"
VERIFY="tools/verify_natural_admissibility_to_dominance_class.py"
TEST="tests/test_natural_admissibility_to_dominance_class.py"

git fetch origin main
git checkout main
git pull --ff-only origin main
git checkout -B "$BRANCH"

mkdir -p lean/Chronos/Frontier artifacts/chronos docs/status tools tests

cat > "$LEAN" <<'LEAN'
import Chronos.Frontier.DominanceAdmissibleComputableClass

namespace Chronos
namespace Frontier

/--
A natural admissibility interface for target applications.

This packages the exact data a target application must supply in order to
enter the dominance-admissible computable class.
-/
structure NaturalAdmissibilityDominanceCertificate
    (X : ComputableFiniteAdmissibleClass) where
  admissible_witness : X.admissible
  rank_entropy_dominance :
    SemanticRankRate X ≤ FiberEntropyGap X

/--
A target-facing admissible computable object.

The field `natural_certificate` is the bridge from application-specific
admissibility to dominance admissibility.
-/
structure NaturalDominanceAdmissibleComputableClass where
  base : ComputableFiniteAdmissibleClass
  natural_certificate :
    NaturalAdmissibilityDominanceCertificate base

def NaturalDominanceSemanticRankRate
    (X : NaturalDominanceAdmissibleComputableClass) : Nat :=
  SemanticRankRate X.base

def NaturalDominanceFiberEntropyGap
    (X : NaturalDominanceAdmissibleComputableClass) : Nat :=
  FiberEntropyGap X.base

def natural_to_dominance_admissible
    (X : NaturalDominanceAdmissibleComputableClass) :
    DominanceAdmissibleComputableClass where
  base := X.base
  admissible_witness := X.natural_certificate.admissible_witness
  rank_entropy_dominance := X.natural_certificate.rank_entropy_dominance

theorem natural_admissibility_supplies_dominance_class
    (X : NaturalDominanceAdmissibleComputableClass) :
    DominanceSemanticRankRate (natural_to_dominance_admissible X)
      ≤ DominanceFiberEntropyGap (natural_to_dominance_admissible X) := by
  exact dominance_admissible_bridge (natural_to_dominance_admissible X)

theorem natural_admissibility_bridge
    (X : NaturalDominanceAdmissibleComputableClass) :
    NaturalDominanceSemanticRankRate X ≤
      NaturalDominanceFiberEntropyGap X := by
  exact X.natural_certificate.rank_entropy_dominance

theorem natural_admissibility_finite_support
    (X : NaturalDominanceAdmissibleComputableClass) :
    X.base.objectCount > 0 := by
  exact X.base.finite_support

theorem natural_admissibility_semantic_rank_computable
    (X : NaturalDominanceAdmissibleComputableClass) :
    ∃ n : Nat, n = NaturalDominanceSemanticRankRate X := by
  exact X.base.semantic_rank_rate_computable

theorem natural_admissibility_fiber_entropy_computable
    (X : NaturalDominanceAdmissibleComputableClass) :
    ∃ n : Nat, n = NaturalDominanceFiberEntropyGap X := by
  exact X.base.fiber_entropy_gap_computable

/--
Remaining application-level problem: each target application must construct
`NaturalAdmissibilityDominanceCertificate` from its own admissibility axioms.
-/
def TargetApplicationCertificateProblem : Prop :=
  ∀ X : ComputableFiniteAdmissibleClass,
    X.admissible →
      NaturalAdmissibilityDominanceCertificate X

end Frontier
end Chronos
LEAN

python3 - <<'PY'
from pathlib import Path

p = Path("lean/Chronos.lean")
s = p.read_text()
line = "import Chronos.Frontier.NaturalAdmissibilityToDominanceClass\n"
if line not in s:
    p.write_text(line + s)
PY

cat > "$ART" <<'JSON'
{
  "date": "2026-05-27",
  "status": "NATURAL_ADMISSIBILITY_TO_DOMINANCE_CLASS_INTERFACE",
  "object": "NaturalDominanceAdmissibleComputableClass",
  "proved": [
    "natural admissibility dominance certificate constructs DominanceAdmissibleComputableClass",
    "natural admissibility supplies SemanticRankRate <= FiberEntropyGap",
    "natural admissibility preserves finite-support positivity",
    "natural admissibility preserves computability of SemanticRankRate",
    "natural admissibility preserves computability of FiberEntropyGap"
  ],
  "next_missing_ingredient": "construct NaturalAdmissibilityDominanceCertificate inside each target application",
  "does_not_prove": [
    "certificate construction for any target application",
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
# Natural Admissibility to Dominance Class — 2026-05-27

Status: `NATURAL_ADMISSIBILITY_TO_DOMINANCE_CLASS_INTERFACE`

This connects target-facing admissibility data to `DominanceAdmissibleComputableClass`.

## Core interface

```lean
structure NaturalAdmissibilityDominanceCertificate
    (X : ComputableFiniteAdmissibleClass) where
  admissible_witness : X.admissible
  rank_entropy_dominance :
    SemanticRankRate X <= FiberEntropyGap X
Proved
natural admissibility dominance certificate constructs DominanceAdmissibleComputableClass
natural admissibility supplies SemanticRankRate X <= FiberEntropyGap X
finite-support positivity is preserved
semantic rank computability is preserved
fiber entropy computability is preserved
Next missing ingredient
Construct NaturalAdmissibilityDominanceCertificate inside each target application.
Does not prove
certificate construction for any target application
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
