namespace Chronos.Frontier.GDMEmpiricalMassMapBindingTheorem

structure GDMEmpiricalMassMap where
  baryonicMass : Nat
  apparentMass : Nat
deriving Repr, DecidableEq

def empiricalResidualMass (x : GDMEmpiricalMassMap) : Nat :=
  x.apparentMass - x.baryonicMass

def boundApparentMass (x : GDMEmpiricalMassMap) : Nat :=
  x.baryonicMass + empiricalResidualMass x

def exactEmpiricalMassBindingObligation (x : GDMEmpiricalMassMap) : Prop :=
  boundApparentMass x = x.apparentMass

theorem empirical_mass_map_binding_from_obligation
    (x : GDMEmpiricalMassMap)
    (h : exactEmpiricalMassBindingObligation x) :
    boundApparentMass x = x.apparentMass := h

theorem zero_residual_under_identical_masses (m : Nat) :
    empiricalResidualMass { baryonicMass := m, apparentMass := m } = 0 := by
  simp [empiricalResidualMass]

end Chronos.Frontier.GDMEmpiricalMassMapBindingTheorem
