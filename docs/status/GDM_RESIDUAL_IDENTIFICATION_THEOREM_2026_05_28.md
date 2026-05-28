# GDM Residual Identification Theorem — 2026-05-28

Status: `GDM_RESIDUAL_IDENTIFICATION_PROVED_FINITE_NONNEGATIVE_MODEL_ONLY`

## Name

`GDM`: Gravity Dark Matter / Geometric Deficit Mass.

## Object

`GDMResidualData` is a finite nonnegative residual-identification model.

Core decomposition:

```text
observedMass = baryonicMass + geometricDeficitMass
set -euo pipefail

cd ~/chronos-urf-rr

BRANCH="formalize/gdm-residual-identification-theorem-2026-05-28"
LEAN="lean/Chronos/Frontier/GDMResidualIdentificationTheorem.lean"
ART="artifacts/chronos/gdm_residual_identification_theorem_2026_05_28.json"
DOC="docs/status/GDM_RESIDUAL_IDENTIFICATION_THEOREM_2026_05_28.md"
VERIFY="tools/verify_gdm_residual_identification_theorem.py"
TEST="tests/test_gdm_residual_identification_theorem.py"

git checkout main
git pull --ff-only origin main
git checkout -b "$BRANCH"

mkdir -p lean/Chronos/Frontier artifacts/chronos docs/status tools tests

cat > "$LEAN" <<'LEAN_EOF'
namespace Chronos.Frontier

/--
GDM residual identification model.

This is still only a finite nonnegative model.  It closes the internal
dark-matter-residual accounting step:

observed/effective gravitational mass =
baryonic mass + geometric deficit mass

therefore

observed residual = geometric deficit mass.
-/
structure GDMResidualData where
  baryonicMass : Nat
  geometricDeficitMass : Nat
deriving Repr, DecidableEq

namespace GDMResidual

def observedMass (d : GDMResidualData) : Nat :=
  d.baryonicMass + d.geometricDeficitMass

def residualMass (d : GDMResidualData) : Nat :=
  observedMass d - d.baryonicMass

theorem observed_mass_decomposition (d : GDMResidualData) :
    observedMass d = d.baryonicMass + d.geometricDeficitMass := rfl

theorem residual_identifies_geometric_deficit (d : GDMResidualData) :
    residualMass d = d.geometricDeficitMass := by
  simp [residualMass, observedMass]

theorem zero_residual_iff_zero_deficit (d : GDMResidualData) :
    residualMass d = 0 ↔ d.geometricDeficitMass = 0 := by
  rw [residual_identifies_geometric_deficit]

theorem positive_deficit_implies_positive_residual (d : GDMResidualData)
    (h : 0 < d.geometricDeficitMass) :
    0 < residualMass d := by
  rw [residual_identifies_geometric_deficit]
  exact h

theorem positive_residual_implies_positive_deficit (d : GDMResidualData)
    (h : 0 < residualMass d) :
    0 < d.geometricDeficitMass := by
  rwa [residual_identifies_geometric_deficit] at h

def status : String :=
  "GDM_RESIDUAL_IDENTIFICATION_PROVED_FINITE_NONNEGATIVE_MODEL_ONLY"

theorem status_eq :
    status =
      "GDM_RESIDUAL_IDENTIFICATION_PROVED_FINITE_NONNEGATIVE_MODEL_ONLY" := rfl

end GDMResidual

end Chronos.Frontier
LEAN_EOF

grep -q "Chronos.Frontier.GDMResidualIdentificationTheorem" lean/Chronos.lean || printf '\nimport Chronos.Frontier.GDMResidualIdentificationTheorem\n' >> lean/Chronos.lean

cat > "$ART" <<'JSON_EOF'
{
  "id": "GDM_RESIDUAL_IDENTIFICATION_THEOREM_V1",
  "date": "2026-05-28",
  "status": "GDM_RESIDUAL_IDENTIFICATION_PROVED_FINITE_NONNEGATIVE_MODEL_ONLY",
  "toolkit_name": "GDM",
  "expanded_name": "Gravity Dark Matter / Geometric Deficit Mass",
  "mathematical_object": "finite nonnegative residual-identification model",
  "core_decomposition": "observedMass = baryonicMass + geometricDeficitMass",
  "proved_identification": "residualMass = observedMass - baryonicMass = geometricDeficitMass",
  "proved_theorems": [
    "GDMResidual.observed_mass_decomposition",
    "GDMResidual.residual_identifies_geometric_deficit",
    "GDMResidual.zero_residual_iff_zero_deficit",
    "GDMResidual.positive_deficit_implies_positive_residual",
    "GDMResidual.positive_residual_implies_positive_deficit"
  ],
  "modeling_closure": "Within the finite nonnegative GDM model, the dark-matter-like residual is exactly identified with the geometric deficit mass.",
  "intended_gravity_use": "Convert a gravity-side apparent missing-mass residual into a named geometric-deficit variable before any observational, lensing, rotation-curve, or field-equation instantiation.",
  "boundary": [
    "finite nonnegative model only",
    "internal residual-identification theorem only",
    "no observational evidence",
    "no galaxy rotation curve fit",
    "no lensing fit",
    "no empirical residual measurement",
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
# GDM Residual Identification Theorem — 2026-05-28

Status: `GDM_RESIDUAL_IDENTIFICATION_PROVED_FINITE_NONNEGATIVE_MODEL_ONLY`

## Name

`GDM`: Gravity Dark Matter / Geometric Deficit Mass.

## Object

`GDMResidualData` is a finite nonnegative residual-identification model.

Core decomposition:

```text
observedMass = baryonicMass + geometricDeficitMass
Residual definition:
residualMass = observedMass - baryonicMass
Proved Lean theorem
The dark-matter-like residual is exactly the geometric deficit:
residualMass = geometricDeficitMass
Lean theorem:
GDMResidual.residual_identifies_geometric_deficit
Additional proved consequences
GDMResidual.observed_mass_decomposition
GDMResidual.zero_residual_iff_zero_deficit
GDMResidual.positive_deficit_implies_positive_residual
GDMResidual.positive_residual_implies_positive_deficit
Boundary
This artifact proves only a finite nonnegative residual-identification theorem.
It does not provide observational evidence, galaxy rotation curve fits, lensing fits, empirical residual measurement, a dark matter replacement, a Lambda-CDM refutation, a modified gravity theorem, an Einstein-matter theorem, a collapse theorem, Cosmic Censorship, the Hoop Conjecture, quantum gravity, unrestricted Chronos-RR, unrestricted H4.1/FGL, P vs NP, or any Clay problem.
