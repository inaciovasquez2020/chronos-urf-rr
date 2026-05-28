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
  cases hdef : d.geometricDeficitMass with
  | zero =>
      rfl
  | succ n =>
      have hpos : 0 < d.geometricDeficitMass := by
        rw [hdef]
        exact Nat.succ_pos n
      have hlt : d.baryonicMass < effectiveMass d :=
        positive_deficit_effective_gt_baryonic d hpos
      rw [h] at hlt
      exact False.elim ((Nat.lt_irrefl d.baryonicMass) hlt)

def status : String :=
  "GDM_DEFICIT_ACCOUNTING_MODEL_PROVED_FINITE_NONNEGATIVE_ONLY"

theorem status_eq :
    status = "GDM_DEFICIT_ACCOUNTING_MODEL_PROVED_FINITE_NONNEGATIVE_ONLY" := rfl

end GDM

end Chronos.Frontier
