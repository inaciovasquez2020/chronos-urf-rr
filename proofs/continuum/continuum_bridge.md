# Proof Skeleton: Continuum Bridge

## Definitions

Let \((X,\mu)\) be a finite measure space.

For a finite family \(\mathcal F = (f_i)_{i=1}^m \subset L^2(X,\mu)\), define:
\[
\operatorname{supp}(f_i) = \{x \in X : f_i(x) \ne 0\},
\]
\[
S(\mathcal F) = \sum_{i=1}^m \mu(\operatorname{supp}(f_i)),
\]
\[
N_{\mathcal F}(x) = \sum_{i=1}^m 1_{\operatorname{supp}(f_i)}(x),
\]
\[
\Omega(\mathcal F) = \int_X N_{\mathcal F}(x)^2\, d\mu(x),
\]
\[
G(\mathcal F) = \sum_{i,j=1}^m |\langle f_i,f_j\rangle|^2.
\]

## Lemma 1: Support expansion identity

\[
\Omega(\mathcal F)
=
S(\mathcal F)
+
\sum_{i \ne j} \mu(\operatorname{supp}(f_i)\cap \operatorname{supp}(f_j)).
\]

### Proof
Expand \(N_{\mathcal F}(x)^2\) pointwise and integrate.

## Lemma 2: Controlled overlap consequence

If \(\Omega(\mathcal F) \le K S(\mathcal F)\), then
\[
\sum_{i \ne j} \mu(\operatorname{supp}(f_i)\cap \operatorname{supp}(f_j))
\le (K-1)S(\mathcal F).
\]

### Proof
Apply Lemma 1 and rearrange.

## Lemma 3: Diagonal Gram lower bound

If \(\|f_i\|_2 \ge \alpha\) for all \(i\), then
\[
G(\mathcal F) \ge \alpha^4 m.
\]

### Proof
\[
G(\mathcal F)
=
\sum_{i,j} |\langle f_i,f_j\rangle|^2
\ge
\sum_i |\langle f_i,f_i\rangle|^2
=
\sum_i \|f_i\|_2^4
\ge
\alpha^4 m.
\]

## Theorem: Continuum rigidity lower bound

Assume:
1. \( \|f_i\|_2 = 1 \) for all \(i\),
2. \( \mu(\operatorname{supp}(f_i)) \ge s_0 > 0 \),
3. \( \Omega(\mathcal F) \le K S(\mathcal F) \).

Then:
\[
S(\mathcal F) \ge s_0 m,
\qquad
G(\mathcal F) \ge m.
\]

### Proof
The support bound gives \(S(\mathcal F) \ge s_0 m\). The Gram bound is Lemma 3 with \(\alpha=1\).

## Realization map from discrete data

For a finite vertex set \(V\) with counting measure and subsets \(A_i \subseteq V\), define
\[
f_i = \frac{1_{A_i}}{\sqrt{|A_i|}}.
\]
Then
\[
\|f_i\|_2 = 1,
\qquad
\operatorname{supp}(f_i)=A_i,
\qquad
\Omega(\mathcal F)=\sum_{v \in V} \left(\sum_i 1_{A_i}(v)\right)^2.
\]

Hence any discrete support-overlap theorem gives a continuum witness family with the same deterministic obstruction profile.

## Endpoint

The continuum bridge is complete once the discrete layer produces a witness family with:
- nontrivial support mass,
- bounded overlap energy,
- admissible normalization.

No probabilistic input is required in the bridge itself.
