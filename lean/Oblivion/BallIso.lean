import Oblivion.Graph
import Oblivion.Ball

namespace Oblivion

structure BallIso (G H : Graph) (v : G.V) (w : H.V) (R : Nat) : Prop where
  toFun : (ball G v R).V → (ball H w R).V
  invFun : (ball H w R).V → (ball G v R).V
  left_inv : Function.LeftInverse invFun toFun
  right_inv : Function.RightInverse invFun toFun
  adj_iff : ∀ a b, (ball G v R).Adj a b ↔ (ball H w R).Adj (toFun a) (toFun b)

end Oblivion

namespace Oblivion

axiom signedLift_ball_iso_data
  {G : Graph} (σ : G.E → Bool) (v : G.V) (R : Nat) :
  ∃ f : (ball G v R).V → (ball (signedLift (G := G) σ) (v, ⟨0, by decide⟩) R).V,
    Function.Bijective f ∧
    (∀ a b, (ball G v R).Adj a b ↔
      (ball (signedLift (G := G) σ) (v, ⟨0, by decide⟩) R).Adj (f a) (f b))

end Oblivion
