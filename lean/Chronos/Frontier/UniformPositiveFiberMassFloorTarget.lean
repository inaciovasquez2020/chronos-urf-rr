import Mathlib.Data.Real.Basic

namespace Chronos
namespace Frontier

/--
A minimal abstract fiber-mass domain for the first global URF sink:
the missing uniform positive fiber-mass floor.
-/
structure FiberMassDomain where
  Fiber : Type
  admissible : Fiber → Prop
  mass : Fiber → ℝ

/--
Closure exit for the first sink.

This is a target object only: it states the exact floor that would be
needed to advance the restricted UFEG/Chronos-RR route.
-/
def UniformPositiveFiberMassFloor (D : FiberMassDomain) : Prop :=
  ∃ epsilon : ℝ,
    0 < epsilon ∧
      ∀ x : D.Fiber, D.admissible x → epsilon ≤ D.mass x

/--
Countermodel exit for the first sink.

A sequence of admissible positive-mass fibers with masses arbitrarily close
to zero blocks any global positive lower floor.
-/
def NoUniformPositiveFiberMassFloorCountermodel
    (D : FiberMassDomain) : Prop :=
  ∃ sequence : Nat → D.Fiber,
    (∀ n : Nat, D.admissible (sequence n)) ∧
      (∀ n : Nat, 0 < D.mass (sequence n)) ∧
        ∀ epsilon : ℝ,
          0 < epsilon → ∃ n : Nat, D.mass (sequence n) < epsilon

/--
Every first-sink resolution must be either a closure certificate or a
countermodel certificate.
-/
inductive UniformPositiveFiberMassSinkResolution
    (D : FiberMassDomain) : Prop where
  | closure :
      UniformPositiveFiberMassFloor D →
      UniformPositiveFiberMassSinkResolution D
  | countermodel :
      NoUniformPositiveFiberMassFloorCountermodel D →
      UniformPositiveFiberMassSinkResolution D

theorem uniform_positive_floor_closure_resolves_sink
    (D : FiberMassDomain)
    (h : UniformPositiveFiberMassFloor D) :
    UniformPositiveFiberMassSinkResolution D := by
  exact UniformPositiveFiberMassSinkResolution.closure h

theorem no_uniform_positive_floor_countermodel_resolves_sink
    (D : FiberMassDomain)
    (h : NoUniformPositiveFiberMassFloorCountermodel D) :
    UniformPositiveFiberMassSinkResolution D := by
  exact UniformPositiveFiberMassSinkResolution.countermodel h

/--
A countermodel certificate excludes the closure certificate.
-/
theorem countermodel_excludes_uniform_positive_floor
    (D : FiberMassDomain)
    (hCounter : NoUniformPositiveFiberMassFloorCountermodel D) :
    ¬ UniformPositiveFiberMassFloor D := by
  intro hFloor
  rcases hCounter with ⟨sequence, hAdmissible, _hPositiveMass, hSmall⟩
  rcases hFloor with ⟨epsilon, hEpsilonPos, hFloorBound⟩
  rcases hSmall epsilon hEpsilonPos with ⟨n, hnSmall⟩
  have hle : epsilon ≤ D.mass (sequence n) :=
    hFloorBound (sequence n) (hAdmissible n)
  exact (not_lt_of_ge hle) hnSmall

def UniformPositiveFiberMassFloorTargetStatus : String :=
  "OPEN_TARGET_SURFACE_ONLY"

def UniformPositiveFiberMassFloorTargetBoundary : String :=
  "Does not prove existence of a uniform positive fiber-mass floor."

end Frontier
end Chronos
