# β13 propagation-channel volume–Hamiltonian commutator boundary

```text
STATUS := conditional structural reduction
```

Let \(S_0\) satisfy

\[
\widehat V^{RS}S_0=\nu_vS_0,\qquad \nu_v>0.
\]

For the unresolved constituents

\[
S_{r,\epsilon}=S_{\beta_{13}^{(r)},\epsilon},
\qquad r\in\{0,1\},
\]

assume

\[
\widehat V^{RS}S_{r,\epsilon}=0
\]

and define

\[
\Pi_r\widehat H_\epsilon^E[N]S_0
=
A_{r,\epsilon}[N]S_{r,\epsilon}.
\]

Then

\[
\begin{aligned}
\Pi_r[\widehat V^{RS},\widehat H_\epsilon^E[N]]S_0
&=
\widehat V^{RS}A_{r,\epsilon}[N]S_{r,\epsilon}
-\nu_vA_{r,\epsilon}[N]S_{r,\epsilon}
\\
&=
-\nu_vA_{r,\epsilon}[N]S_{r,\epsilon}.
\end{aligned}
\]

Therefore,

\[
\boxed{
\Pi_{\beta_{13}}
[\widehat V^{RS},\widehat H_\epsilon^E[N]]S_0
=
-\nu_v\sum_{r=0}^{1}
A_{r,\epsilon}[N]S_{r,\epsilon}
}.
\]

If later

\[
A_{r,\epsilon}[N]
=
c_E(\kappa,\hbar,\gamma)\frac{N(v)}{\epsilon}P_r
\]

and

\[
\widetilde\Psi(S_{r,\epsilon})
=
a_r\epsilon+O(\epsilon^2),
\]

then

\[
\lim_{\epsilon\to0}
\widetilde\Psi\!\left(
\Pi_{\beta_{13}}
[\widehat V^{RS},\widehat H_\epsilon^E[N]]S_0
\right)
=
-\nu_vc_E(\kappa,\hbar,\gamma)N(v)
(P_0a_0+P_1a_1).
\]

```text
BOUNDARY := exact tensor projections P_0 and P_1 are not derived
BOUNDARY := c_E(κ,ℏ,γ) is not fixed
BOUNDARY := PATCH_1 is not reapplied
BOUNDARY := Euclidean anomaly-free closure on a modified habitat is not proved
BOUNDARY := no Lorentzian Hamiltonian or mixed commutator is defined

STRONGEST_PROVED_RESULT :=
Under the stated branch assumptions, the β13 projection of [V_RS,H_E]
equals minus the parent volume eigenvalue times the projected child amplitude.

WEAKEST_UNRESOLVED_GAP :=
Derive P_0 and P_1 directly from the defining β13 tensor contraction.

NEXT_BOUNDED_PROBLEM :=
Compute the two exact β13 constituent projections before modifying the habitat.
```
