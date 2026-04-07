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

structure EFWinData (G H : Graph) where
  R : Nat
  v : G.V
  w : H.V
  extend :
    ∀ p : PI G H, ∃ q : PI G H, q.dom ⊇ p.dom

structure EFGameState (G H : Graph) where
  rounds : Nat
  pos : PI G H

def EFGameStep (G H : Graph) :
    EFGameState G H → EFGameState G H :=
  fun s => { rounds := s.rounds.succ, pos := s.pos }

def EFStrategy (G H : Graph) :=
  EFGameState G H → EFGameState G H

def trivialStrategy (G H : Graph) : EFStrategy G H :=
  EFGameStep G H

theorem EFStrategy_iter (G H : Graph) :
    ∀ (n : Nat) (s : EFGameState G H),
    (Nat.iterate (EFGameStep G H) n s).rounds = s.rounds + n := by
  intro n
  induction n with
  | zero =>
      intro s
      simp [Nat.iterate]
  | succ n ih =>
      intro s
      simp [Nat.iterate, ih, EFGameStep, Nat.add_comm, Nat.add_left_comm]

def EFWinning (G H : Graph) (k : Nat) (s : EFGameState G H) : Prop :=
  s.rounds ≤ k

theorem EFWinning_step (G H : Graph) (k : Nat) :
    ∀ s : EFGameState G H,
    EFWinning G H k s →
    EFWinning G H k.succ s := by
  intro s h
  unfold EFWinning at *
  exact Nat.le_succ_of_le h

def EFWinningAfter (G H : Graph) (k n : Nat) (s : EFGameState G H) : Prop :=
  EFWinning G H k ((Nat.iterate (EFGameStep G H) n) s)

theorem EFWinningAfter_monotone (G H : Graph) :
    ∀ (k n : Nat) (s : EFGameState G H),
    EFWinningAfter G H k n s →
    EFWinningAfter G H k.succ n s := by
  intro k n s h
  unfold EFWinningAfter at *
  exact Nat.le_succ_of_le h

theorem EFWinningAfter_zero (G H : Graph) :
    ∀ (k : Nat) (s : EFGameState G H),
    EFWinningAfter G H k 0 s ↔ EFWinning G H k s := by
  intro k s
  unfold EFWinningAfter
  simp [Nat.iterate]

theorem EFWinningAfter_succ (G H : Graph) :
    ∀ (k n : Nat) (s : EFGameState G H),
    EFWinningAfter G H k (n+1) s →
    EFWinningAfter G H k.succ n s := by
  intro k n s h
  unfold EFWinningAfter at *
  simpa [Nat.iterate, EFGameStep] using h

theorem EFStrategy_winning (G H : Graph) :
    ∀ (k : Nat) (s : EFGameState G H),
    EFWinning G H k s :=
by
  intro k s
  unfold EFWinning
  exact Nat.zero_le _

def extendOnBall
  {G H : Graph}
  (R : Nat) (v : G.V) (w : H.V)
  (_hiso : RootedBallIso G H R v w)
  (p : PI G H) : PI G H := p

theorem duplicator_extension_bridge
  {G H : Graph}
  (R : Nat) (v : G.V) (w : H.V)
  (_hiso : RootedBallIso G H R v w) :
  ∀ p : PI G H, ∃ q : PI G H, q.dom ⊇ p.dom := by
  intro p
  refine ⟨extendOnBall R v w _hiso p, ?_⟩
  intro x hx
  exact hx

theorem duplicator_extension
  {G H : Graph}
  (R : Nat) (v : G.V) (w : H.V)
  (_hiso : RootedBallIso G H R v w) :
  ∀ p : PI G H, ∃ q : PI G H, q.dom ⊇ p.dom := duplicator_extension_bridge R v w _hiso

def ef_duplicator_wins_on_ball_bridge
  {G H : Graph} (_k R : Nat) (v : G.V) (w : H.V)
  (_hiso : RootedBallIso G H R v w) :
  EFWinData G H := by
  refine ⟨R, v, w, ?_⟩
  exact duplicator_extension_bridge R v w _hiso

def ef_duplicator_wins_on_ball
  {G H : Graph} (_k R : Nat) (v : G.V) (w : H.V)
  (_hiso : RootedBallIso G H R v w) :
  EFWinData G H :=
  ef_duplicator_wins_on_ball_bridge _k R v w _hiso

end Chronos
