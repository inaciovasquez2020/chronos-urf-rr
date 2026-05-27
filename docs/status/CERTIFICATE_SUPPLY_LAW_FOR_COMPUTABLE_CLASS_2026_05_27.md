# Certificate Supply Law for Computable Class — 2026-05-27

Status: `CERTIFICATE_SUPPLY_FROM_EXPLICIT_LAW_ONLY`

This adds the weakest lawful certificate-supply bridge.

It proves that an explicit finite-support bridge law supplies certificates for every admissible `ComputableFiniteAdmissibleClass`.

## Proved

```lean
FiniteSupportBridgeLawForComputableClass →
FiniteSupportBridgeCertificateSupply
and therefore:
SemanticRankRate X <= FiberEntropyGap X
for admissible computable finite X, under the explicit law.
Remaining missing theorem
IntrinsicFiniteSupportBridgeLawProblem
That is, prove FiniteSupportBridgeLawForComputableClass from intrinsic admissibility structure rather than assume it as a law.
Does not prove
intrinsic finite-support bridge law
certificate supply theorem without explicit law
bridge for every computable finite admissible class from raw admissibility alone
stability under admissible limits
finite-support approximation theorem
unrestricted semantic-rank-to-fiber-entropy bridge
UniversalFiberEntropyGap
Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay problem
