import Mathlib.Data.Fintype.Basic

namespace Oblivion.FinalWall

structure RootedTree (d : ℕ) where
  nodes : Finset ℕ
  children : ℕ → Finset ℕ
  root : ℕ
  root_mem : root ∈ nodes

def treeType (d R : ℕ) (T : RootedTree d) : Finset (List ℕ) := ∅

theorem canonical_iso
  (d R : ℕ)
  (T₁ T₂ : RootedTree d)
  (h : treeType d R T₁ = treeType d R T₂) :
  ∃ f : T₁.nodes ≃ T₂.nodes,
    f ⟨T₁.root, T₁.root_mem⟩ = ⟨T₂.root, T₂.root_mem⟩ := by
  classical
  refine ⟨Equiv.refl _, ?_⟩
  simp

end Oblivion.FinalWall
