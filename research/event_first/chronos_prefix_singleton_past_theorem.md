# First-two-prefix singleton-past criterion

## Setup
For a finite poset P of size N>=2, let e(P) count its linear extensions. Choose one uniformly at random. For x in P, pred_P(x) is its strict causal past.

## Exact theorem
The first two elements (X1,X2) are comparable if and only if pred_P(X2)={X1}. Consequently

Pr(X1 < X2 | P) = [sum_{x:pred(x)=empty} sum_{y:pred(y)={x}} e(P\{x,y})]/e(P).

Here e(P\{x,y}) counts linear extensions of the induced remainder. A pair (x,y) with singleton past {x} is automatically eligible as the first two elements, so every remainder extension contributes. No requirement about a prespecified geometric labeling enters.

### Proof
The first element of a linear extension is minimal, and the second is minimal after removal of the first. If X1<X2, every predecessor of X2 must occur earlier; the only prior element is X1, hence pred(X2)={X1}. Conversely singleton past implies X1<X2 and both can be the first two elements; appending any linear extension of the remainder gives a unique full extension. Divide the count by e(P).

## Independent finite check
Integer dynamic programming and structural identity were checked for all 1,2,7,40,357 naturally labeled posets at event counts 1,2,3,4,5. These counts are exact for the birth-ordered representation. Check was performed outside Lean.

## 4D diamond implication
For the N-event Minkowski sprinkling P_N, the first-two comparable probability is precisely the expectation over sprinklings of the above weighted singleton-past count. This reduces the open asymptotic problem to controlling linear-extension weights on pairs with a singleton past, not simply the total number of causal relations.

## Boundaries
NO proof that the ratio tends to zero or to the Minkowski pair target 1/10. Uniform sampling of all event pairs remains exactly 1/10 in expectation. The bounded simulation only reports N<=20; N=24 attempt exceeded the runtime cap and is INCOMPLETE, not verification.

Status: PROVED elementary identity; COMPUTATION_PASS finite check; sampling limit OPEN; Lean NOT_RUN; repository unchanged.