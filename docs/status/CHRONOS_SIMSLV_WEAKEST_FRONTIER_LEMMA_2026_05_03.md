# Chronos / SiMSLV Weakest Frontier Lemma

Status: CONDITIONAL_FRONTIER  
Date: 2026-05-03  
Boundary: FRONTIER_OPEN preserved.  
Scope: finite-patch SiMSLV / H4.1-FGL local span replacement.

## Objects

Let

\[
X:=X(P),
\qquad
\Pi:=\Pi_{k,R,B}(P),
\qquad
\mathcal U:=\mathcal U_{R,B}(P).
\]

Define

\[
x\sim_{\mathcal U}y
\quad\Longleftrightarrow\quad
\forall U\in\mathcal U,\quad x|_U=y|_U.
\]

Define

\[
x\sim_{\Pi}y
\quad\Longleftrightarrow\quad
\tau_{\Pi}(x)=\tau_{\Pi}(y).
\]

## Weakest Frontier Lemma

The exact weakest condition needed for the unaugmented finite-patch span closure is

\[
\boxed{
\sim_{\mathcal U}\subseteq \sim_{\Pi}.
}
\]

Equivalently,

\[
\boxed{
\tau_{\mathrm{cyl}}(x)=\tau_{\mathrm{cyl}}(y)
\Longrightarrow
\tau_{\Pi}(x)=\tau_{\Pi}(y).
}
\]

Equivalently, there exists a factorization map

\[
\rho:\tau_{\mathrm{cyl}}(X(P))\to\Pi_{k,R,B}(P)
\]

such that

\[
\boxed{
\tau_{\Pi}=\rho\circ\tau_{\mathrm{cyl}}.
}
\]

## Conditional Span Closure

Assume

\[
\boxed{
\sim_{\mathcal U}\subseteq \sim_{\Pi}.
}
\]

Then

\[
\Pi_{k,R,B}(P)\preceq\Pi^{\mathrm{cyl}}_{k,R,B}(P).
\]

Define

\[
D^{\mathrm{corr}}_{k,R,B}(P)
:=
\left\{
d\in D_{\mathrm{full}}(P):
\exists A\in\Pi^{\mathrm{cyl}}_{k,R,B}(P)
\text{ such that }
\operatorname{supp}(d)\subseteq s(A)
\right\}.
\]

Then

\[
\boxed{
\operatorname{span}_{\mathbb Q}
\operatorname{Proj}_{\Pi}
D^{\mathrm{corr}}_{k,R,B}(P)
=
\mathbb Q^{\Pi_{k,R,B}(P)}.
}
\]

Hence

\[
\boxed{
\operatorname{rank}_{\mathbb Q}
\mathcal C^{\mathrm{corr}}_{k,R,B}(P)
=
|\Pi_{k,R,B}(P)|.
}
\]

## Exact Obstruction

The obstruction to unaugmented closure is exactly the existence of

\[
\boxed{
x,y\in X(P):
x\sim_{\mathcal U}y
\quad\text{and}\quad
x\not\sim_{\Pi}y.
}
\]

If no such pair exists, the original unaugmented finite-patch span closure holds.

If such a pair exists, the missing projected character is represented by

\[
\boxed{
1_{\tau_{\Pi}(x)}-1_{\tau_{\Pi}(y)}
\in
\mathbb Q^{\Pi_{k,R,B}(P)}
}
\]

outside the generated projected span

\[
\operatorname{span}_{\mathbb Q}
\operatorname{Proj}_{\Pi}
D^{\mathrm{corr}}_{k,R,B}(P).
\]

## Boundary

This document records a conditional frontier criterion only.

It does not assert unconditional Chronos closure.

It does not assert theorem-level H4.1/FGL closure.

It does not assert that the obstruction pair is absent.

It does not assert that the original unaugmented cylinder family is complete.

It preserves FRONTIER_OPEN status.
