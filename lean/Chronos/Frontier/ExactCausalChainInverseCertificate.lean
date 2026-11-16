import Init

namespace Chronos.Frontier.ExactCausalChainInverse

def a : Rat := 1 / 25
def b : Rat := 0
def c : Rat := 9 / 3500
def d : Rat := 16 / 165375

def p : Rat := 25
def q : Rat := 0
def r : Rat := -(42525 / 64)
def s : Rat := 165375 / 16

set_option maxRecDepth 4096

theorem forward_inverse_11 :
    a * p + b * r = 1 := by decide +kernel

theorem forward_inverse_12 :
    a * q + b * s = 0 := by decide +kernel

theorem forward_inverse_21 :
    c * p + d * r = 0 := by decide +kernel

theorem forward_inverse_22 :
    c * q + d * s = 1 := by decide +kernel

theorem inverse_forward_11 :
    p * a + q * c = 1 := by decide +kernel

theorem inverse_forward_12 :
    p * b + q * d = 0 := by decide +kernel

theorem inverse_forward_21 :
    r * a + s * c = 0 := by decide +kernel

theorem inverse_forward_22 :
    r * b + s * d = 1 := by decide +kernel

theorem determinant_exact :
    a * d - b * c = 16 / 4134375 := by
  decide +kernel

theorem determinant_positive :
    (0 : Rat) < a * d - b * c := by
  decide +kernel

#print axioms forward_inverse_11
#print axioms forward_inverse_12
#print axioms forward_inverse_21
#print axioms forward_inverse_22
#print axioms inverse_forward_11
#print axioms inverse_forward_12
#print axioms inverse_forward_21
#print axioms inverse_forward_22
#print axioms determinant_exact
#print axioms determinant_positive

end Chronos.Frontier.ExactCausalChainInverse
