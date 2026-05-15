# Counting With Entropy-Mass To FiberMassBalance — 2026-05-15

## Closed bridge

```lean
CountingFiberSeparationWithEntropyMassFromNonProp I
→ FiberMassBalanceFromNonProp I
Meaning
Ordinary CountingFiberSeparationFromNonProp carries rank agreement and fiber-size agreement.
The enriched counting predicate adds the missing entropy-mass agreement:
W.fiber.entropyMass = I.entropyMass c
With that single additional datum, FiberMassBalanceFromNonProp follows.
Additional consequence
The enriched counting predicate also yields:
UniversalFiberEntropyGapFromNonProp I
through the existing counting-and-mass assembly theorem.
Boundary
This proves only the enriched-counting bridge.
It does not prove:
FiberMassBalance from ordinary CountingFiberSeparationFromNonProp alone
unrestricted UniversalFiberEntropyGap
unrestricted Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay problem
