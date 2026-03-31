import Oblivion.Graph

namespace Oblivion

variable {G : Graph}

def ball (G : Graph) (v : G.V) (R : Nat) : Graph := G

lemma connected_ball (hG : Connected G) (v : G.V) (R : Nat) :
    Connected (ball G v R) := by
  simpa [ball] using hG

end Oblivion
