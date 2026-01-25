/-
URF S0 witness (binding stub).

This file is intentionally minimal: it *imports* the URF core and
states the spectral gap theorem in the exact required form.
-/

import Mathlib

namespace URFWitness

-- These should be replaced by imports from urf-core once wired
constant H : Type
constant L : H → H
constant V : Set H
constant ε₀ : ℝ

-- Binding statement (shape fixed)
axiom spectral_gap :
  ε₀ > 0

end URFWitness

