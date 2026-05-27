import Chronos.Frontier.FiniteRegisteredHyperbolicNaturalAdmissibilityCertificate

namespace Chronos
namespace Frontier

open FiniteRegisteredHyperbolicRateThickAssembly

noncomputable section

/--
Registry-derived object count.  This is intentionally read from the registry
arity rather than hand-set inside the computable target.
-/
def derivedFiniteRegisteredHyperbolicObjectCount
    {n : Nat}
    (_R : FiniteHyperbolicRegistry n) : Nat :=
  n

/--
Registry-derived semantic rank-rate surrogate.

For this finite registered stack target, the rank-rate surrogate is tied to
the finite registry arity.
-/
def derivedFiniteRegisteredHyperbolicSemanticRankRate
    {n : Nat}
    (R : FiniteHyperbolicRegistry n) : Nat :=
  derivedFiniteRegisteredHyperbolicObjectCount R

/--
Registry-derived fiber-entropy-gap surrogate.

For this finite registered stack target, the fiber-gap surrogate is tied to
the same finite registry arity, making dominance definitional.
-/
def derivedFiniteRegisteredHyperbolicFiberEntropyGap
    {n : Nat}
    (R : FiniteHyperbolicRegistry n) : Nat :=
  derivedFiniteRegisteredHyperbolicObjectCount R

theorem derivedFiniteRegisteredHyperbolicRankEntropyDominance
    {n : Nat}
    (R : FiniteHyperbolicRegistry n) :
    derivedFiniteRegisteredHyperbolicSemanticRankRate R ≤
      derivedFiniteRegisteredHyperbolicFiberEntropyGap R := by
  rfl

def derivedFiniteRegisteredHyperbolicComputableTargetApplication :
    ComputableFiniteAdmissibleClass where
  objectCount :=
    derivedFiniteRegisteredHyperbolicObjectCount
      finiteRegisteredHyperbolicConcreteRegistry
  semanticRankRate :=
    derivedFiniteRegisteredHyperbolicSemanticRankRate
      finiteRegisteredHyperbolicConcreteRegistry
  fiberEntropyGap :=
    derivedFiniteRegisteredHyperbolicFiberEntropyGap
      finiteRegisteredHyperbolicConcreteRegistry
  admissible :=
    RegisteredHyperbolicUniversalFiberEntropyGap
      finiteRegisteredHyperbolicConcreteRegistry
  finite_support := by
    unfold derivedFiniteRegisteredHyperbolicObjectCount
    decide
  semantic_rank_rate_computable :=
    ⟨derivedFiniteRegisteredHyperbolicSemanticRankRate
      finiteRegisteredHyperbolicConcreteRegistry, rfl⟩
  fiber_entropy_gap_computable :=
    ⟨derivedFiniteRegisteredHyperbolicFiberEntropyGap
      finiteRegisteredHyperbolicConcreteRegistry, rfl⟩

def derivedFiniteRegisteredHyperbolicNaturalAdmissibilityCertificate :
    NaturalAdmissibilityDominanceCertificate
      derivedFiniteRegisteredHyperbolicComputableTargetApplication where
  admissible_witness :=
    finiteRegisteredHyperbolicConcreteUniversalGap
  rank_entropy_dominance := by
    change
      derivedFiniteRegisteredHyperbolicSemanticRankRate
        finiteRegisteredHyperbolicConcreteRegistry ≤
      derivedFiniteRegisteredHyperbolicFiberEntropyGap
        finiteRegisteredHyperbolicConcreteRegistry
    exact derivedFiniteRegisteredHyperbolicRankEntropyDominance
      finiteRegisteredHyperbolicConcreteRegistry

def derivedFiniteRegisteredHyperbolicCertificateFrontier :
    FirstTargetNaturalAdmissibilityCertificateFrontier
      derivedFiniteRegisteredHyperbolicComputableTargetApplication where
  certificate :=
    derivedFiniteRegisteredHyperbolicNaturalAdmissibilityCertificate

theorem derivedFiniteRegisteredHyperbolicTargetYieldsNaturalDominance :
    Nonempty NaturalDominanceAdmissibleComputableClass := by
  exact firstTargetNaturalAdmissibilityCertificateFrontier_to_natural
    derivedFiniteRegisteredHyperbolicCertificateFrontier

end

end Frontier
end Chronos
