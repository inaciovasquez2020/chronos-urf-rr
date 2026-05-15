import Chronos.Frontier.UniversalFiberEntropyGapFromCountingAndMass

namespace Chronos
namespace Frontier
namespace CountingToMassUnderNonPropInvariant

open Chronos.Frontier.FiberLargeFromNonPropCore
open Chronos.Frontier.CountingFiberSeparationFromFiberLarge
open Chronos.Frontier.FiberMassBalanceFromNonPropInvariant
open Chronos.Frontier.UniversalFiberEntropyGapFromCountingAndMass

theorem fiberMassBalance_from_countingFiberSeparation_under_nonprop_invariant
    (I : NonPropFinalCarrierInvariant)
    (_hcount : CountingFiberSeparationFromNonProp I) :
    FiberMassBalanceFromNonProp I := by
  exact fiberMassBalance_from_nonprop_invariant I

theorem universalFiberEntropyGap_from_countingFiberSeparation_under_nonprop_invariant
    (I : NonPropFinalCarrierInvariant)
    (hcount : CountingFiberSeparationFromNonProp I) :
    UniversalFiberEntropyGapFromNonProp I := by
  exact
    universalFiberEntropyGap_from_counting_and_mass
      I
      hcount
      (fiberMassBalance_from_countingFiberSeparation_under_nonprop_invariant I hcount)

def FrontierStatus : String :=
  "COUNTING_TO_MASS_UNDER_NONPROP_INVARIANT_CLOSED_ONLY"

def Boundary : String :=
  "Typed repository bridge under NonPropFinalCarrierInvariant only; the counting premise is not information-exact and is not used to reconstruct entropyMass; no standalone CountingFiberSeparationToFiberMassBalance, unrestricted UniversalFiberEntropyGap, Chronos-RR, H4.1/FGL, P vs NP, or Clay closure"

end CountingToMassUnderNonPropInvariant
end Frontier
end Chronos
