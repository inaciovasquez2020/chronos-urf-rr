import URF_Core.URF_Axioms_Core

open URF

namespace URFWitness

abbrev H := URF.H
abbrev L := URF.L
abbrev V := URF.defectSpace
abbrev ε₀ := URF.epsilon0

theorem spectral_gap :
  inf_spec (restrict L Vᶜ) ≥ ε₀ :=
by
  exact URF.spectral_gap_core

end URFWitness

