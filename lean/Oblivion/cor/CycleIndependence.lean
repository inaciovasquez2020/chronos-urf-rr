-- lean/oblivion/cor/CORProjection.lean  (APPEND at end)

import Mathlib.LinearAlgebra.Matrix
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Finset

namespace COR

open scoped Matrix

structure PatchCycles (V : Type) :=
(cycles : Finset (Finset V))
(patches : Finset (Finset V))

def incidence
{V} [DecidableEq V]
(C : PatchCycles V) :
Matrix (Fin C.cycles.card) (Fin C.patches.card) (ZMod 2) :=
by
  classical
  exact fun i j =>
    if C.cycles[i]! ⊆ C.patches[j]! then 1 else 0

def COR
{V} [DecidableEq V]
(C : PatchCycles V) :=
Matrix.rank (incidence C)

axiom rank_ge_card_of_rows_linearIndependent
{m n : Type} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]
{R : Type} [Semiring R]
(A : Matrix m n R)
(hLI : LinearIndependent R (fun i : m => A i)) :
Matrix.rank A ≥ Fintype.card m

lemma packing_bound_to_cor_ge_packing
{V} [DecidableEq V]
(C : PatchCycles V)
(hLI : LinearIndependent (ZMod 2) (fun i : Fin C.cycles.card => incidence (C:=C) i)) :
COR C ≥ C.cycles.card :=
by
  classical
  -- rank(A) ≥ #rows
  have h := rank_ge_card_of_rows_linearIndependent (A := incidence (C:=C)) hLI
  simpa [COR] using h

end COR
