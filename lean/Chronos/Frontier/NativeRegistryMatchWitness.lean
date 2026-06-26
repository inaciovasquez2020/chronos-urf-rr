import Mathlib.Tactic
import Chronos.Frontier.NewsteinR1R2R3NativeBindingSpec

namespace Chronos
namespace Frontier

/--
Repository-native registry-match data required by the Newstein R1/R2/R3
binding interface.

This is a witness surface for registry matching only.
It does not construct geometric, quotient, fiber, two-chain, or R1/R2/R3
correctness data.
-/
structure NativeRegistryMatchData where
  binding : NewsteinR1R2R3NativeBindingSpec
  r1MatchesOpenInputsRegistrySupplied : binding.r1MatchesOpenInputsRegistry
  r2MatchesOpenInputsRegistrySupplied : binding.r2MatchesOpenInputsRegistry
  r3MatchesOpenInputsRegistrySupplied : binding.r3MatchesOpenInputsRegistry

def NativeRegistryMatchesSupplied
    (R : NativeRegistryMatchData) : Prop :=
  R.binding.r1MatchesOpenInputsRegistry ∧
  R.binding.r2MatchesOpenInputsRegistry ∧
  R.binding.r3MatchesOpenInputsRegistry

theorem native_registry_matches_supplied
    (R : NativeRegistryMatchData) :
    NativeRegistryMatchesSupplied R := by
  exact ⟨
    R.r1MatchesOpenInputsRegistrySupplied,
    R.r2MatchesOpenInputsRegistrySupplied,
    R.r3MatchesOpenInputsRegistrySupplied
  ⟩

end Frontier
end Chronos
