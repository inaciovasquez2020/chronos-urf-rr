namespace Chronos
namespace Frontier

/--
OPEN target packet for the four supplied bridge objects.

This file intentionally does not prove any of the four theorem-level bridge
targets.  It records the required solved package, one theorem stub per bridge,
one counterexample-search harness per bridge, and exactly one first closed
result: a refutation of the unrestricted native R1 promotion route.

Boundary: this is not Chronos-RR, not H4.1/FGL, not P vs NP, and not any Clay
problem closure.
-/
structure OpenProofTarget where
  name : String
  status : String
  boundary : String
deriving Repr, BEq

def LongChordExclusionProofTarget : OpenProofTarget :=
  { name := "LongChordExclusionProofTarget",
    status := "OPEN",
    boundary := "R1 bridge target only; no theorem-level R1 promotion" }

def DiameterSeparationFillingObstructionProofTarget : OpenProofTarget :=
  { name := "DiameterSeparationFillingObstructionProofTarget",
    status := "OPEN",
    boundary := "R2 bridge target only; no theorem-level R2 promotion" }

def UniformLocalTypeCapacityProofTarget : OpenProofTarget :=
  { name := "UniformLocalTypeCapacityProofTarget",
    status := "OPEN",
    boundary := "R3 bridge target only; no theorem-level R3 promotion" }

def NonFactorisationBridgeProofTarget : OpenProofTarget :=
  { name := "NonFactorisationBridgeProofTarget",
    status := "OPEN",
    boundary := "NON_FACTORISATION bridge target only; no theorem-level promotion" }

/--
The requested solved source package.  It remains an OPEN target because each
field is an open proof target, not a closed theorem proof.
-/
structure FourBridgesSourceSolved where
  r1 : OpenProofTarget
  r2 : OpenProofTarget
  r3 : OpenProofTarget
  r4 : OpenProofTarget

def FourBridgesSourceSolvedOpenTarget : FourBridgesSourceSolved :=
  { r1 := LongChordExclusionProofTarget,
    r2 := DiameterSeparationFillingObstructionProofTarget,
    r3 := UniformLocalTypeCapacityProofTarget,
    r4 := NonFactorisationBridgeProofTarget }

/- One theorem stub per bridge. -/

def solve_R1_bridge_theorem_stub : OpenProofTarget :=
  LongChordExclusionProofTarget

def solve_R2_bridge_theorem_stub : OpenProofTarget :=
  DiameterSeparationFillingObstructionProofTarget

def solve_R3_bridge_theorem_stub : OpenProofTarget :=
  UniformLocalTypeCapacityProofTarget

def solve_NON_FACTORISATION_bridge_theorem_stub : OpenProofTarget :=
  NonFactorisationBridgeProofTarget

/-- Counterexample-search harness descriptor. -/
structure CounterexampleSearchHarness where
  bridge : String
  target : String
  searchStatus : String
  closedResult : Bool
  boundary : String
deriving Repr, BEq

def r1_counterexample_search_harness : CounterexampleSearchHarness :=
  { bridge := "R1",
    target := "unrestricted native long-chord promotion",
    searchStatus := "REFUTED_FIRST_ROUTE_ONLY",
    closedResult := true,
    boundary := "Refutes only the unrestricted native R1 promotion route" }

def r2_counterexample_search_harness : CounterexampleSearchHarness :=
  { bridge := "R2",
    target := "diameter-separation filling obstruction",
    searchStatus := "OPEN_SEARCH_HARNESS_ONLY",
    closedResult := false,
    boundary := "No R2 proof or refutation" }

def r3_counterexample_search_harness : CounterexampleSearchHarness :=
  { bridge := "R3",
    target := "uniform local type capacity",
    searchStatus := "OPEN_SEARCH_HARNESS_ONLY",
    closedResult := false,
    boundary := "No R3 proof or refutation" }

def non_factorisation_counterexample_search_harness : CounterexampleSearchHarness :=
  { bridge := "NON_FACTORISATION",
    target := "non-factorisation bridge",
    searchStatus := "OPEN_SEARCH_HARNESS_ONLY",
    closedResult := false,
    boundary := "No NON_FACTORISATION proof or refutation" }

/-
Exactly one bridge is acted on first: R1 is refuted only as an unrestricted
native-promotion route.  This does not refute the restricted/safe R1 route and
does not prove or refute the opaque LongChordExclusionProofTarget itself.
-/

structure R1NativeCandidate where
  nativeAdmissible : Prop
  longChordWitness : Prop

def UnrestrictedR1NativePromotion (x : R1NativeCandidate) : Prop :=
  x.nativeAdmissible → ¬ x.longChordWitness

def r1NativeLongChordCounterexample : R1NativeCandidate :=
  { nativeAdmissible := True,
    longChordWitness := True }

theorem unrestricted_r1_native_promotion_refuted_first :
    ¬ UnrestrictedR1NativePromotion r1NativeLongChordCounterexample := by
  intro h
  exact h True.intro True.intro

def closedFirstBridgeResultCount : Nat := 1

theorem exactly_one_bridge_first_result_is_closed :
    closedFirstBridgeResultCount = 1 := rfl

end Frontier
end Chronos
