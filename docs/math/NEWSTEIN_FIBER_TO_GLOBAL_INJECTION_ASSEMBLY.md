# Newstein Fiber-to-Global Injection Assembly

## Status
OPEN

## Statement
Let the residual quotient decompose as a direct sum of independent fiber components \(\bigoplus_i Q_i\). Then the canonical map
\[
\iota:\bigoplus_i Q_i \hookrightarrow Q_{\mathrm{global}}
\]
is injective. Equivalently, no nontrivial residual fiber class vanishes after passage to the global quotient.

## Assembly inputs
1. Direct-sum independence assembly.
2. Definition of the canonical map from residual fiber classes to the global quotient.
3. Trivial-kernel criterion for injectivity.

## Proof skeleton
1. By direct-sum independence assembly, the residual fiber quotient is a direct sum of independent components.
2. Let \(x \in \bigoplus_i Q_i\) satisfy \(\iota(x)=0\) in \(Q_{\mathrm{global}}\).
3. If \(x \neq 0\), then some fiber component of \(x\) is nonzero.
4. Independence of the direct-sum decomposition forbids cancellation of a nonzero fiber component in the global quotient.
5. Hence \(x=0\).
6. Therefore \(\ker(\iota)=0\), so \(\iota\) is injective.

## Dependency edge
\[
\mathrm{FiberToGlobalInjection}
\Longrightarrow
\mathrm{PerStepInformationBound}.
\]
