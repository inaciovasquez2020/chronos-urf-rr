import Oblivion.CFISkeleton
import Oblivion.OmegaTwistDetection

theorem omega_CFI_spec (H : BaseGraph) :
  omega (CFI H false) = false ∧
  omega (CFI H true) = true :=
by
  constructor <;> simp [CFI, omega, graph₀, graph₁]
