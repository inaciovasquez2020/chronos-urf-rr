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


namespace Chronos.Frontier.GDMEmpiricalMassMapBindingTheorem

def equalMassActualWitness : GDMEmpiricalMassMap :=
  { baryonicMass := 42, apparentMass := 42 }

def positiveResidualActualWitness : GDMEmpiricalMassMap :=
  { baryonicMass := 42, apparentMass := 57 }

def exactBindingActualWitness : GDMEmpiricalMassMap :=
  { baryonicMass := 40, apparentMass := 55 }

theorem equal_mass_actual_values :
    empiricalResidualMass equalMassActualWitness = 0 := by
  simp [equalMassActualWitness, empiricalResidualMass]

theorem positive_residual_actual_values :
    empiricalResidualMass positiveResidualActualWitness = 15 := by
  simp [positiveResidualActualWitness, empiricalResidualMass]

theorem exact_binding_actual_values :
    boundApparentMass exactBindingActualWitness = exactBindingActualWitness.apparentMass := by
  simp [exactBindingActualWitness, boundApparentMass, empiricalResidualMass]

end Chronos.Frontier.GDMEmpiricalMassMapBindingTheorem
