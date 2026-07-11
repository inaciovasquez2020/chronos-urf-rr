import Chronos.Frontier.H41FGLAffineLiftK4AtomEnumeration

namespace Chronos
namespace Frontier

open scoped BigOperators

/--
The parity of the four-bit dot product between two indices in `Fin 16`.
-/
def h41FGLK4WalshParity
    (history character : Fin 16) : Nat :=
  (∑ i : Fin 4,
      if Nat.testBit history.val i.val &&
          Nat.testBit character.val i.val
      then 1
      else 0) % 2

/--
The rational `16 × 16` Walsh character matrix for the bounded four-bit
`K₄` model.
-/
def h41FGLK4WalshMatrix :
    Matrix (Fin 16) (Fin 16) ℚ :=
  fun history character =>
    if h41FGLK4WalshParity history character = 0
    then 1
    else -1

/--
The candidate inverse `(1 / 16) Wᵀ`.
-/
def h41FGLK4WalshMatrixInv :
    Matrix (Fin 16) (Fin 16) ℚ :=
  (1 / 16 : ℚ) • h41FGLK4WalshMatrix.transpose

/--
Exact Walsh orthogonality.
-/
theorem h41FGLK4WalshMatrix_mul_transpose :
    h41FGLK4WalshMatrix *
        h41FGLK4WalshMatrix.transpose =
      (16 : ℚ) •
        (1 : Matrix (Fin 16) (Fin 16) ℚ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/--
The Walsh matrix multiplied by its explicit inverse is the identity.
-/
theorem h41FGLK4WalshMatrix_mul_inv :
    h41FGLK4WalshMatrix *
        h41FGLK4WalshMatrixInv =
      (1 : Matrix (Fin 16) (Fin 16) ℚ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/--
The explicit inverse multiplied by the Walsh matrix is the identity.
-/
theorem h41FGLK4WalshMatrix_inv_mul :
    h41FGLK4WalshMatrixInv *
        h41FGLK4WalshMatrix =
      (1 : Matrix (Fin 16) (Fin 16) ℚ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/--
The concrete Walsh matrix as a unit in the rational matrix ring.
-/
def h41FGLK4WalshMatrixUnit :
    (Matrix (Fin 16) (Fin 16) ℚ)ˣ where
  val := h41FGLK4WalshMatrix
  inv := h41FGLK4WalshMatrixInv
  val_inv := h41FGLK4WalshMatrix_mul_inv
  inv_val := h41FGLK4WalshMatrix_inv_mul

theorem h41FGLK4WalshMatrix_isUnit :
    IsUnit h41FGLK4WalshMatrix := by
  exact ⟨h41FGLK4WalshMatrixUnit, rfl⟩

/--
The maximal Walsh minor has exact rational rank sixteen.
-/
theorem h41FGLK4WalshMatrix_rank :
    h41FGLK4WalshMatrix.rank = 16 := by
  simpa using
    Matrix.rank_of_isUnit
      h41FGLK4WalshMatrix
      h41FGLK4WalshMatrix_isUnit

/--
The bounded Walsh correlation transform.
-/
def h41FGLK4WalshTransform
    (f : Fin 16 → ℚ) : Fin 16 → ℚ :=
  h41FGLK4WalshMatrix.mulVec f

/--
Full Walsh rank gives injectivity of the bounded correlation transform.
-/
theorem h41FGLK4WalshTransform_injective :
    Function.Injective h41FGLK4WalshTransform := by
  exact
    (Matrix.mulVec_injective_iff).2
      (Matrix.linearIndependent_cols_of_isUnit
        h41FGLK4WalshMatrix_isUnit)

/--
Kernel-trivial form of bounded correlation injectivity.
-/
theorem h41FGLK4WalshTransform_kernel_trivial
    (f : Fin 16 → ℚ)
    (hf : h41FGLK4WalshTransform f = 0) :
    f = 0 := by
  apply h41FGLK4WalshTransform_injective
  simpa [h41FGLK4WalshTransform] using hf

/--
Binary observable detecting a nonzero input vector.
-/
def h41FGLK4RankRate
    (f : Fin 16 → ℚ) : Nat :=
  if f = 0 then 0 else 1

/--
Binary observable detecting a nonzero Walsh correlation output.
-/
def h41FGLK4FiberMass
    (f : Fin 16 → ℚ) : Nat :=
  if h41FGLK4WalshTransform f = 0 then 0 else 1

/--
Exact restricted positivity consequence for the constructed bounded `K₄`
Walsh model.

This does not identify the model with the independently intended external
H4.1/FGL history space.
-/
theorem h41FGLK4RestrictedPositivity
    (f : Fin 16 → ℚ) :
    0 < h41FGLK4RankRate f →
      0 < h41FGLK4FiberMass f := by
  intro hr
  have hf : f ≠ 0 := by
    intro hzero
    simp [h41FGLK4RankRate, hzero] at hr
  have hTf : h41FGLK4WalshTransform f ≠ 0 := by
    intro hzero
    exact hf
      (h41FGLK4WalshTransform_kernel_trivial f hzero)
  simp [
    h41FGLK4FiberMass,
    hTf
  ]

end Frontier
end Chronos
