import Oblivion.RootedBallCode
import Oblivion.CFI2Lift

variable {G : Graph} [Fintype G.V] [DecidableEq G.V]

def proj (v : (TwoLift G).V) : G.V := v.1

theorem ball_projection_eq
  (R : Nat) (v : (TwoLift G).V) :
  rootedBallCode (TwoLift G) R v =
  (rootedBallCode G R (proj v)).image (fun x => (x, false)) :=
by
  ext w
  simp [rootedBallCode, Ball, proj]

theorem duplicator_preserves_ball
  (R : Nat)
  (v : (TwoLift G).V) :
  rootedBallCode (TwoLift G) R v =
  rootedBallCode (TwoLift G) R (v.1, false) :=
by
  simp [rootedBallCode]
