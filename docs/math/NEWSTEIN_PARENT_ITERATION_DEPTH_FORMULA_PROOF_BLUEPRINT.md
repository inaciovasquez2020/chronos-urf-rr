# Newstein Parent-Iteration Depth Formula Proof Blueprint

Status: OPEN

## Objective
For every vertex \(v \in B_R(r)\) and every \(j \in \mathbb{N}\),
\[
d(\eta^j(v))=\max(d(v)-j,0).
\]

## Inputs
- `MetricDepthCoincidence^thm`
- `ParentDepthDecrement^thm`

## Base case
At \(j=0\),
\[
d(\eta^0(v))=d(v)=\max(d(v)-0,0).
\]

## Inductive step
Assume
\[
d(\eta^j(v))=\max(d(v)-j,0).
\]

### Case 1
If \(d(v)\le j\), then
\[
d(\eta^j(v))=0,
\]
so \(\eta^j(v)=r\), hence
\[
d(\eta^{j+1}(v))=0=\max(d(v)-(j+1),0).
\]

### Case 2
If \(d(v)>j\), then
\[
d(\eta^j(v))=d(v)-j>0.
\]
Apply `ParentDepthDecrement^thm`:
\[
d(\eta^{j+1}(v))=d(\eta^j(v))-1=d(v)-(j+1).
\]
Thus
\[
d(\eta^{j+1}(v))=\max(d(v)-(j+1),0).
\]

## Conclusion
By induction on \(j\),
\[
d(\eta^j(v))=\max(d(v)-j,0).
\]

## Role
This yields
\[
d(\eta^R(v))=0,
\]
hence
\[
\eta^R(v)=r,
\]
which is the core step in `ParentIterationToRoot^thm`.
