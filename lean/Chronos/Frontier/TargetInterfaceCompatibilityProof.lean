import Chronos.Frontier.PackageCompatibilityProof

namespace Chronos
namespace Frontier

/--
Target-interface compatibility proof-obligation surface.

Status:
  PROOF_OBLIGATION_SURFACE_ONLY_NO_TARGET_INTERFACE_COMPATIBILITY_PROOF

This records the next admissible proof-obligation slot after the package
compatibility proof-obligation surface.

It does not prove target-interface compatibility and does not close the
concrete analytic Einstein-matter estimate package.
-/
structure TargetInterfaceCompatibilityProofSurfaceData where
  packageCompatibilityData : PackageCompatibilityProofSurfaceData
  targetInterface : Type
  packageOutputInterface : Type
  einsteinMatterTarget : Type
  analyticTargetStatement : Type

structure TargetInterfaceCompatibilityProofSurfaceObligations where
  packageCompatibilityAvailable : Prop
  targetInterfaceDefined : Prop
  packageOutputInterfaceDefined : Prop
  packageOutputMatchesTargetInput : Prop
  einsteinMatterTargetDefined : Prop
  analyticTargetStatementMatches : Prop
  targetConclusionCompatible : Prop

def TargetInterfaceCompatibilityProofSurfaceObligation
    (_D : TargetInterfaceCompatibilityProofSurfaceData) : Prop :=
  True

/--
Proof-obligation surface only.

If the package compatibility input, target interface, package-output match,
Einstein-matter target, analytic target statement, and target conclusion
compatibility are supplied, the target-interface compatibility obligation slot
is recorded.

The analytic proof of those supplied ingredients is not provided here.
-/
theorem TargetInterfaceCompatibilityProofSurface
    (D : TargetInterfaceCompatibilityProofSurfaceData)
    (H : TargetInterfaceCompatibilityProofSurfaceObligations)
    (_h_package : H.packageCompatibilityAvailable)
    (_h_target : H.targetInterfaceDefined)
    (_h_output : H.packageOutputInterfaceDefined)
    (_h_match : H.packageOutputMatchesTargetInput)
    (_h_em_target : H.einsteinMatterTargetDefined)
    (_h_statement : H.analyticTargetStatementMatches)
    (_h_conclusion : H.targetConclusionCompatible) :
    TargetInterfaceCompatibilityProofSurfaceObligation D := by
  trivial

def TargetInterfaceCompatibilityProofSurfaceStatus : String :=
  "PROOF_OBLIGATION_SURFACE_ONLY_NO_TARGET_INTERFACE_COMPATIBILITY_PROOF"

def TargetInterfaceCompatibilityProofSurfacePreviousObject : String :=
  "PACKAGE_COMPATIBILITY_PROOF"

def TargetInterfaceCompatibilityProofSurfaceNextAdmissibleObject : String :=
  "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF"

end Frontier
end Chronos
