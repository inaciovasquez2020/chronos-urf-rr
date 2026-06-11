import Chronos.Frontier.R1R2R3PromotionProofTargetRegistry

namespace Chronos.Frontier

/--
Minimal R1 obstruction certificate.

Open object: records the obstruction to promoting the finite checked R1
long-chord certificate into the repository-native `R1PromotionProofTarget`.

This is not proved or eliminated here.
-/
def R1PromotionProofObstructionCertificate : Prop := True

/--
R1 counterexample-search harness target.

A concrete counterexample search must either find an obstruction witness or
produce an elimination certificate.  This file only records the target.
-/
def R1PromotionCounterexampleSearchHarnessTarget : Prop :=
  R1PromotionProofObstructionCertificate

/--
R1 obstruction elimination certificate.

This is the exact certificate needed to remove the R1 promotion obstruction.
-/
def R1PromotionProofObstructionEliminationCertificate : Prop :=
  R1PromotionProofObstructionCertificate → False

/--
R1 theorem-target reduction.

If the R1 obstruction is eliminated and a proof-reduction rule is supplied,
then the R1 promotion proof target follows.

This does not prove the reduction rule.
-/
def R1PromotionProofTargetReductionFromObstructionElimination : Prop :=
  R1PromotionProofObstructionEliminationCertificate →
  R1PromotionProofTarget

/--
Selected target remains open.

This marker records that R1 is the selected target and remains open until
the obstruction is eliminated and the reduction is supplied.
-/
def R1PromotionSelectedTargetOpen : Prop :=
  R1PromotionProofTarget

def R1PromotionSelectedTargetStatus : String := "OPEN"
def R1PromotionProofObstructionStatus : String := "OPEN"
def R1PromotionCounterexampleSearchHarnessStatus : String := "TARGET_ONLY"
def R1PromotionProofTargetReductionStatus : String := "OPEN"

end Chronos.Frontier
