import Oblivion.LocalityHolonomySeparation

/-!
# URF–Chronos finite-cycle decoder obstruction

This is a concrete instantiation of URF Core's exact reconstruction obstruction
(O(G) = O(H) but I(G) != I(H) implies no exact decoder) using Chronos's
already-proved finite-cycle separation theorem.

The observation invariance premise must be proved for any actual observer.
Chronos's LocalEquiv uses independent gauges on proper path windows and
thus does not by itself model graph-ball indistinguishability.
No fifth physical dimension, global geometry, or unrestricted locality claim
is derived here.
-/

namespace Oblivion

/-- A local-equivalence-invariant observation maps the existing
separation witness to equal observations but unequal global cycle holonomy. -/
theorem urf_chronos_observation_collision
    (n r : Nat) (hn : 3 ≤ n) (hr : 2 * r + 1 < n)
    {Y : Type} (observe : LabeledCFI → Y)
    (hobs : ∀ G H : LabeledCFI,
      LocalEquiv n r G H → observe G = observe H) :
    ∃ G H : LabeledCFI,
      G.localSummary = n ∧ H.localSummary = n ∧
      observe G = observe H ∧ PhiH n G ≠ PhiH n H := by
  obtain ⟨G, H, hlocal, hneq⟩ :=
    locality_holonomy_separation n r hn hr
  exact ⟨G, H, hlocal.1, hlocal.2.1, hobs G H hlocal, hneq⟩

/-- No decoder can reconstruct the global cycle XOR from an observation
which is invariant under the stated independent proper-path gauges.
The decoder is required to be correct on every configuration with
localSummary = n. -/
theorem urf_chronos_no_exact_holonomy_decoder
    (n r : Nat) (hn : 3 ≤ n) (hr : 2 * r + 1 < n)
    {Y : Type} (observe : LabeledCFI → Y)
    (hobs : ∀ G H : LabeledCFI,
      LocalEquiv n r G H → observe G = observe H) :
    ¬ ∃ decode : Y → Bool,
        ∀ F : LabeledCFI, F.localSummary = n →
          decode (observe F) = PhiH n F := by
  intro hdecoder
  obtain ⟨decode, hcorrect⟩ := hdecoder
  obtain ⟨G, H, hg, hh, heq, hneq⟩ :=
    urf_chronos_observation_collision n r hn hr observe hobs
  apply hneq
  calc
    PhiH n G = decode (observe G) := (hcorrect G hg).symm
    _ = decode (observe H) := congrArg decode heq
    _ = PhiH n H := hcorrect H hh

#print axioms Oblivion.urf_chronos_observation_collision
#print axioms Oblivion.urf_chronos_no_exact_holonomy_decoder

end Oblivion
