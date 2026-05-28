namespace Chronos.Frontier.GravityPullPushActualValueTest

structure GravityPullPushSample where
  pullMagnitude : Nat
  pushMagnitude : Nat
deriving Repr, DecidableEq

def pullResidual (x : GravityPullPushSample) : Nat :=
  x.pullMagnitude - x.pushMagnitude

def pushResidual (x : GravityPullPushSample) : Nat :=
  x.pushMagnitude - x.pullMagnitude

def totalMagnitude (x : GravityPullPushSample) : Nat :=
  x.pullMagnitude + x.pushMagnitude

def isBalanced (x : GravityPullPushSample) : Prop :=
  pullResidual x = 0 ∧ pushResidual x = 0

def isPullDominant (x : GravityPullPushSample) : Prop :=
  0 < pullResidual x

def isPushDominant (x : GravityPullPushSample) : Prop :=
  0 < pushResidual x

def emptyPullPushWitness : GravityPullPushSample :=
  { pullMagnitude := 0, pushMagnitude := 0 }

def balancedPullPushWitness : GravityPullPushSample :=
  { pullMagnitude := 7, pushMagnitude := 7 }

def pullDominantWitness : GravityPullPushSample :=
  { pullMagnitude := 13, pushMagnitude := 5 }

def pushDominantWitness : GravityPullPushSample :=
  { pullMagnitude := 4, pushMagnitude := 9 }

theorem empty_pull_push_actual_values :
    pullResidual emptyPullPushWitness = 0 ∧
    pushResidual emptyPullPushWitness = 0 ∧
    totalMagnitude emptyPullPushWitness = 0 ∧
    isBalanced emptyPullPushWitness := by
  simp [emptyPullPushWitness, pullResidual, pushResidual, totalMagnitude, isBalanced]

theorem balanced_pull_push_actual_values :
    pullResidual balancedPullPushWitness = 0 ∧
    pushResidual balancedPullPushWitness = 0 ∧
    totalMagnitude balancedPullPushWitness = 14 ∧
    isBalanced balancedPullPushWitness := by
  simp [balancedPullPushWitness, pullResidual, pushResidual, totalMagnitude, isBalanced]

theorem pull_dominant_actual_values :
    pullResidual pullDominantWitness = 8 ∧
    pushResidual pullDominantWitness = 0 ∧
    totalMagnitude pullDominantWitness = 18 ∧
    isPullDominant pullDominantWitness := by
  simp [pullDominantWitness, pullResidual, pushResidual, totalMagnitude, isPullDominant]

theorem push_dominant_actual_values :
    pullResidual pushDominantWitness = 0 ∧
    pushResidual pushDominantWitness = 5 ∧
    totalMagnitude pushDominantWitness = 13 ∧
    isPushDominant pushDominantWitness := by
  simp [pushDominantWitness, pullResidual, pushResidual, totalMagnitude, isPushDominant]

end Chronos.Frontier.GravityPullPushActualValueTest
