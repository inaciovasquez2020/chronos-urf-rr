# Chronos Prefix-Conditioning Embedding

Status: CONDITIONAL_PREFIX_EMBEDDING_REDUCTION

## Boundary

This file records a conditional replacement for the rejected leave-one-out embedding step.

It does not assert unconditional theorem-level closure.
It does not prove the terminal Chronos lower bound.
It does not prove \(P\ne NP\).
It does not replace the remaining requirement that the prefix embedding be implemented for the exact repository search distribution.
It preserves frontier status unless the exact prefix pushforward and protocol simulation are separately verified.

## Replacement

The false leave-one-out target

\[
\mathbb E_J\!\left[
I(X_J;T\mid Y,X_{-J},J)
+
I(Y_J;T\mid X,Y_{-J},J)
\right]
\le
\frac1n IC_{\mu_n}(\Pi)
\]

is replaced by prefix conditioning.

Sample public randomness

\[
\sigma\sim \mathrm{Unif}(S_n).
\]

For transcript \(T\) of \(\Pi\), define

\[
\alpha_i^\sigma
:=
I(X_{\sigma(i)};T\mid Y,X_{\sigma(<i)}),
\]

\[
\beta_i^\sigma
:=
I(Y_{\sigma(i)};T\mid X,Y_{\sigma(<i)}).
\]

By the chain rule,

\[
I(X;T\mid Y)
=
\sum_{i=1}^n
I(X_{\sigma(i)};T\mid Y,X_{\sigma(<i)}),
\]

\[
I(Y;T\mid X)
=
\sum_{i=1}^n
I(Y_{\sigma(i)};T\mid X,Y_{\sigma(<i)}).
\]

Therefore

\[
IC_{\mu_n}(\Pi)
=
I(X;T\mid Y)+I(Y;T\mid X)
=
\sum_{i=1}^n
\mathbb E_\sigma[
\alpha_i^\sigma+\beta_i^\sigma].
\]

Equivalently, for \(I\sim\mathrm{Unif}([n])\) independent of \(\sigma\),

\[
\mathbb E_{\sigma,I}
[
\alpha_I^\sigma+\beta_I^\sigma
]
=
\frac1n IC_{\mu_n}(\Pi).
\]

## Prefix Embedding Target

Embed AND into a uniformly random prefix-coordinate contribution.

Let

\[
H:=\sigma(I),
\qquad
P_X:=X_{\sigma(<I)},
\qquad
P_Y:=Y_{\sigma(<I)}.
\]

The prefix embedding uses public randomness \((\sigma,I,P_X,P_Y)\) and maps

\[
(a,b)\mapsto (X,Y)
\]

so that

\[
X_H=a,
\qquad
Y_H=b,
\]

and the suffix coordinates are sampled from the exact conditional law

\[
\mu_n\bigl(
X,Y
\mid
X_{\sigma(<I)}=P_X,\,
Y_{\sigma(<I)}=P_Y,\,
X_H=a,\,
Y_H=b
\bigr).
\]

The induced AND transcript is

\[
T_Q:=T_\Pi(X,Y).
\]

## Conditional Embedding Lemma

If the exact prefix sampler exists for the repository distribution \(\mu_n\), and if it preserves the AND input law \(\zeta\), then

\[
Q=\mathrm{PrefixEmb}_n(\Pi)
\in
\mathsf{Prot}_\varepsilon(\mathrm{AND})
\]

and

\[
IC_\zeta(Q)
\le
\mathbb E_{\sigma,I}
[
\alpha_I^\sigma+\beta_I^\sigma
]
=
\frac1n IC_{\mu_n}(\Pi).
\]

Thus

\[
\boxed{
IC_\zeta(\mathrm{PrefixEmb}_n(\Pi))
\le
n^{-1}IC_{\mu_n}(\Pi)
}
\]

conditionally on the exact prefix pushforward construction.

## Consequence

With

\[
\gamma_\varepsilon:=\frac{(1-2\varepsilon)^2}{12},
\]

the AND information lower bound gives

\[
IC_\zeta^\varepsilon(\mathrm{AND})
\ge
\gamma_\varepsilon.
\]

Hence, conditionally,

\[
IC_{\mu_n}^{\varepsilon}(\mathrm{Search}_{F_n})
\ge
\gamma_\varepsilon n.
\]

Using the repository constant

\[
C_{k,5,k+1}=2^{8k}k^{2k}5^{3k},
\]

one gets

\[
T_n
\ge
\frac{(1-2\varepsilon)^2}
{12\cdot 2^{8k}k^{2k}5^{3k}}\,n.
\]

Therefore, conditionally,

\[
\boxed{
T_n=\Omega_k(n).
}
\]

## Minimal Remaining Object

\[
\boxed{
\mathrm{PrefixEmb}_{n\#}\zeta=\mu_n
\text{ on the exact repository search distribution.}
}
\]

