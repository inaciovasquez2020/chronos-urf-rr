import Chronos.Frontier.R1R2R3FiniteDataPromotionAssumptions

namespace Chronos.Frontier

/--
R1 promotion proof target.

Open target: prove that the finite checked R1 long-chord certificate
promotes to the repository-native R1 proof target.
-/
def R1PromotionProofTarget : Prop :=
  R1FiniteDataToGeneralProofPromotionAssumption

/--
R2 promotion proof target.

Open target: prove that the finite checked R2 diameter/separation/filling
certificate promotes to the repository-native R2 proof target.
-/
def R2PromotionProofTarget : Prop :=
  R2FiniteDataToGeneralProofPromotionAssumption

/--
R3 promotion proof target.

Open target: prove that the finite checked R3 uniform local-type capacity
certificate promotes to the repository-native R3 proof target.
-/
def R3PromotionProofTarget : Prop :=
  R3FiniteDataToGeneralProofPromotionAssumption

/--
NON_FACTORISATION bridge proof target.

Open target: prove that a repository-native R1/R2/R3 instance implies the
downstream non-factorisation target.
-/
def NonFactorisationBridgeProofTarget : Prop :=
  NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance

/--
The four-object proof target registry.

This is a registry only.  It names the remaining proof targets but does
not prove any of them.
-/
def R1R2R3PromotionProofTargetRegistry : Prop :=
  R1PromotionProofTarget ∧
  R2PromotionProofTarget ∧
  R3PromotionProofTarget ∧
  NonFactorisationBridgeProofTarget

/--
Open-status marker for the proof target registry.

This intentionally aliases the full registry rather than proving it.
-/
def R1R2R3PromotionProofTargetRegistryOpen : Prop :=
  R1R2R3PromotionProofTargetRegistry

def R1PromotionProofTargetStatus : String := "OPEN"
def R2PromotionProofTargetStatus : String := "OPEN"
def R3PromotionProofTargetStatus : String := "OPEN"
def NonFactorisationBridgeProofTargetStatus : String := "OPEN"
def R1R2R3PromotionProofTargetRegistryStatus : String := "OPEN"

end Chronos.Frontier
