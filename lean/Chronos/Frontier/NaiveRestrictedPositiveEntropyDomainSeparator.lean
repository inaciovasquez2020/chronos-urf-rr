import Chronos.Frontier.LatentTraceEntropyRoute

namespace Chronos

/--
A naive restricted positive-entropy construction is one where a nonempty
restricted domain still returns the already-refuted unrestricted witness type.
-/
def NaiveRestrictedPositiveEntropyDomainConstruction
    (lam : ℝ) : Prop :=
  ∃ (Domain : Type),
    Nonempty Domain ∧
      Nonempty (Domain → PositiveEntropyAdmissibleClassUniformWitness lam)

/--
The naive restricted-domain route is impossible: a nonempty domain together
with a map into unrestricted witnesses immediately reconstructs the refuted
unrestricted construction.
-/
theorem naiveRestrictedPositiveEntropyDomainConstruction_refuted
    (lam : ℝ) :
    ¬ NaiveRestrictedPositiveEntropyDomainConstruction lam := by
  intro h
  rcases h with ⟨Domain, hNonempty, hMap⟩
  rcases hNonempty with ⟨d⟩
  rcases hMap with ⟨mkWitness⟩
  exact positiveEntropyAdmissibleClassUniformWitnessConstruction_refuted lam
    ⟨mkWitness d⟩

end Chronos
