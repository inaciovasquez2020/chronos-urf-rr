/-
  Conditional SIDFH conserved-source surface.

  This file does not prove gravity recovery and does not derive conservation
  from the proposed SIDFH bridge tensor.  It records the weakest admissible
  replacement for the previous informal conservation claim: conservation is an
  explicit invariant supplied to any downstream flat-curve or gravity-recovery
  theorem.
-/

namespace Chronos
namespace Frontier

universe u

/-- An abstract index type for the spacetime component being tested. -/
structure SIDFHIndexSurface where
  Index : Type u

/--
A minimal source surface for an SIDFH correction tensor.

`divergence ν` represents the component
`∇ᵐ Ω_{mν}` without asserting any analytic formula for `Ω`.
-/
structure SIDFHSourceSurface (ι : SIDFHIndexSurface.{u}) where
  Omega : ι.Index → ι.Index → Prop
  divergence : ι.Index → Prop

/--
The weakest conservation invariant needed before an SIDFH correction can be
used as a consistent source in a modified gravitational field equation.
-/
structure ConservedSIDFHSource
    (ι : SIDFHIndexSurface.{u})
    (S : SIDFHSourceSurface ι) : Prop where
  conserved : ∀ ν : ι.Index, S.divergence ν

/--
Projection theorem: once `ConservedSIDFHSource` is supplied, the componentwise
conservation statement is available.

This is intentionally conditional; it does not prove conservation from any
bridge-tensor formula.
-/
theorem conservedSIDFHSource_divergence
    {ι : SIDFHIndexSurface.{u}}
    {S : SIDFHSourceSurface ι}
    (h : ConservedSIDFHSource ι S) :
    ∀ ν : ι.Index, S.divergence ν :=
  h.conserved

/--
A named boundary marker for the current state of the gravity program.

`False` is used here as a proposition marker: this file introduces no theorem
that closes full gravity recovery.
-/
def solvedGravityFromCurrentSIDFHDerivation : Prop :=
  False

end Frontier
end Chronos
