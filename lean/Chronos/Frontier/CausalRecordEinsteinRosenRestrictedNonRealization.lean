import Mathlib

namespace Chronos.Frontier

universe u v w

structure TopologicalCarrier where
  carrier : Type
  topology : TopologicalSpace carrier

instance instTopologicalSpace (X : TopologicalCarrier) : TopologicalSpace X.carrier :=
  X.topology

abbrev R3 := EuclideanSpace ℝ (Fin 3)

abbrev ClosedBall3 :=
  {x : R3 // x ∈ Metric.closedBall (0 : R3) 1}

structure SliceEvolution (Time : Type u) where
  Slice : Time → TopologicalCarrier
  initialTime : Time
  evolutionHomeomorph :
    ∀ s t, (Slice s).carrier ≃ₜ (Slice t).carrier
  initialR3Homeomorph :
    (Slice initialTime).carrier ≃ₜ R3

namespace SliceEvolution

def r3Homeomorph
    {Time : Type u}
    (E : SliceEvolution Time)
    (t : Time) :
    (E.Slice t).carrier ≃ₜ R3 :=
  (E.evolutionHomeomorph t E.initialTime).trans E.initialR3Homeomorph

theorem preservesR3
    {Time : Type u}
    (E : SliceEvolution Time)
    (t : Time) :
    Nonempty ((E.Slice t).carrier ≃ₜ R3) :=
  ⟨E.r3Homeomorph t⟩

end SliceEvolution

def Extends
    {α : Type w}
    (earlier later : List α) : Prop :=
  ∃ suffix, later = earlier ++ suffix

structure DecodedCoreSystem
    (Time : Type u)
    (α : Type w)
    (E : SliceEvolution Time) where
  recordPrefix : Nat → List α
  prefixSucc :
    ∀ d, ∃ a, recordPrefix (d + 1) = recordPrefix d ++ [a]
  decode :
    ∀ t, List α → Set (E.Slice t).carrier
  decodeAntitone :
    ∀ t {earlier later},
      Extends earlier later →
      decode t later ⊆ decode t earlier
  coreChart :
    ∀ t d,
      Nonempty
        ({x // x ∈ decode t (recordPrefix d)} ≃ₜ ClosedBall3)

namespace DecodedCoreSystem

theorem decodedCoresNested
    {Time : Type u}
    {α : Type w}
    {E : SliceEvolution Time}
    (C : DecodedCoreSystem Time α E)
    (t : Time)
    (d : Nat) :
    C.decode t (C.recordPrefix (d + 1)) ⊆
      C.decode t (C.recordPrefix d) := by
  apply C.decodeAntitone t
  rcases C.prefixSucc d with ⟨a, ha⟩
  exact ⟨[a], ha⟩

theorem decodedCoreIsThreeBall
    {Time : Type u}
    {α : Type w}
    {E : SliceEvolution Time}
    (C : DecodedCoreSystem Time α E)
    (t : Time)
    (d : Nat) :
    Nonempty
      ({x // x ∈ C.decode t (C.recordPrefix d)} ≃ₜ ClosedBall3) :=
  C.coreChart t d

end DecodedCoreSystem

structure CenterSystem
    (Time : Type u)
    (E : SliceEvolution Time) where
  center :
    ∀ t, (E.Slice t).carrier
  IsCenter :
    ∀ t, (E.Slice t).carrier → Prop
  RegularAt :
    ∀ t, (E.Slice t).carrier → Prop
  centerCharacterization :
    ∀ t x, IsCenter t x ↔ x = center t
  centerTransport :
    ∀ s t,
      E.evolutionHomeomorph s t (center s) = center t
  regularTransport :
    ∀ s t x,
      RegularAt s x ↔
      RegularAt t (E.evolutionHomeomorph s t x)
  initialRegular :
    RegularAt E.initialTime (center E.initialTime)

namespace CenterSystem

theorem centerUnique
    {Time : Type u}
    {E : SliceEvolution Time}
    (C : CenterSystem Time E)
    {t : Time}
    {x y : (E.Slice t).carrier}
    (hx : C.IsCenter t x)
    (hy : C.IsCenter t y) :
    x = y := by
  exact
    ((C.centerCharacterization t x).mp hx).trans
      ((C.centerCharacterization t y).mp hy).symm

theorem centerRemainsRegular
    {Time : Type u}
    {E : SliceEvolution Time}
    (C : CenterSystem Time E)
    (t : Time) :
    C.RegularAt t (C.center t) := by
  have h :=
    (C.regularTransport E.initialTime t (C.center E.initialTime)).mp
      C.initialRegular
  rw [C.centerTransport E.initialTime t] at h
  exact h

end CenterSystem

structure AsymptoticEndSystem
    (Time : Type u)
    (initialTime : Time) where
  End : Time → Type v
  endTransport :
    ∀ s t, End s ≃ End t
  initialEnd :
    End initialTime
  initialEndUnique :
    ∀ e : End initialTime, e = initialEnd

namespace AsymptoticEndSystem

theorem endRemainsUnique
    {Time : Type u}
    {initialTime : Time}
    (A : AsymptoticEndSystem Time initialTime)
    (t : Time)
    (e₁ e₂ : A.End t) :
    e₁ = e₂ := by
  apply (A.endTransport initialTime t).symm.injective
  calc
    (A.endTransport initialTime t).symm e₁ = A.initialEnd :=
      A.initialEndUnique _
    _ = (A.endTransport initialTime t).symm e₂ :=
      (A.initialEndUnique _).symm

def HasEinsteinRosenTwoEndTopology
    {Time : Type u}
    {initialTime : Time}
    (A : AsymptoticEndSystem Time initialTime)
    (t : Time) : Prop :=
  ∃ e₁ e₂ : A.End t, e₁ ≠ e₂

theorem noSecondAsymptoticEnd
    {Time : Type u}
    {initialTime : Time}
    (A : AsymptoticEndSystem Time initialTime)
    (t : Time) :
    ¬ A.HasEinsteinRosenTwoEndTopology t := by
  rintro ⟨e₁, e₂, hne⟩
  exact hne (A.endRemainsUnique t e₁ e₂)

end AsymptoticEndSystem

theorem causalRecordRestrictedEinsteinRosenNonRealization
    {Time : Type u}
    {α : Type w}
    (E : SliceEvolution Time)
    (C : DecodedCoreSystem Time α E)
    (Z : CenterSystem Time E)
    (A : AsymptoticEndSystem Time E.initialTime)
    (t : Time) :
    Nonempty ((E.Slice t).carrier ≃ₜ R3) ∧
    (∀ d,
      C.decode t (C.recordPrefix (d + 1)) ⊆
        C.decode t (C.recordPrefix d)) ∧
    (∀ d,
      Nonempty
        ({x // x ∈ C.decode t (C.recordPrefix d)} ≃ₜ ClosedBall3)) ∧
    Z.RegularAt t (Z.center t) ∧
    (∀ {x y : (E.Slice t).carrier},
      Z.IsCenter t x →
      Z.IsCenter t y →
      x = y) ∧
    ¬ A.HasEinsteinRosenTwoEndTopology t := by
  constructor
  · exact E.preservesR3 t
  constructor
  · intro d
    exact C.decodedCoresNested t d
  constructor
  · intro d
    exact C.decodedCoreIsThreeBall t d
  constructor
  · exact Z.centerRemainsRegular t
  constructor
  · intro x y hx hy
    exact Z.centerUnique hx hy
  · exact A.noSecondAsymptoticEnd t

def causalRecordRestrictedEinsteinRosenBoundary : String :=
  "CONDITIONAL_RESTRICTED_NON_REALIZATION_ONLY"

end Chronos.Frontier
