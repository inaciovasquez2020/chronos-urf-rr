import Oblivion.Graph
import Oblivion.Cycle

namespace Oblivion

def Acyclic (G : Graph) : Prop := ∀ C : Cycle G, False

structure IsTree (G : Graph) : Prop where
  connected : Connected G
  acyclic : Acyclic G

end Oblivion
