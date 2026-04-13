
# Newstein Fiber-to-Global Injection Lemma

Status: OPEN

## Weakest sufficient remaining lemma

Let T be a Newstein triangulation in the rooted-ball trivialization regime, and let q_R denote the quotient by locally trivialized rooted-ball cycles. The canonical map from the surviving fiber quotient classes into the global quotient is injective.

Formal target:
If a surviving fiber class maps to 0 in the global quotient, then that fiber class is already 0 in the fiber quotient.

## Role in closure

This is the exact transport step needed to lift the local Newstein quotient-rank lower bound into the global quotient-gap statement.

## Dependencies

* RootedBallTrivialization
* FiberQuotientRankLemma
* support separation between surviving fiber representatives and rooted-ball boundaries
* no extra global cancellation outside the fiber quotient
  EOF
  cat > tests/test_newstein_fiber_to_global_injection_lemma_lock.py <<'EOF'
  from pathlib import Path

def test_newstein_fiber_to_global_injection_lemma_lock():
text = Path("docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTION_LEMMA.md").read_text()
assert "Status: OPEN" in text
assert "canonical map from the surviving fiber quotient classes into the global quotient is injective" in text
assert "maps to 0 in the global quotient" in text
assert "already 0 in the fiber quotient" in text
assert "Fiber-to-Global Injection Lemma" in text
