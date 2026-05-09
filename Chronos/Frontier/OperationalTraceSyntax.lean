import Chronos.Frontier.RepositoryNativeTraceSyntax

namespace Chronos.Frontier.OperationalTraceSyntax

open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.RepositoryNativeSemanticTrace
open Chronos.Frontier.RepositoryNativeTraceSyntax

inductive OperationalTraceSyntax
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) : Type where
  | atom :
      RepositoryNativeTraceSyntax C b lam →
      OperationalTraceSyntax C b lam
  | lift :
      OperationalTraceSyntax C b lam →
      OperationalTraceSyntax C b lam
  | relabel :
      OperationalTraceSyntax C b lam →
      OperationalTraceSyntax C b lam

def normalize
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat} :
    OperationalTraceSyntax C b lam →
      RepositoryNativeTraceSyntax C b lam
  | OperationalTraceSyntax.atom x => x
  | OperationalTraceSyntax.lift x => normalize x
  | OperationalTraceSyntax.relabel x => normalize x

def atomOnly
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat} :
    RepositoryNativeTraceSyntax C b lam →
      OperationalTraceSyntax C b lam :=
  fun x => OperationalTraceSyntax.atom x

theorem normalize_atomOnly
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : RepositoryNativeTraceSyntax C b lam) :
    normalize (atomOnly x) = x := by
  rfl

def OperationalTraceNormalizes
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) : Prop :=
  ∀ x : OperationalTraceSyntax C b lam,
    ∃ y : RepositoryNativeTraceSyntax C b lam,
      normalize x = y

theorem operational_trace_normalizes
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) :
    OperationalTraceNormalizes C b lam := by
  intro x
  exact ⟨normalize x, rfl⟩

def AtomOnlyOperationalTrace
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) : Type :=
  RepositoryNativeTraceSyntax C b lam

def atom_only_operational_equiv_syntax
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) :
    AtomOnlyOperationalTrace C b lam ≃ RepositoryNativeTraceSyntax C b lam :=
  Equiv.refl _

theorem atom_only_operational_trace_equivalent
    (C : RepositoryNativeChronosCarrier) :
    SyntaxTraceEquivalent C C.toChronosCarrierData := by
  exact repository_native_syntax_trace_equivalent C

end Chronos.Frontier.OperationalTraceSyntax
