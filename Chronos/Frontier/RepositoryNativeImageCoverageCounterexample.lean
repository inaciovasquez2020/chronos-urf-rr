import Chronos.Frontier.RepositoryNativeImageCoverageFrontier

namespace Chronos.Frontier.RepositoryNativeImageCoverageCounterexample

open Chronos.Frontier.RepositoryNativeImageCoverageFrontier
open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.RealChronosAdmissible

def zeroArityCarrierData : ChronosCarrierData :=
  {
    arity := 0
    stratum := 0
    index := 0
  }

theorem zero_arity_real_chronos_admissible :
    RealChronosAdmissiblePredicate
      ChronosRegistry ChronosTraceFamily zeroArityCarrierData := by
  exact registered_carrier_is_real_chronos_admissible
    ChronosRegistry ChronosTraceFamily zeroArityCarrierData trivial

theorem zero_arity_not_repository_native_image :
    ¬ RepositoryNativeImagePredicate zeroArityCarrierData := by
  intro h
  rcases h with ⟨C, hC⟩
  have hArity : C.arity = 0 := by
    have h := congrArg ChronosCarrierData.arity hC
    simpa [RepositoryNativeChronosCarrier.toChronosCarrierData,
      zeroArityCarrierData] using h
  have hZero : 0 < 0 := by
    simpa [hArity] using C.arity_pos
  exact (Nat.lt_irrefl 0) hZero

theorem not_missing_repository_native_image_coverage_theorem :
    ¬ MissingRepositoryNativeImageCoverageTheorem := by
  intro h
  exact zero_arity_not_repository_native_image
    (h zeroArityCarrierData zero_arity_real_chronos_admissible)

end Chronos.Frontier.RepositoryNativeImageCoverageCounterexample
