-- lean/oblivion/trace_method/TraceMethod.lean

import Mathlib.LinearAlgebra.Matrix
import Mathlib.Data.Real.Basic

namespace TraceMethod

open Matrix

variable {n : Type} [Fintype n] [DecidableEq n]

axiom trace_pow_eigen_expansion
(A : Matrix n n ℝ)
(k : Nat)
(hsymm : Aᵀ = A) :
∃ λ : n → ℝ,
Matrix.trace (A^k) = ∑ i, (λ i)^k

axiom spectral_gap_bound
(A : Matrix n n ℝ)
(d λ : ℝ)
(k : Nat)
(i1 : n)
(hsymm : Aᵀ = A) :
Matrix.trace (A^k) ≥ d^k - ((Fintype.card n - 1 : ℝ) * λ^k)

end TraceMethod
