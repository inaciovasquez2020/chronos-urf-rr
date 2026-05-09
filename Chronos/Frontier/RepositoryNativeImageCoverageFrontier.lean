import Chronos.Frontier.NonErasingRegSNFImageBridge
import Chronos.Frontier.RealChronosAdmissible

namespace Chronos.Frontier.RepositoryNativeImageCoverageFrontier

open Chronos.Frontier.NonErasingRegSNFImageBridge
open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.CarrierRegistryExhaustivenessBridge
open Chronos.Frontier.RealChronosAdmissible

def RepositoryNativeImagePredicate (D : ChronosCarrierData) : Prop :=
  ∃ C : RepositoryNativeChronosCarrier,
    C.toChronosCarrierData = D

def RepositoryNativeImageCovers
    (Admissible : ChronosCarrierData → Prop) : Prop :=
  ∀ D : ChronosCarrierData,
    Admissible D → RepositoryNativeImagePredicate D

def ConditionalUnrestrictedRegSNF
    (Admissible : ChronosCarrierData → Prop) : Prop :=
  RepositoryNativeBranchNonErasingCanonical ∧
  RepositoryNativeImageCovers Admissible →
  RegSNF ChronosRegistry ChronosTraceFamily Admissible

theorem repository_native_image_coverage_implies_reg_snf
    (Admissible : ChronosCarrierData → Prop)
    (hCover : RepositoryNativeImageCovers Admissible) :
    RegSNF ChronosRegistry ChronosTraceFamily Admissible := by
  intro D hD
  exact repository_native_implies_reg_snf_on_image D (hCover D hD)

theorem conditional_unrestricted_reg_snf
    (Admissible : ChronosCarrierData → Prop) :
    ConditionalUnrestrictedRegSNF Admissible := by
  intro h
  exact repository_native_image_coverage_implies_reg_snf Admissible h.2

def MissingRepositoryNativeImageCoverageTheorem : Prop :=
  RepositoryNativeImageCovers
    (RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily)

end Chronos.Frontier.RepositoryNativeImageCoverageFrontier
