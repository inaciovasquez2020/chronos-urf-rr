import Chronos.Frontier.RepositoryNativeSemanticTrace

namespace Chronos.Frontier.RepositoryNativeTraceSyntax

open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.TraceEquivalentCardinality
open Chronos.Frontier.TraceEquivalentEquiv
open Chronos.Frontier.RepositoryNativeSemanticTrace

inductive RepositoryNativeTraceSyntax
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) : Type where
  | atom : Fin (repositoryNativeSemanticTraceSize C b lam) →
      RepositoryNativeTraceSyntax C b lam

def RepositoryNativeTraceSyntax.toSemantic
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat} :
    RepositoryNativeTraceSyntax C b lam →
      RepositoryNativeSemanticTrace C b lam
  | RepositoryNativeTraceSyntax.atom idx => idx

def RepositoryNativeTraceSyntax.ofSemantic
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat} :
    RepositoryNativeSemanticTrace C b lam →
      RepositoryNativeTraceSyntax C b lam :=
  fun idx => RepositoryNativeTraceSyntax.atom idx

def repository_native_trace_syntax_equiv_semantic
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) :
    RepositoryNativeTraceSyntax C b lam ≃
      RepositoryNativeSemanticTrace C b lam where
  toFun := RepositoryNativeTraceSyntax.toSemantic
  invFun := RepositoryNativeTraceSyntax.ofSemantic
  left_inv := by
    intro x
    cases x
    rfl
  right_inv := by
    intro x
    rfl

def SyntaxTraceEquivalent
    (C : RepositoryNativeChronosCarrier)
    (D : ChronosCarrierData) : Prop :=
  ∀ b lam : Nat,
    Nonempty (RepositoryNativeTraceSyntax C b lam ≃ ChronosTrace D b lam)

theorem repository_native_syntax_trace_equivalent
    (C : RepositoryNativeChronosCarrier) :
    SyntaxTraceEquivalent C C.toChronosCarrierData := by
  intro b lam
  exact ⟨
    (repository_native_trace_syntax_equiv_semantic C b lam).trans
      (Classical.choice
        (repository_native_semantic_trace_equivalent C b lam))
  ⟩

theorem syntax_trace_equivalent_implies_semantic_trace_equivalent
    (C : RepositoryNativeChronosCarrier)
    (D : ChronosCarrierData)
    (h : SyntaxTraceEquivalent C D) :
    SemanticTraceEquivalent C D := by
  intro b lam
  rcases h b lam with ⟨e⟩
  exact ⟨(repository_native_trace_syntax_equiv_semantic C b lam).symm.trans e⟩

theorem repository_native_bridge_with_syntax_trace_equivalence
    (C : RepositoryNativeChronosCarrier) :
    ∃ D : ChronosCarrierData,
      IntendedChronosCarrier D ∧ SyntaxTraceEquivalent C D := by
  refine ⟨C.toChronosCarrierData, ?_, ?_⟩
  · exact repository_native_to_intended C
  · exact repository_native_syntax_trace_equivalent C

end Chronos.Frontier.RepositoryNativeTraceSyntax
