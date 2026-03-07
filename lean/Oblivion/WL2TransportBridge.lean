import Oblivion.TransportSignatureLemma
import Oblivion.WL2Definitions

namespace Oblivion

variable {V : Type}

/-- Transport signature difference implies WL² color difference (skeleton). -/
theorem transport_implies_wl2
  (G : Graph V)
  (R : Nat)
  :
  ∀ u v : V,
  signature G R u ≠ signature G R v →
  wl2Color G u ≠ wl2Color G v := by
  intro u v h
  admit

/-- COR_R ⇒ WL² diversity (skeleton). -/
theorem corR_implies_wl2
  (G : Graph V)
  (R T : Nat)
  (h : largeCycleOverlap G R T)
  :
  ∃ u v : V, wl2Color G u ≠ wl2Color G v := by
  obtain ⟨u,v,hSig⟩ := transport_signature_diversity (G:=G) (R:=R) (T:=T) h
  have h2 := transport_implies_wl2 (G:=G) (R:=R) u v hSig
  exact ⟨u,v,h2⟩

end Oblivion
