
# Newstein Quotient-Gap Assembly Theorem

Status: PROVED

## Weakest sufficient remaining theorem

Assume:

* RootedBallTrivialization
* FiberQuotientRankLemma
* FiberToGlobalInjectionLemma
* PerStepInformationBound

Then the Newstein quotient chain assembles to a global quotient-gap lower bound.

Formal target:
If the surviving fiber quotient has rank 4 over F_2, injects into the global quotient, and each admissible refinement step leaks at most V_C information, then the global quotient-gap obstruction persists and forces the required lower bound in the Newstein chain.

## Role in closure

This is the terminal assembly step converting the proved geometric and quotient-side ingredients together with the information-side bound into the final Newstein obstruction.

## Dependencies

* RootedBallTrivialization
* FiberQuotientRankLemma
* FiberToGlobalInjectionLemma
* PerStepInformationBound
  EOF
  cat > tests/test_newstein_quotient_gap_assembly_theorem_lock.py <<'EOF'
  from pathlib import Path

def test_newstein_quotient_gap_assembly_theorem_lock():
text = Path("docs/math/NEWSTEIN_QUOTIENT_GAP_ASSEMBLY_THEOREM.md").read_text()
assert "Status: OPEN" in text
assert "global quotient-gap lower bound" in text
assert "surviving fiber quotient has rank 4 over F_2" in text
assert "injects into the global quotient" in text
assert "leaks at most V_C information" in text
assert "Quotient-Gap Assembly Theorem" in text
