/-
URF witness scaffold.

Target theorem shape:
  theorem spectral_gap :
    inf_spec (L.restrict (Vᶜ)) ≥ ε₀

This file is intentionally a scaffold: you will connect it to your existing URF core
(L, defect space V=ker(Per), truncation/certificate pipeline).
-/

namespace URFWitness

-- Placeholder types
universe u
variable {H : Type u}

-- Placeholder objects (replace with your actual Hilbert space, operator, and defect space)
constant L : H → H
constant V : Set H
constant ε₀ : Prop

-- TODO: replace ε₀ : Prop by ε₀ : ℝ and state a real spectral bound theorem.

theorem spectral_gap_scaffold : True := by
  trivial

end URFWitness
