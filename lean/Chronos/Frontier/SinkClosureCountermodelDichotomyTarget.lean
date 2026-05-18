import Chronos.Frontier.FiniteSupportToAdmissibleDomainLiftTarget

namespace Chronos
namespace Frontier

/--
Abstract resolution problem for remaining URF sinks.

Each sink has exactly two admissible exits:
closure under named hypotheses, or a countermodel certificate.
-/
structure SinkResolutionProblem where
  Sink : Type
  closureCertificate : Sink → Prop
  countermodelCertificate : Sink → Prop

def SinkResolved
    (P : SinkResolutionProblem)
    (s : P.Sink) : Prop :=
  P.closureCertificate s ∨ P.countermodelCertificate s

def CountermodelOrClosureDichotomyTarget
    (P : SinkResolutionProblem) : Prop :=
  ∀ s : P.Sink, SinkResolved P s

def CountermodelOrClosureDichotomyFailure
    (P : SinkResolutionProblem) : Prop :=
  ∃ s : P.Sink, ¬ SinkResolved P s

theorem closure_certificate_resolves_sink
    (P : SinkResolutionProblem)
    (s : P.Sink)
    (h : P.closureCertificate s) :
    SinkResolved P s := by
  exact Or.inl h

theorem countermodel_certificate_resolves_sink
    (P : SinkResolutionProblem)
    (s : P.Sink)
    (h : P.countermodelCertificate s) :
    SinkResolved P s := by
  exact Or.inr h

theorem unresolved_sink_excludes_dichotomy
    (P : SinkResolutionProblem)
    (hFail : CountermodelOrClosureDichotomyFailure P) :
    ¬ CountermodelOrClosureDichotomyTarget P := by
  intro hTarget
  rcases hFail with ⟨s, hs⟩
  exact hs (hTarget s)

def SinkClosureCountermodelDichotomyTargetStatus : String :=
  "OPEN_DICHOTOMY_TARGET_SURFACE_ONLY"

def SinkClosureCountermodelDichotomyTargetBoundary : String :=
  "Does not prove closure or countermodel existence for any remaining sink."

end Frontier
end Chronos
