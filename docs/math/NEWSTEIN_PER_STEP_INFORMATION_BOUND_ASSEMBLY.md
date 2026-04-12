# Newstein Per-Step Information Bound Assembly

## Status
OPEN

## Statement
Let
\[
\iota:\bigoplus_i Q_i \hookrightarrow Q_{\mathrm{global}}
\]
be the injective residual fiber-to-global map. Then each admissible refinement step contributes at most the rank of one newly realized independent residual fiber class. Consequently, the information gain per step is bounded by the increment of the injected residual quotient rank. Equivalently, if \(\Delta_t\) denotes the rank gained at step \(t\), then
\[
\Delta_t \leq \operatorname{rank}(Q_{\mathrm{global}}^{(t)})-\operatorname{rank}(Q_{\mathrm{global}}^{(t-1)}).
\]

## Assembly inputs
1. Fiber-to-global injection assembly.
2. Rank monotonicity under admissible quotient refinement.
3. Definition of per-step information gain as newly realized independent quotient-rank contribution.

## Proof skeleton
1. By fiber-to-global injection assembly, every surviving residual fiber class remains nontrivial in the global quotient.
2. Therefore each newly realized independent residual class contributes a genuine increase in global quotient rank.
3. Rank monotonicity implies that a single admissible step cannot contribute more independent information than the quotient-rank increase realized at that step.
4. Hence the per-step information gain is bounded by the stepwise rank increment.
5. This is the required per-step information bound.

## Dependency edge
\[
\mathrm{PerStepInformationBound}
\Longrightarrow
\mathrm{AssemblyTheorem}.
\]
