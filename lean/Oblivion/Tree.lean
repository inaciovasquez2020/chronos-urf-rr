import Oblivion.Graph

namespace Oblivion

structure IsTree (G : Graph) : Prop where
  connected : Connected G
  acyclic : True

end Oblivion
