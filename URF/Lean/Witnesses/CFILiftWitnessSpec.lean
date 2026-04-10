namespace URF
namespace Witnesses

structure CFILiftWitnessSpec where
  BaseFamily : ℕ → Type
  Gplus : ℕ → Type
  Gminus : ℕ → Type
  degBound : ℕ
  radius : ℕ
  pebbleK : ℕ
  localAgreement : ∀ n, True
  globalSeparation : ∀ n, True
  treewidthGrowth : ∀ n, True

end Witnesses
end URF
