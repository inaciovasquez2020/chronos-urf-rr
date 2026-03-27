import Oblivion.EFEquiv

structure Ball (G : Graph) (R : Nat) (v : G.V) where
  nodes : Finset G.V

def RadiusRType (G : Graph) (R : Nat) : Type :=
G.V → Nat

class RadiusRCode (G : Graph) where
  code : Nat → Nat → EFState G · → Nat

def localType (G : Graph) (R : Nat) : RadiusRType G R :=
fun v => 0

instance (G : Graph) : RadiusRCode G where
  code R t s := 0
