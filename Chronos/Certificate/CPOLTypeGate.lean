namespace Chronos
namespace Certificate

/--
CPOL type gate.

This is a repository-side primitive carrier family only.
It is independent of the target-side objects F_n={0,1}^n and μ_n.

Boundary:
- does not construct C_n^Chr;
- does not define P_Chr;
- does not prove CPDL;
- does not prove CCSL;
- does not define ν_n;
- does not define admissible observables;
- does not prove ChronosCertificateEmbedding.
-/
inductive TChr (n : Nat) : Type
| base : TChr n
deriving DecidableEq

def tChrCanonicalWitness (n : Nat) : TChr n :=
  TChr.base

def tChrCode {n : Nat} (_ : TChr n) : Nat :=
  0

theorem tChr_code_eq_zero {n : Nat} (x : TChr n) : tChrCode x = 0 := by
  cases x
  rfl

theorem tChr_all_eq_base {n : Nat} (x : TChr n) : x = TChr.base := by
  cases x
  rfl

theorem tChr_nonempty (n : Nat) : Nonempty (TChr n) :=
  ⟨TChr.base⟩

theorem tChr_decidableEq_exists (n : Nat) : Nonempty (DecidableEq (TChr n)) :=
  ⟨inferInstance⟩

end Certificate
end Chronos
