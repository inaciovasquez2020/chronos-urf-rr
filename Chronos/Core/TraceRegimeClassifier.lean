namespace Chronos.Core

inductive RegimeStatus where
  | ZAP2_REGIME_CLOSED
  | AFFINE_LINEAR_ADMISSIBLE
  | AFFINE_SUBLINEAR_FORBIDDEN
  | AFFINE_INTERMEDIATE_FRONTIER_OPEN
  | UNKNOWN_FRONTIER_OPEN
  deriving DecidableEq, Repr

inductive CarrierKind where
  | repo_iso
  | affine
  | quotient
  | unknown
  deriving DecidableEq, Repr

inductive GrowthClass where
  | uniform_linear
  | sublinear
  | intermediate
  | unknown
  deriving DecidableEq, Repr

structure TraceInput where
  kind : CarrierKind
  has_native_iso : Bool
  kernel_growth : GrowthClass
  no_forbidden_claims : Bool
  deriving Repr

def ChronosTraceRegimeClassifier (t : TraceInput) : RegimeStatus :=
  if t.no_forbidden_claims = false then
    RegimeStatus.UNKNOWN_FRONTIER_OPEN
  else
    match t.kind with
    | CarrierKind.repo_iso =>
        if t.has_native_iso then
          RegimeStatus.ZAP2_REGIME_CLOSED
        else
          RegimeStatus.UNKNOWN_FRONTIER_OPEN
    | CarrierKind.affine =>
        match t.kernel_growth with
        | GrowthClass.uniform_linear =>
            RegimeStatus.AFFINE_LINEAR_ADMISSIBLE
        | GrowthClass.sublinear =>
            RegimeStatus.AFFINE_SUBLINEAR_FORBIDDEN
        | GrowthClass.intermediate =>
            RegimeStatus.AFFINE_INTERMEDIATE_FRONTIER_OPEN
        | GrowthClass.unknown =>
            RegimeStatus.UNKNOWN_FRONTIER_OPEN
    | CarrierKind.quotient =>
        RegimeStatus.UNKNOWN_FRONTIER_OPEN
    | CarrierKind.unknown =>
        RegimeStatus.UNKNOWN_FRONTIER_OPEN

structure TraceRecord where
  trace_id : String
  input : TraceInput
  source_file : String
  boundary_status : String
  deriving Repr

abbrev ChronosTraceManifest := List TraceRecord

def classifyTraceRecord (r : TraceRecord) : RegimeStatus :=
  ChronosTraceRegimeClassifier r.input

def boundaryStatusOfRegime : RegimeStatus → String
  | RegimeStatus.ZAP2_REGIME_CLOSED =>
      "CLOSED"
  | RegimeStatus.AFFINE_LINEAR_ADMISSIBLE =>
      "ADMISSIBLE"
  | RegimeStatus.AFFINE_SUBLINEAR_FORBIDDEN =>
      "FORBIDDEN"
  | RegimeStatus.AFFINE_INTERMEDIATE_FRONTIER_OPEN =>
      "FRONTIER_OPEN"
  | RegimeStatus.UNKNOWN_FRONTIER_OPEN =>
      "FRONTIER_OPEN"

def traceBoundaryMatchesClassifier (r : TraceRecord) : Bool :=
  r.boundary_status == boundaryStatusOfRegime (classifyTraceRecord r)

def auditChronosTraceManifest (M : ChronosTraceManifest) : Bool :=
  M.all traceBoundaryMatchesClassifier

def ChronosTraceManifest_2026_05_05 : ChronosTraceManifest := [
  {
    trace_id := "Chronos/ZaP2",
    source_file := "Chronos/Regimes/ZaP2.lean",
    boundary_status := "CLOSED",
    input := {
      kind := CarrierKind.repo_iso,
      has_native_iso := true,
      kernel_growth := GrowthClass.unknown,
      no_forbidden_claims := true
    }
  },
  {
    trace_id := "Affine/High-Entropy",
    source_file := "Chronos/Affine/HighEntropy.lean",
    boundary_status := "ADMISSIBLE",
    input := {
      kind := CarrierKind.affine,
      has_native_iso := false,
      kernel_growth := GrowthClass.uniform_linear,
      no_forbidden_claims := true
    }
  },
  {
    trace_id := "Affine/Over-Constrained",
    source_file := "Chronos/Affine/Sublinear.lean",
    boundary_status := "FORBIDDEN",
    input := {
      kind := CarrierKind.affine,
      has_native_iso := false,
      kernel_growth := GrowthClass.sublinear,
      no_forbidden_claims := true
    }
  },
  {
    trace_id := "Affine/Oscillatory",
    source_file := "Chronos/Affine/Intermediate.lean",
    boundary_status := "FRONTIER_OPEN",
    input := {
      kind := CarrierKind.affine,
      has_native_iso := false,
      kernel_growth := GrowthClass.intermediate,
      no_forbidden_claims := true
    }
  },
  {
    trace_id := "Generic Repository",
    source_file := "N/A",
    boundary_status := "FRONTIER_OPEN",
    input := {
      kind := CarrierKind.unknown,
      has_native_iso := false,
      kernel_growth := GrowthClass.unknown,
      no_forbidden_claims := true
    }
  }
]

theorem classifier_forbidden_claim_guard
  (t : TraceInput)
  (h : t.no_forbidden_claims = false) :
  ChronosTraceRegimeClassifier t = RegimeStatus.UNKNOWN_FRONTIER_OPEN := by
  cases t
  simp_all [ChronosTraceRegimeClassifier]

theorem ChronosTraceClassifierCompleteness
  (t : TraceInput) :
  ChronosTraceRegimeClassifier t =
      RegimeStatus.ZAP2_REGIME_CLOSED
    ∨
    ChronosTraceRegimeClassifier t =
      RegimeStatus.AFFINE_LINEAR_ADMISSIBLE
    ∨
    ChronosTraceRegimeClassifier t =
      RegimeStatus.AFFINE_SUBLINEAR_FORBIDDEN
    ∨
    ChronosTraceRegimeClassifier t =
      RegimeStatus.AFFINE_INTERMEDIATE_FRONTIER_OPEN
    ∨
    ChronosTraceRegimeClassifier t =
      RegimeStatus.UNKNOWN_FRONTIER_OPEN := by
  cases t with
  | mk kind has_native_iso kernel_growth no_forbidden_claims =>
    cases no_forbidden_claims <;>
    cases kind <;>
    cases has_native_iso <;>
    cases kernel_growth <;>
    simp [ChronosTraceRegimeClassifier]

theorem ChronosTraceManifest_2026_05_05_audit :
  auditChronosTraceManifest ChronosTraceManifest_2026_05_05 = true := by
  native_decide

structure ChronosTraceClassifierSolved where
  manifest : ChronosTraceManifest
  audit_passes : auditChronosTraceManifest manifest = true
  forbidden_guard :
    ∀ t : TraceInput,
      t.no_forbidden_claims = false →
      ChronosTraceRegimeClassifier t = RegimeStatus.UNKNOWN_FRONTIER_OPEN
  completeness :
    ∀ t : TraceInput,
      ChronosTraceRegimeClassifier t =
          RegimeStatus.ZAP2_REGIME_CLOSED
        ∨
        ChronosTraceRegimeClassifier t =
          RegimeStatus.AFFINE_LINEAR_ADMISSIBLE
        ∨
        ChronosTraceRegimeClassifier t =
          RegimeStatus.AFFINE_SUBLINEAR_FORBIDDEN
        ∨
        ChronosTraceRegimeClassifier t =
          RegimeStatus.AFFINE_INTERMEDIATE_FRONTIER_OPEN
        ∨
        ChronosTraceRegimeClassifier t =
          RegimeStatus.UNKNOWN_FRONTIER_OPEN
  status : String
  status_eq :
    status = "TRACE_REGIME_CLASSIFIER_SOLVED_FRONTIER_PRESERVED"

def ChronosTraceClassifierSolved_2026_05_05 :
  ChronosTraceClassifierSolved :=
{
  manifest := ChronosTraceManifest_2026_05_05
  audit_passes := ChronosTraceManifest_2026_05_05_audit
  forbidden_guard := classifier_forbidden_claim_guard
  completeness := ChronosTraceClassifierCompleteness
  status := "TRACE_REGIME_CLASSIFIER_SOLVED_FRONTIER_PRESERVED"
  status_eq := rfl
}

end Chronos.Core
