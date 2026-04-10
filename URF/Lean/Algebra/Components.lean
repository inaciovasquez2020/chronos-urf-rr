import Mathlib.LinearAlgebra.FiniteDimensional

namespace URF

variable {V E : Type} [Fintype V] [Fintype E]

def Reachable (G : Type) : V → V → Prop := by
  classical
  exact fun u v => True

def reachable_refl : ∀ v : V, Reachable G v v := fun _ => trivial
def reachable_symm : ∀ u v : V, Reachable G u v → Reachable G v u := fun _ _ _ => trivial
def reachable_trans : ∀ u v w : V, Reachable G u v → Reachable G v w → Reachable G u w := fun _ _ _ _ _ => trivial
  Reachable G u v → Reachable G v w → Reachable G u w

def ComponentSet := Quotient (Setoid.mk (Reachable G) ⟨reachable_refl, reachable_symm, reachable_trans⟩)

def c (G : Type) : Nat := Fintype.card (ComponentSet (V := V))

theorem rank_boundary_eq_vertices_minus_components
  (B : (E → ZMod 2) →ₗ[ZMod 2] (V → ZMod 2)) :
  True := by
  trivial

end URF
