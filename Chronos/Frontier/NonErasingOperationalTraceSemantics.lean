import Chronos.Frontier.ErasingCanonicalRepositoryNativeClosure
import Chronos.Frontier.OperationalTraceConstructorPreservation

namespace Chronos.Frontier.NonErasingOperationalTraceSemantics

open Chronos.Frontier.OperationalTraceConstructorPreservation

inductive OperationalTraceConstructorTag where
  | native
  | lift
  | relabel
deriving DecidableEq

structure NonErasingOperationalTraceSemantics
    (C : RepositoryNativeChronosCarrier) (b lam : Nat) where
  trace : OperationalTraceSyntax C b lam
  tag : OperationalTraceConstructorTag

def nativeSemantics
    {C : RepositoryNativeChronosCarrier} {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    NonErasingOperationalTraceSemantics C b lam :=
  ⟨x, OperationalTraceConstructorTag.native⟩

def liftSemantics
    {C : RepositoryNativeChronosCarrier} {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    NonErasingOperationalTraceSemantics C b lam :=
  ⟨OperationalTraceSyntax.lift x, OperationalTraceConstructorTag.lift⟩

def relabelSemantics
    {C : RepositoryNativeChronosCarrier} {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    NonErasingOperationalTraceSemantics C b lam :=
  ⟨OperationalTraceSyntax.relabel x, OperationalTraceConstructorTag.relabel⟩

def ForgetsToErasingSemantics
    {C : RepositoryNativeChronosCarrier} {b lam : Nat}
    (s : NonErasingOperationalTraceSemantics C b lam) :
    OperationalTraceSyntax C b lam :=
  s.trace

def PreservesLiftNonErasing
    {C : RepositoryNativeChronosCarrier} {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) : Prop :=
  (liftSemantics x).tag = OperationalTraceConstructorTag.lift ∧
  SemanticallyEquivalent (ForgetsToErasingSemantics (liftSemantics x)) x

def PreservesRelabelNonErasing
    {C : RepositoryNativeChronosCarrier} {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) : Prop :=
  (relabelSemantics x).tag = OperationalTraceConstructorTag.relabel ∧
  SemanticallyEquivalent (ForgetsToErasingSemantics (relabelSemantics x)) x

theorem lift_non_erasing_semantics_preserved
    {C : RepositoryNativeChronosCarrier} {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    PreservesLiftNonErasing x := by
  constructor
  · rfl
  · exact
      (canonical_repository_native_semantics_preserves_erasing_constructors
        canonical_repository_native_semantics x).1

theorem relabel_non_erasing_semantics_preserved
    {C : RepositoryNativeChronosCarrier} {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    PreservesRelabelNonErasing x := by
  constructor
  · rfl
  · exact
      (canonical_repository_native_semantics_preserves_erasing_constructors
        canonical_repository_native_semantics x).2

def NonErasingConstructorPreservation : Prop :=
  ∀ {C : RepositoryNativeChronosCarrier} {b lam : Nat}
      (x : OperationalTraceSyntax C b lam),
    PreservesLiftNonErasing x ∧ PreservesRelabelNonErasing x

theorem non_erasing_constructor_preservation :
    NonErasingConstructorPreservation := by
  intro C b lam x
  exact ⟨lift_non_erasing_semantics_preserved x,
    relabel_non_erasing_semantics_preserved x⟩

end Chronos.Frontier.NonErasingOperationalTraceSemantics
