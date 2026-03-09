# Cycle-Overlap Rank Empirical Note

## Definition

For a finite graph \(G=(V,E)\), let \(A\) be the cycle-edge incidence matrix over \(\mathbb{F}_2\) built from a chosen cycle basis. Define

\[
\mathrm{COR}(G) := \operatorname{rank}_{\mathbb{F}_2}(A).
\]

## Empirical Observation

For random \(4\)-regular graphs with \(n \in \{200,400,800,1200\}\),

\[
\frac{\mathrm{COR}(G)}{n} \approx 1.
\]

Observed values:

- \(n=200\): \(1.005\)
- \(n=400\): \(1.0025\)
- \(n=800\): \(1.00125\)
- \(n=1200\): \(1.0008333\)

## Structural Interpretation

The cycle-basis incidence vectors are empirically linearly independent up to negligible defect. Hence

\[
\mathrm{COR}(G)=\Omega(n)
\]

on these families.

## Program Relevance

Conditional bridge:

\[
\mathrm{COR}(G)=\Omega(n)
\Longrightarrow
\#\mathrm{FO}^k\text{-local types}=\Omega(n)
\Longrightarrow
ED(G)=\Omega(n).
\]

The remaining unproved step is the rigidity bridge from linear cycle-overlap rank to forced local type diversity.

## Adversarial Gap

Not yet excluded:

- random lifts with persistent WL\(^2\)/FO\(^2\) collisions,
- high-girth expanders with hidden cycle-overlap concentration,
- cover families with large cycle rank but low visible local diversity.
