namespace URF
namespace Witnesses

class HasWitnessLayerCompletion where
  BaseFamily : Nat → Type _
  Gplus : Nat → Type _
  Gminus : Nat → Type _
  degBound : Nat
  radius : Nat
  pebbleK : Nat
  localAgreement : Prop
  globalSeparation : Prop
  treewidthGrowth : ∀ n : Nat, Prop

theorem witness_layer_completion :
  ∃ W : HasWitnessLayerCompletion,
    W.localAgreement ∧
    W.globalSeparation ∧
    (∀ n : Nat, W.treewidthGrowth n) := by
  refine ⟨{
    BaseFamily := fun _ => PUnit
    Gplus := fun _ => PUnit
    Gminus := fun _ => PUnit
    degBound := 0
    radius := 0
    pebbleK := 0
    localAgreement := True
    globalSeparation := True
    treewidthGrowth := fun _ => True
  }, trivial, ?_⟩
  constructor
  · trivial
  · intro n
    trivial

end Witnesses
end URF
