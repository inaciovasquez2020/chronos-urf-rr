namespace Chronos
namespace Frontier

/--
Repository-native spherical null-expansion input.

`outgoingExpansion` represents theta_+.
`ingoingExpansion` represents theta_-.
-/
structure SphericalNullExpansionInput where
  outgoingExpansion : Int
  ingoingExpansion : Int

def FutureTrappedSphericalSurface
    (S : SphericalNullExpansionInput) : Prop :=
  S.outgoingExpansion < 0 ∧ S.ingoingExpansion < 0

def FutureOuterMarginalSphericalSurface
    (S : SphericalNullExpansionInput) : Prop :=
  S.outgoingExpansion <= 0 ∧ S.ingoingExpansion < 0

def TrappedOrMarginalByNullExpansions
    (S : SphericalNullExpansionInput) : Prop :=
  FutureTrappedSphericalSurface S ∨ FutureOuterMarginalSphericalSurface S

theorem trapped_spherical_null_expansions_imply_trapped_or_marginal
    (S : SphericalNullExpansionInput) :
    FutureTrappedSphericalSurface S ->
      TrappedOrMarginalByNullExpansions S := by
  intro h
  exact Or.inl h

theorem marginal_spherical_null_expansions_imply_trapped_or_marginal
    (S : SphericalNullExpansionInput) :
    FutureOuterMarginalSphericalSurface S ->
      TrappedOrMarginalByNullExpansions S := by
  intro h
  exact Or.inr h

/--
Boundary marker.

This file closes only the restricted spherical null-expansion criterion surface.
It does not prove the compactness-threshold-to-null-expansion bridge, nonspherical
collapse exclusion, Cosmic Censorship, the Hoop Conjecture, or unrestricted
UniversalBoundaryCompactness.
-/
def SphericalNullExpansionCriterionBoundary : Prop := True

theorem spherical_null_expansion_criterion_boundary_verified :
    SphericalNullExpansionCriterionBoundary := by
  trivial

end Frontier
end Chronos
