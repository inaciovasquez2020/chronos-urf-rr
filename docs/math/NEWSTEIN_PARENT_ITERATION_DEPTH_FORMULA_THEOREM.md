# Newstein Parent Iteration Depth Formula Theorem

Status: PROVED

## Statement
Let \(r\) be the distinguished root and let \(\eta\) denote the parent map on the rooted ball \(B_R(r)\).
For every vertex \(v \in B_R(r)\) and every integer \(n\) with \(0 \le n \le d(v,r)\),
\[
d\!\left(\eta^{\,n}(v), r\right)=d(v,r)-n.
\]

## Immediate consequence
Taking \(n=d(v,r)\) yields
\[
\eta^{\,d(v,r)}(v)=r.
\]

## Role in the Newstein closure chain
\[
\mathrm{ParentIterationDepthFormula}^{\mathrm{thm}}
\Longrightarrow
\mathrm{ParentIterationToRoot}^{\mathrm{thm}}
\Longrightarrow
\mathrm{TreeContractionHomotopy}^{\mathrm{thm}}
\Longrightarrow
\mathrm{RootedBallTrivialization}^{\mathrm{thm}}.
\]

## Weakest sufficient next proof object
This theorem is the current weakest sufficient theorem-level replacement target in the Newstein proof-closure queue.

## Proof status
Proved by induction using the one-step parent-depth decrement law.

