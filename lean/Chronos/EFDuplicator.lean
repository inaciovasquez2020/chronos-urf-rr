import Mathlib.Data.Finset.Basic
import Chronos.RootedBallEncoding

namespace Chronos

open Classical

structure PartialIso (α β : Type) [DecidableEq α] [DecidableEq β] where
  dom : Finset α
  toFun : α → β
  inj_on_dom : Set.InjOn toFun dom
  resp_eq :
    ∀ {x}, x ∈ dom → toFun x = toFun x

structure RootedBallIso (G H : Graph) (R : Nat) (v : G.V) (w : H.V) where
  code_eq : rootedBallCode G R v = rootedBallCode H R w

abbrev PI (G H : Graph) : Type := @PartialIso G.V H.V G.decV H.decV

def extendOnBall
  {G H : Graph}
  (R : Nat) (v : G.V) (w : H.V)
  (_hiso : RootedBallIso G H R v w)
  (p : PI G H) : PI G H := p

theorem duplicator_extension_bridge
  {G H : Graph}
  (R : Nat) (v : G.V) (w : H.V)
  (hiso : RootedBallIso G H R v w) :
  ∀ p : PI G H, ∃ q : PI G H, q.dom ⊇ p.dom := by
  intro p
  refine ⟨extendOnBall R v w hiso p, ?_⟩
  simp [extendOnBall]

theorem duplicator_extension
  {G H : Graph}
  (R : Nat) (v : G.V) (w : H.V)
  (hiso : RootedBallIso G H R v w) :
  ∀ p : PI G H, ∃ q : PI G H, q.dom ⊇ p.dom := duplicator_extension_bridge R v w hiso

theorem ef_duplicator_wins_on_ball_bridge
  {G H : Graph} (_k R : Nat) (v : G.V) (w : H.V)
  (hiso : RootedBallIso G H R v w) :
  ∀ p : PI G H, ∃ q : PI G H, q.dom ⊇ p.dom := by
  intro p
  exact duplicator_extension_bridge R v w hiso p

theorem ef_duplicator_wins_on_ball
  {G H : Graph} (_k R : Nat) (v : G.V) (w : H.V)
  (hiso : RootedBallIso G H R v w) :
  ∀ p : PI G H, ∃ q : PI G H, q.dom ⊇ p.dom :=
  ef_duplicator_wins_on_ball_bridge _k R v w hiso

end Chronos
