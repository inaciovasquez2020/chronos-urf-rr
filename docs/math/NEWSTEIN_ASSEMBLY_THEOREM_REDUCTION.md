# Newstein Assembly Theorem Reduction

Status: OPEN

## Reduction statement
Assume:
\[
\mathrm{FiberQuotientRank},
\qquad
\mathrm{DirectSumIndependence},
\qquad
\mathrm{PerStepInformationBound},
\qquad
\mathrm{FiberToGlobalInjection}.
\]

Then the quotient-gap assembly theorem follows.

## Proof skeleton
Let \(Q_{\mathrm{fib}}\) denote the direct sum of the certified fiber quotients.
By FiberQuotientRank and DirectSumIndependence,
\[
\dim_{\mathbf F_2} Q_{\mathrm{fib}} \ge 4.
\]

By FiberToGlobalInjection, the canonical map
\[
Q_{\mathrm{fib}} \longrightarrow Q_{\mathrm{glob}}
\]
is injective. Therefore
\[
\dim_{\mathbf F_2} Q_{\mathrm{glob}} \ge 4.
\]

By PerStepInformationBound, each admissible refinement step leaks at most \(V_C\) information. Hence producing the required global quotient-gap forces the stated lower bound on admissible refinement cost.

## Output
AssemblyTheorem is reduced to FiberQuotientRank plus DirectSumIndependence plus PerStepInformationBound plus FiberToGlobalInjection.
