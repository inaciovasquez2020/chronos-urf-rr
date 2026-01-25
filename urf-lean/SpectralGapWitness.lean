import urf_core.URF_Axioms_Core

open URF

namespace URFWitness

-- Real objects from urf-core
abbrev H := URF.H
abbrev L := URF.L
abbrev V := URF.defectSpace   -- ker(Per)
abbrev ε₀ := URF.epsilon0

-- Binding theorem (now references real core)
theorem spectral_gap :
  inf_spec (L.restrict (Vᶜ)) ≥ ε₀ :=
by
  exact URF.spectral_gap_core

end URFWitness

