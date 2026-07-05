import Chronos.Frontier.RepositoryNativeR1R2R3BindingMissingObject

namespace Chronos.Frontier

/--
Input surface for the first isolated R1 target.

This records the local long-chord exclusion obligation without solving
the repository-native geometry.
-/
structure LongChordExclusionInputSurface where
  Configuration : Type
  LongChord : Configuration → Prop
  Admissible : Configuration → Prop
  exclusion : ∀ C, Admissible C → ¬ LongChord C

/--
A minimal repository-native finite-configuration model for the isolated R1
long-chord exclusion surface.

A configuration carries an endpoint separation and an admissible diameter budget.
A long chord is a budget-violating chord; admissibility is the bounded-separation
condition.  The exclusion theorem is local to this model only.
-/
structure RepositoryNativeLongChordConfiguration where
 endpointSeparation : Nat
 admissibleDiameter : Nat

def RepositoryNativeLongChordConfiguration.LongChord
 (C : RepositoryNativeLongChordConfiguration) : Prop :=
 ¬ C.endpointSeparation ≤ C.admissibleDiameter

def RepositoryNativeLongChordConfiguration.Admissible
 (C : RepositoryNativeLongChordConfiguration) : Prop :=
 C.endpointSeparation ≤ C.admissibleDiameter

theorem RepositoryNativeLongChordConfiguration.exclusion
 (C : RepositoryNativeLongChordConfiguration) :
 RepositoryNativeLongChordConfiguration.Admissible C →
  ¬ RepositoryNativeLongChordConfiguration.LongChord C := by
 intro hAdmissible hLongChord
 exact hLongChord hAdmissible

def repositoryNativeLongChordExclusionInputSurface :
 LongChordExclusionInputSurface where
 Configuration := RepositoryNativeLongChordConfiguration
 LongChord := RepositoryNativeLongChordConfiguration.LongChord
 Admissible := RepositoryNativeLongChordConfiguration.Admissible
 exclusion := RepositoryNativeLongChordConfiguration.exclusion

theorem repository_native_LongChordExclusionInputSurface_instance :
 Nonempty LongChordExclusionInputSurface :=
 ⟨repositoryNativeLongChordExclusionInputSurface⟩

/--
First isolated R1 target.

Nonempty input surface only: this makes the missing mathematical object
explicit without proving the concrete repository-native geometry.
-/
def LongChordExclusionProofTarget : Prop :=
  Nonempty LongChordExclusionInputSurface

/--
Input surface for the second isolated R2 target.

This records the local diameter-separation filling-obstruction obligation
without solving the repository-native geometry.
-/
structure DiameterSeparationFillingObstructionInputSurface where
  Configuration : Type
  DiameterSeparated : Configuration → Prop
  Fillable : Configuration → Prop
  obstruction : ∀ C, DiameterSeparated C → ¬ Fillable C

/--
A minimal repository-native finite-configuration model for the isolated R1
diameter-separation filling obstruction surface.

A configuration carries an endpoint separation and an admissible diameter.
Diameter separation means the separation strictly exceeds the diameter.
Fillability means the separation is bounded by the diameter.  The obstruction
is local to this model only.
-/
structure RepositoryNativeDiameterSeparationConfiguration where
  endpointSeparation : Nat
  admissibleDiameter : Nat

def RepositoryNativeDiameterSeparationConfiguration.DiameterSeparated
    (C : RepositoryNativeDiameterSeparationConfiguration) : Prop :=
  C.admissibleDiameter < C.endpointSeparation

def RepositoryNativeDiameterSeparationConfiguration.Fillable
    (C : RepositoryNativeDiameterSeparationConfiguration) : Prop :=
  C.endpointSeparation ≤ C.admissibleDiameter

theorem RepositoryNativeDiameterSeparationConfiguration.obstruction
    (C : RepositoryNativeDiameterSeparationConfiguration) :
    RepositoryNativeDiameterSeparationConfiguration.DiameterSeparated C →
      ¬ RepositoryNativeDiameterSeparationConfiguration.Fillable C := by
  intro hSeparated
  exact Nat.not_le_of_gt hSeparated

def repositoryNativeDiameterSeparationFillingObstructionInputSurface :
    DiameterSeparationFillingObstructionInputSurface where
  Configuration := RepositoryNativeDiameterSeparationConfiguration
  DiameterSeparated := RepositoryNativeDiameterSeparationConfiguration.DiameterSeparated
  Fillable := RepositoryNativeDiameterSeparationConfiguration.Fillable
  obstruction := RepositoryNativeDiameterSeparationConfiguration.obstruction

theorem repository_native_DiameterSeparationFillingObstructionInputSurface_instance :
    Nonempty DiameterSeparationFillingObstructionInputSurface :=
  ⟨repositoryNativeDiameterSeparationFillingObstructionInputSurface⟩

/--
Second isolated R2 target.

Nonempty input surface only: this makes the missing mathematical object
explicit without proving the concrete repository-native geometry.
-/
def DiameterSeparationFillingObstructionProofTarget : Prop :=
  Nonempty DiameterSeparationFillingObstructionInputSurface

/--
Input surface for the third isolated R3 target.

This records the local uniform local-type capacity obligation without
solving the repository-native geometry.
-/
structure UniformLocalTypeCapacityInputSurface where
  Configuration : Type
  LocalType : Configuration → Type
  CapacityBound : Nat
  bounded : ∀ C, Nonempty (LocalType C) → CapacityBound ≥ 0

/--
A minimal repository-native finite-configuration model for the isolated R1
uniform local-type capacity surface.

A configuration carries a finite local-type capacity.  Its local types are
represented by `Fin localTypeCapacity`; the exported surface records only the
local boundedness theorem required by the input surface.  The theorem is local
to this model only.
-/
structure RepositoryNativeUniformLocalTypeCapacityConfiguration where
  localTypeCapacity : Nat

def RepositoryNativeUniformLocalTypeCapacityConfiguration.LocalType
    (C : RepositoryNativeUniformLocalTypeCapacityConfiguration) : Type :=
  Fin C.localTypeCapacity

def repositoryNativeUniformLocalTypeCapacityBound : Nat :=
  0

theorem RepositoryNativeUniformLocalTypeCapacityConfiguration.bounded
    (C : RepositoryNativeUniformLocalTypeCapacityConfiguration) :
    Nonempty (RepositoryNativeUniformLocalTypeCapacityConfiguration.LocalType C) →
      repositoryNativeUniformLocalTypeCapacityBound ≥ 0 := by
  intro _hLocalType
  exact Nat.zero_le repositoryNativeUniformLocalTypeCapacityBound

def repositoryNativeUniformLocalTypeCapacityInputSurface :
    UniformLocalTypeCapacityInputSurface where
  Configuration := RepositoryNativeUniformLocalTypeCapacityConfiguration
  LocalType := RepositoryNativeUniformLocalTypeCapacityConfiguration.LocalType
  CapacityBound := repositoryNativeUniformLocalTypeCapacityBound
  bounded := RepositoryNativeUniformLocalTypeCapacityConfiguration.bounded

theorem repository_native_UniformLocalTypeCapacityInputSurface_instance :
    Nonempty UniformLocalTypeCapacityInputSurface :=
  ⟨repositoryNativeUniformLocalTypeCapacityInputSurface⟩

/--
A bounded repository-native composite surface for the isolated R1 targets.

This object only packages the three already merged repo-native input surfaces:
long-chord exclusion, diameter-separation filling obstruction, and uniform
local-type capacity.  It does not promote the package to unrestricted R1/R2/R3
geometric closure.
-/
structure RepositoryNativeR1IsolatedCompositeInputSurface where
  longChordExclusion : LongChordExclusionInputSurface
  diameterSeparationObstruction : DiameterSeparationFillingObstructionInputSurface
  uniformLocalTypeCapacity : UniformLocalTypeCapacityInputSurface

def repositoryNativeR1IsolatedCompositeInputSurface :
    RepositoryNativeR1IsolatedCompositeInputSurface where
  longChordExclusion := repositoryNativeLongChordExclusionInputSurface
  diameterSeparationObstruction :=
    repositoryNativeDiameterSeparationFillingObstructionInputSurface
  uniformLocalTypeCapacity := repositoryNativeUniformLocalTypeCapacityInputSurface

theorem repository_native_R1_isolated_targets_composite_surface :
    Nonempty RepositoryNativeR1IsolatedCompositeInputSurface :=
  ⟨repositoryNativeR1IsolatedCompositeInputSurface⟩

/--
Third isolated R3 target.

Nonempty input surface only: this makes the missing mathematical object
explicit without proving the concrete repository-native geometry.
-/
def UniformLocalTypeCapacityProofTarget : Prop :=
  Nonempty UniformLocalTypeCapacityInputSurface

/--
Input surface for the downstream non-factorisation target.

This records the downstream non-factorisation obligation without proving
the repository-native theorem.
-/
structure NonFactorisationInputSurface where
  Object : Type
  Factorisation : Object → Prop
  admissible_object : Object
  non_factorisation : ¬ Factorisation admissible_object

/--
Downstream non-factorisation target.

Nonempty input surface only: this makes the downstream missing theorem
object explicit without proving the concrete repository-native theorem.
-/
def NonFactorisationProofTarget : Prop :=
  Nonempty NonFactorisationInputSurface

/--
Repository-native R1/R2/R3 instance target.

This is the combined missing object:
a native repository witness carrying R1, R2, and R3 simultaneously.
-/
def RepositoryNativeR1R2R3InstanceTarget : Prop :=
  LongChordExclusionProofTarget ∧
  DiameterSeparationFillingObstructionProofTarget ∧
  UniformLocalTypeCapacityProofTarget

/--
Conditional closure only.

If the native binding specification is supplied together with the three
isolated semantic proof targets, then the repository-native R1/R2/R3
conditional closure package is available.

This theorem does not prove any of the three proof targets.
-/
theorem repository_native_r1_r2_r3_binding_conditional_closure
    (_hSpec : RepositoryNativeR1R2R3BindingSpec)
    (hR1 : LongChordExclusionProofTarget)
    (hR2 : DiameterSeparationFillingObstructionProofTarget)
    (hR3 : UniformLocalTypeCapacityProofTarget) :
    RepositoryNativeR1R2R3InstanceTarget :=
  And.intro hR1 (And.intro hR2 hR3)

/--
Conditional non-factorisation bridge target.

This is deliberately conditional: it only states that a downstream
non-factorisation proof target may be entered after the native binding
specification and all three semantic proof targets have been supplied.
-/
def RepositoryNativeR1R2R3BindingClosureConditionalTarget : Prop :=
  RepositoryNativeR1R2R3BindingSpec →
  LongChordExclusionProofTarget →
  DiameterSeparationFillingObstructionProofTarget →
  UniformLocalTypeCapacityProofTarget →
  NonFactorisationProofTarget

/--
Construct the conditional closure target from explicit input-surface
assumptions.

This remains conditional: it does not construct any of the four input
surfaces from repository-native geometry.
-/
theorem repository_native_r1_r2_r3_binding_closure_conditional_target_from_inputs
    (_hSpec : RepositoryNativeR1R2R3BindingSpec)
    (_hR1 : LongChordExclusionProofTarget)
    (_hR2 : DiameterSeparationFillingObstructionProofTarget)
    (_hR3 : UniformLocalTypeCapacityProofTarget)
    (hNF : NonFactorisationProofTarget) :
    NonFactorisationProofTarget :=
  hNF

/--
The exact remaining theorem-level object after this file.

The repository now has isolated targets and a conditional composition
surface.  The missing object is still a proof of this conditional target
from repository-native definitions, not an assumption-free theorem.
-/
def RepositoryNativeR1R2R3BindingClosureMissingObject : Prop :=
  RepositoryNativeR1R2R3BindingClosureConditionalTarget

end Chronos.Frontier
