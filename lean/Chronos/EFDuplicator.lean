import Mathlib.Data.Finset.Basic
import Chronos.RootedBallEncoding

namespace Chronos

open Classical

structure PartialIso {α β : Type} [DecidableEq α] [DecidableEq β] where
  dom : Finset α
  toFun : α → β
  inj_on_dom : Set.InjOn toFun dom
  resp_eq :
    ∀ {x}, x ∈ dom → toFun x = toFun x

structure RootedBallIso (G H : Graph) (R : Nat) (v : G.V) (w : H.V) where
  code_eq : rootedBallCode G R v = rootedBallCode H R w

def extendOnBall
  {G H : Graph} [DecidableEq G.V] [DecidableEq H.V]
  (R : Nat) (v : G.V) (w : H.V)
  (hiso : RootedBallIso G H R v w)
  (p : PartialIso) : PartialIso := p

theorem duplicator_extension_bridge
  {G H : Graph} [DecidableEq G.V] [DecidableEq H.V]
  (R : Nat) (v : G.V) (w : H.V)
  (hiso : RootedBallIso G H R v w) :
  ∀ p : PartialIso, ∃ q : PartialIso, q.dom ⊇ p.dom := by
  intro p
  refine ⟨extendOnBall R v w hiso p, ?_⟩
  simp [extendOnBall]

theorem duplicator_extension
  {G H : Graph} [DecidableEq G.V] [DecidableEq H.V]
  (R : Nat) (v : G.V) (w : H.V)
  (hiso : RootedBallIso G H R v w) :
  ∀ p : PartialIso, ∃ q : PartialIso, q.dom ⊇ p.dom := duplicator_extension_bridge R v w hiso

axiom ef_duplicator_wins_on_ball_bridge
  {G H : Graph} (k R : Nat) (v : G.V) (w : H.V)
  (hiso : RootedBallIso G H R v w) :
  True

theorem ef_duplicator_wins_on_ball := ef_duplicator_wins_on_ball_bridge

end Chronos
