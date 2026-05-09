import Chronos.Frontier.NonErasingCanonicalRepositoryNativeClosure
import Chronos.Frontier.RepositoryNativeChronosCarrierBridge

namespace Chronos.Frontier.NonErasingRegSNFImageBridge

open Chronos.Frontier.NonErasingCanonicalRepositoryNativeClosure
open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.CarrierRegistryExhaustivenessBridge

def NonErasingRepositoryNativeRegSNFOnImage : Prop :=
  RepositoryNativeBranchNonErasingCanonical ∧
  RegSNF ChronosRegistry ChronosTraceFamily
    (fun D : ChronosCarrierData =>
      ∃ C : RepositoryNativeChronosCarrier,
        C.toChronosCarrierData = D)

theorem non_erasing_repository_native_reg_snf_on_image :
    NonErasingRepositoryNativeRegSNFOnImage := by
  constructor
  · exact repository_native_branch_non_erasing_canonical
  · exact repository_native_implies_reg_snf_on_image

end Chronos.Frontier.NonErasingRegSNFImageBridge
