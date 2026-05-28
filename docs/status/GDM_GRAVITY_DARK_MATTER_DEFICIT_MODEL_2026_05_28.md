# GDM Gravity Dark Matter Deficit Model — 2026-05-28

Status: `GDM_DEFICIT_ACCOUNTING_MODEL_PROVED_FINITE_NONNEGATIVE_ONLY`

## Name

`GDM`: Gravity Dark Matter / Geometric Deficit Mass.

## Object

`GDMData` is a finite nonnegative gravitational deficit-accounting model.

Core identity:

```text
effectiveMass = baryonicMass + geometricDeficitMass
set -euo pipefail

cd ~/chronos-urf-rr

BRANCH="formalize/gdm-gravity-dark-matter-deficit-model-2026-05-28"
LEAN="lean/Chronos/Frontier/GDMGravityDarkMatterDeficitModel.lean"
ART="artifacts/chronos/gdm_gravity_dark_matter_deficit_model_2026_05_28.json"
DOC="docs/status/GDM_GRAVITY_DARK_MATTER_DEFICIT_MODEL_2026_05_28.md"
VERIFY="tools/verify_gdm_gravity_dark_matter_deficit_model.py"
TEST="tests/test_gdm_gravity_dark_matter_deficit_model.py"

git checkout main
git pull --ff-only origin main
git checkout -b "$BRANCH"

mkdir -p lean/Chronos/Frontier artifacts/chronos docs/status tools tests

cat > "$LEAN" <<'LEAN_EOF'
namespace Chronos.Frontier

/--
GDM = Gravity Dark Matter, formalized here only as a finite
nonnegative deficit-accounting model.

Interpretation:
effective gravitational mass = visible/baryonic mass + geometric deficit mass.
-/
structure GDMData where
  baryonicMass : Nat
  geometricDeficitMass : Nat
deriving Repr, DecidableEq

namespace GDM

def effectiveMass (d : GDMData) : Nat :=
  d.baryonicMass + d.geometricDeficitMass

def residualMass (d : GDMData) : Nat :=
  effectiveMass d - d.baryonicMass

theorem baryonic_le_effective (d : GDMData) :
    d.baryonicMass <= effectiveMass d := by
  simp [effectiveMass]

theorem zero_deficit_effective_eq_baryonic (d : GDMData)
    (h : d.geometricDeficitMass = 0) :
    effectiveMass d = d.baryonicMass := by
  simp [effectiveMass, h]

theorem positive_deficit_effective_gt_baryonic (d : GDMData)
    (h : 0 < d.geometricDeficitMass) :
    d.baryonicMass < effectiveMass d := by
  simp [effectiveMass, Nat.lt_add_right_iff_pos, h]

theorem effective_eq_baryonic_implies_zero_deficit (d : GDMData)
    (h : effectiveMass d = d.baryonicMass) :
    d.geometricDeficitMass = 0 := by
  have hz : d.baryonicMass + d.geometricDeficitMass = d.baryonicMass := h
  exact Nat.eq_zero_of_add_eq_self_left hz

def status : String :=
  "GDM_DEFICIT_ACCOUNTING_MODEL_PROVED_FINITE_NONNEGATIVE_ONLY"

theorem status_eq :
    status = "GDM_DEFICIT_ACCOUNTING_MODEL_PROVED_FINITE_NONNEGATIVE_ONLY" := rfl

end GDM

end Chronos.Frontier
LEAN_EOF

grep -q "Chronos.Frontier.GDMGravityDarkMatterDeficitModel" lean/Chronos.lean || printf '\nimport Chronos.Frontier.GDMGravityDarkMatterDeficitModel\n' >> lean/Chronos.lean

cat > "$ART" <<'JSON_EOF'
{
  "id": "GDM_GRAVITY_DARK_MATTER_DEFICIT_MODEL_V1",
  "date": "2026-05-28",
  "status": "GDM_DEFICIT_ACCOUNTING_MODEL_PROVED_FINITE_NONNEGATIVE_ONLY",
  "toolkit_name": "GDM",
  "expanded_name": "Gravity Dark Matter / Geometric Deficit Mass",
  "mathematical_object": "finite nonnegative gravitational deficit accounting model",
  "proved_theorems": [
    "GDM.baryonic_le_effective",
    "GDM.zero_deficit_effective_eq_baryonic",
    "GDM.positive_deficit_effective_gt_baryonic",
    "GDM.effective_eq_baryonic_implies_zero_deficit"
  ],
  "core_identity": "effectiveMass = baryonicMass + geometricDeficitMass",
  "intended_gravity_use": "Abstractly model a gravity-side apparent dark-matter residual as a nonnegative geometric deficit mass term before any physical or observational instantiation.",
  "new_ingredient": "GDM packages the dark-matter-like gravitational residual as a finite nonnegative deficit object with proved monotonicity and zero-deficit rigidity.",
  "boundary": [
    "finite nonnegative accounting model only",
    "internal theorem only",
    "no observational evidence",
    "no galaxy rotation curve fit",
    "no lensing fit",
    "no dark matter replacement",
    "no Lambda-CDM refutation",
    "no modified gravity theorem",
    "no Einstein-matter theorem",
    "no collapse theorem",
    "no Cosmic Censorship",
    "no Hoop Conjecture",
    "no quantum gravity",
    "no unrestricted Chronos-RR",
    "no unrestricted H4.1/FGL",
    "no P vs NP",
    "no Clay problem"
  ]
}
JSON_EOF

cat > "$DOC" <<'MD_EOF'
# GDM Gravity Dark Matter Deficit Model — 2026-05-28

Status: `GDM_DEFICIT_ACCOUNTING_MODEL_PROVED_FINITE_NONNEGATIVE_ONLY`

## Name

`GDM`: Gravity Dark Matter / Geometric Deficit Mass.

## Object

`GDMData` is a finite nonnegative gravitational deficit-accounting model.

Core identity:

```text
effectiveMass = baryonicMass + geometricDeficitMass
Proved Lean theorems
GDM.baryonic_le_effective
GDM.zero_deficit_effective_eq_baryonic
GDM.positive_deficit_effective_gt_baryonic
GDM.effective_eq_baryonic_implies_zero_deficit
Intended gravity use
GDM abstracts a dark-matter-like gravitational residual as a nonnegative geometric deficit mass term before any physical or observational instantiation.
Boundary
This artifact proves only a finite nonnegative accounting model.
It does not provide observational evidence, galaxy rotation curve fits, lensing fits, a dark matter replacement, a Lambda-CDM refutation, a modified gravity theorem, an Einstein-matter theorem, a collapse theorem, Cosmic Censorship, the Hoop Conjecture, quantum gravity, unrestricted Chronos-RR, unrestricted H4.1/FGL, P vs NP, or any Clay problem.
