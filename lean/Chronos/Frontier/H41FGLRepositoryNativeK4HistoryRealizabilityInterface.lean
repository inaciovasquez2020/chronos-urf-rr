import Mathlib

namespace Chronos
namespace Frontier

universe u

/-- The four Boolean coordinates required by the bounded `K₄` history model. -/
abbrev H41FGLK4BitVector : Type :=
  Fin 4 → ZMod 2

/--
The exact repository-native realizability interface still required for
`X(𝒫_{4,0,1})`.

An inhabitant must bind `History` to an independently specified admissible
history carrier. This structure does not construct that carrier and does not
identify it with the existing concrete sixteen-state Walsh model.
-/
structure H41FGLRepositoryNativeK4HistoryRealizability where
  History : Type u
  vertexObservable : Fin 4 → History → ZMod 2
  historyOfBits : H41FGLK4BitVector → History
  vertexObservable_historyOfBits :
    ∀ (σ : H41FGLK4BitVector) (i : Fin 4),
      vertexObservable i (historyOfBits σ) = σ i

namespace H41FGLRepositoryNativeK4HistoryRealizability

/-- The combined four-coordinate observation map. -/
def combinedObservable
    (data : H41FGLRepositoryNativeK4HistoryRealizability.{u}) :
    data.History → H41FGLK4BitVector :=
  fun h i => data.vertexObservable i h

/-- `historyOfBits` realizes its prescribed four Boolean coordinates. -/
theorem combinedObservable_historyOfBits
    (data : H41FGLRepositoryNativeK4HistoryRealizability.{u})
    (σ : H41FGLK4BitVector) :
    combinedObservable data (data.historyOfBits σ) = σ := by
  funext i
  exact data.vertexObservable_historyOfBits σ i

/--
The realizability interface discharges exactly `vertex_realizable`.

It does not prove coordinate extensionality and therefore does not yet produce
an equivalence with the sixteen-state concrete carrier.
-/
theorem vertex_realizable
    (data : H41FGLRepositoryNativeK4HistoryRealizability.{u}) :
    ∀ σ : H41FGLK4BitVector,
      ∃ h : data.History, combinedObservable data h = σ := by
  intro σ
  exact ⟨data.historyOfBits σ, combinedObservable_historyOfBits data σ⟩

/--
Repository-native vertex extensionality is the remaining injectivity
obligation: histories with identical four Boolean coordinates must coincide.
-/
def H41FGLRepositoryNativeK4VertexExt
    (data : H41FGLRepositoryNativeK4HistoryRealizability.{u}) : Prop :=
  ∀ h₁ h₂ : data.History,
    combinedObservable data h₁ = combinedObservable data h₂ →
      h₁ = h₂

/-- Vertex extensionality makes the combined observation map injective. -/
theorem combinedObservable_injective
    (data : H41FGLRepositoryNativeK4HistoryRealizability.{u})
    (hvertexExt : H41FGLRepositoryNativeK4VertexExt data) :
    Function.Injective (combinedObservable data) := by
  intro h₁ h₂ hcoordinates
  exact hvertexExt h₁ h₂ hcoordinates

/--
Realizability and vertex extensionality identify the history carrier with the
four-bit carrier without using an arbitrary inverse choice.
-/
def historyEquivBitVector
    (data : H41FGLRepositoryNativeK4HistoryRealizability.{u})
    (hvertexExt : H41FGLRepositoryNativeK4VertexExt data) :
    data.History ≃ H41FGLK4BitVector where
  toFun := combinedObservable data
  invFun := data.historyOfBits
  left_inv := by
    intro h
    apply hvertexExt
    exact
      combinedObservable_historyOfBits
        data
        (combinedObservable data h)
  right_inv := by
    intro σ
    exact combinedObservable_historyOfBits data σ

end H41FGLRepositoryNativeK4HistoryRealizability

end Frontier
end Chronos
