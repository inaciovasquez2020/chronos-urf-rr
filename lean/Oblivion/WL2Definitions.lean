import Oblivion.CycleOverlapDefinitions

namespace Oblivion

variable {V : Type}

/-- WL² color type. -/
structure WL2Color where
  id : Nat
deriving DecidableEq

/-- WL² vertex color placeholder. -/
def wl2Color (G : Graph V) (v : V) : WL2Color :=
  ⟨0⟩

/-- WL² color equality predicate. -/
def sameWL2Color (G : Graph V) (u v : V) : Prop :=
  wl2Color G u = wl2Color G v

end Oblivion
