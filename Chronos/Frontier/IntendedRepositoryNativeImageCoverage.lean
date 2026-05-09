import Chronos.Frontier.RepositoryNativeImageCoverageCounterexample

namespace Chronos.Frontier.IntendedRepositoryNativeImageCoverage

open Chronos.Frontier.RepositoryNativeImageCoverageFrontier
open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.CarrierRegistryExhaustivenessBridge

theorem intended_chronos_carrier_image_coverage :
    RepositoryNativeImageCovers IntendedChronosCarrier := by
  intro D hD
  rcases D with ⟨arity, stratum, index⟩
  rcases hD with ⟨harity, hindex⟩
  refine ⟨
    {
      arity := arity
      stratum := stratum
      index := index
      arity_pos := harity
      index_le := hindex
    }, ?_⟩
  rfl

theorem intended_chronos_carrier_reg_snf_via_repository_native_image :
    RegSNF ChronosRegistry ChronosTraceFamily IntendedChronosCarrier :=
  repository_native_image_coverage_implies_reg_snf
    IntendedChronosCarrier
    intended_chronos_carrier_image_coverage

def IntendedRepositoryNativeImageCoverageClosed : Prop :=
  RepositoryNativeImageCovers IntendedChronosCarrier ∧
  RegSNF ChronosRegistry ChronosTraceFamily IntendedChronosCarrier

theorem intended_repository_native_image_coverage_closed :
    IntendedRepositoryNativeImageCoverageClosed := by
  exact ⟨intended_chronos_carrier_image_coverage,
    intended_chronos_carrier_reg_snf_via_repository_native_image⟩

end Chronos.Frontier.IntendedRepositoryNativeImageCoverage
