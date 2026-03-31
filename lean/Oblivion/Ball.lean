import Oblivion.Graph

namespace Oblivion

variable {G : Graph}

def ball (G : Graph) (v : G.V) (R : Nat) : Graph := G

lemma connected_ball (v : G.V) (R : Nat) :
    Connected (ball G v R) := by
  admit

end Oblivion
