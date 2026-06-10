namespace Chronos.Frontier

inductive PredictiveDeficitMassRoute where
  | predictiveDeficitMassLaw
  | lowParameterDeficitMassModel
deriving DecidableEq, Repr

def lowParameterDeficitMassModelBound : Nat := 8

structure UniquePredictiveDeficitMassLawOrLowParameterDeficitMassModel where
  route : PredictiveDeficitMassRoute
  parameterCount : Nat
  holdoutGalaxyCount : Nat
  nonAccountingConstraint : Bool
  boundaryGuard : Bool
deriving Repr

def admissiblePredictiveDeficitMassTarget
    (M : UniquePredictiveDeficitMassLawOrLowParameterDeficitMassModel) : Prop :=
  M.nonAccountingConstraint = true ∧
  M.boundaryGuard = true ∧
  0 < M.holdoutGalaxyCount ∧
  (M.route = PredictiveDeficitMassRoute.predictiveDeficitMassLaw ∨
    M.parameterCount ≤ lowParameterDeficitMassModelBound)

theorem admissiblePredictiveDeficitMassTarget_has_boundary_guard
    {M : UniquePredictiveDeficitMassLawOrLowParameterDeficitMassModel}
    (h : admissiblePredictiveDeficitMassTarget M) :
    M.boundaryGuard = true :=
  h.2.1

theorem admissiblePredictiveDeficitMassTarget_has_nonaccounting_constraint
    {M : UniquePredictiveDeficitMassLawOrLowParameterDeficitMassModel}
    (h : admissiblePredictiveDeficitMassTarget M) :
    M.nonAccountingConstraint = true :=
  h.1

theorem admissiblePredictiveDeficitMassTarget_has_holdout
    {M : UniquePredictiveDeficitMassLawOrLowParameterDeficitMassModel}
    (h : admissiblePredictiveDeficitMassTarget M) :
    0 < M.holdoutGalaxyCount :=
  h.2.2.1

theorem lowParameterDeficitMassModel_target_witness :
    ∃ M : UniquePredictiveDeficitMassLawOrLowParameterDeficitMassModel,
      admissiblePredictiveDeficitMassTarget M := by
  refine ⟨
    { route := PredictiveDeficitMassRoute.lowParameterDeficitMassModel
      parameterCount := 0
      holdoutGalaxyCount := 1
      nonAccountingConstraint := true
      boundaryGuard := true },
    ?_⟩
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · decide
  · right
    decide

end Chronos.Frontier
