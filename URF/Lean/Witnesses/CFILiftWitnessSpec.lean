namespace URF
namespace Witnesses

structure CFILiftWitnessSpec where
  BaseFamily : Nat → Type _
  Gplus : Nat → Type _
  Gminus : Nat → Type _
  degBound : Nat
  radius : Nat
  pebbleK : Nat
  localAgreement : True
  globalSeparation : ∀ n : Nat, True
  treewidthGrowth : ∀ n : Nat, True

end Witnesses
end URF
