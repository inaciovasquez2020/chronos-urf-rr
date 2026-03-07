import Oblivion.WL2TransportBridge
import Oblivion.FO3Definitions

namespace Oblivion

variable {V : Type}

/-- WL² distinguishability implies FO³ type difference (skeleton). -/
theorem wl2_implies_fo3
  (G : Graph V)
  :
  ∀ u v : V,
  wl2Color G u ≠ wl2Color G v →
  fo3Type G u ≠ fo3Type G v := by
  intro u v h
  admit

/-- COR_R ⇒ FO³ diversity (skeleton). -/
theorem corR_implies_fo3
  (G : Graph V)
  (R T : Nat)
  (h : largeCycleOverlap G R T)
  :
  ∃ u v : V, fo3Type G u ≠ fo3Type G v := by
  obtain ⟨u,v,hWL⟩ := corR_implies_wl2 (G:=G) (R:=R) (T:=T) h
  have h2 := wl2_implies_fo3 (G:=G) u v hWL
  exact ⟨u,v,h2⟩

end Oblivion
