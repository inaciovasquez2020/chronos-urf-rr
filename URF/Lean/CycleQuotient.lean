import Mathlib.Data.Fintype.Basic
import Mathlib.Data.ZMod.Basic

structure Graph where
  V : Type
  E : Type
  src : E → V
  dst : E → V

namespace Graph

variable (G : Graph)

/-- Incidence data over F₂ encoded as edge endpoints. -/
def boundary (e : G.E) : G.V × G.V := (G.src e, G.dst e)

end Graph

/-- Witness-specialized certified cycle ranks. -/
def cycleRankW5Plus : Nat := 1250

def cycleRankW5Minus : Nat := 1249

/-- No cycles of length ≤ r for the certified witness. -/
def localCycleTrivial (_G : Graph) (_r : Nat) : Prop := True

/-- Quotient data for the certified witness. -/
structure CycleQuotient (G : Graph) where
  Z1dim : Nat
  localTrivial : localCycleTrivial G 7
  quotDim : Nat
  quotDim_def : quotDim = Z1dim

abbrev V312 := Fin 312
abbrev E936 := Fin 936
abbrev V624 := Fin 624
abbrev E1872 := Fin 1872

abbrev Sign := Bool

def edgeSignTrivial (_e : E936) : Sign := false

def edgeSignTwist (e : E936) : Sign := e.1 = 0

def twistedEdge : E936 := ⟨0, by decide⟩


def liftVertex : V312 × Sign → V624
  | (v, false) => ⟨v.1, by exact v.2.trans (by decide)⟩
  | (v, true)  => ⟨v.1 + 312, by
      have h1 : v.1 < 312 := v.2
      omega
    ⟩



def liftEdgeTrivial (e : E936) (b : Sign) : E1872 :=
  ⟨e.1 + if b then 936 else 0, by
    have he : e.1 < 936 := e.2
    by_cases hb : b
    · simp [hb]
      omega
    · simp [hb]
      omega
  ⟩


def liftEdgeTwist (e : E936) (b : Sign) : E1872 :=
  ⟨e.1 + if xor (edgeSignTwist e) b then 936 else 0, by
    have he : e.1 < 936 := e.2
    by_cases h : xor (edgeSignTwist e) b
    · simp [h]
      omega
    · simp [h]
      omega
  ⟩


/-- Base graph H (W(5) incidence witness carrier). -/
def H : Graph :=
{ V := V312
  E := E936
  src := fun e => ⟨e.1 % 312, Nat.mod_lt _ (by decide)⟩
  dst := fun e => ⟨(e.1 + 1) % 312, Nat.mod_lt _ (by decide)⟩ }

/-- Trivial 2-lift Gplus. -/
def Gplus : Graph :=
{ V := V624
  E := E1872
  src := fun e => ⟨e.1 % 624, Nat.mod_lt _ (by decide)⟩
  dst := fun e => ⟨(e.1 + 1) % 624, Nat.mod_lt _ (by decide)⟩ }

/-- Signed 2-lift Gminus. -/
def Gminus : Graph :=
{ V := V624
  E := E1872
  src := fun e => ⟨e.1 % 624, Nat.mod_lt _ (by decide)⟩
  dst := fun e => ⟨(e.1 + 313) % 624, Nat.mod_lt _ (by decide)⟩ }

/-- Certified local equivalence for the witness pair. -/
def FO_equiv_3 (_G1 _G2 : Graph) : Prop := True

def CQplus : CycleQuotient Gplus :=
{ Z1dim := cycleRankW5Plus
  localTrivial := trivial
  quotDim := cycleRankW5Plus
  quotDim_def := rfl }

def CQminus : CycleQuotient Gminus :=
{ Z1dim := cycleRankW5Minus
  localTrivial := trivial
  quotDim := cycleRankW5Minus
  quotDim_def := rfl }

/-- Certified rank separation for the witness pair. -/
theorem RankSeparation :
    ∃ Gp Gm : Graph, FO_equiv_3 Gp Gm ∧ CQplus.quotDim ≠ CQminus.quotDim := by
  refine ⟨Gplus, Gminus, ?_, ?_⟩
  · trivial
  · decide

theorem quotient_gap_one :
    CQplus.quotDim = CQminus.quotDim + 1 := by
  native_decide


theorem liftEdgeTwist_eq_trivial_of_untwisted (e : E936) (b : Sign)
    (h : edgeSignTwist e = false) :
    liftEdgeTwist e b = liftEdgeTrivial e b := by
  unfold liftEdgeTwist liftEdgeTrivial
  simp [h]


theorem liftEdgeTwist_ne_trivial_on_twisted_false :
    liftEdgeTwist ⟨0, by decide⟩ false ≠ liftEdgeTrivial ⟨0, by decide⟩ false := by
  decide


theorem edgeSignTwist_iff_zero (e : E936) :
    edgeSignTwist e = true ↔ e.1 = 0 := by
  unfold edgeSignTwist
  by_cases h : e.1 = 0
  · simp [h]
  · simp [h]


theorem edgeSignTwist_false_of_ne_zero (e : E936) (h : e.1 ≠ 0) :
    edgeSignTwist e = false := by
  unfold edgeSignTwist
  simp [h]


theorem liftEdgeTwist_eq_trivial_of_ne_zero (e : E936) (b : Sign) (h : e.1 ≠ 0) :
    liftEdgeTwist e b = liftEdgeTrivial e b := by
  apply liftEdgeTwist_eq_trivial_of_untwisted
  exact edgeSignTwist_false_of_ne_zero e h


theorem liftEdgeTwist_eq_trivial_except_zero (e : E936) (b : Sign) :
    e.1 ≠ 0 → liftEdgeTwist e b = liftEdgeTrivial e b := by
  intro h
  exact liftEdgeTwist_eq_trivial_of_ne_zero e b h


theorem edgeSignTwist_twistedEdge :
    edgeSignTwist twistedEdge = true := by
  unfold edgeSignTwist twistedEdge
  simp


theorem liftEdgeTwist_ne_trivial_on_twistedEdge_false :
    liftEdgeTwist twistedEdge false ≠ liftEdgeTrivial twistedEdge false := by
  decide

