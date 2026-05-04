# Chronos CPOL Type Gate — 2026-05-04

## Status

STATUS: CPOL_TYPE_GATE_CLOSED_ONLY

This artifact closes only the primitive Lean carrier/typeclass gate:

\[
T_{\mathrm{Chr}}:\mathbb N\to\mathrm{Type}.
\]

It does not prove theorem-level Chronos closure.

It does not prove H4.1/FGL closure.

It does not prove P vs NP.

## Lean Definition

\[
T_{\mathrm{Chr}}(n)\text{ is the singleton inductive carrier with constructor }\operatorname{base}.
\]

The Lean file proves:

\[
\operatorname{Nonempty}(T_{\mathrm{Chr}}(n)),
\]

a nonempty decidable equality instance object

\[
\operatorname{Nonempty}(\operatorname{DecidableEq}(T_{\mathrm{Chr}}(n))),
\]

and a canonical witness

\[
\operatorname{tChrCanonicalWitness}(n):T_{\mathrm{Chr}}(n).
\]

## Boundary

This closes only the typed primitive carrier gate.

It does not construct \(C_n^{\mathrm{Chr}}\).

It does not define \(P_{\mathrm{Chr}}\).

It does not prove CPDL.

It does not prove CCSL.

It does not define \(\nu_n\).

It does not define admissible observables.

It does not prove ChronosNativeFullRankAdmissibleTrace.

It does not prove ChronosCertificateEmbedding.

It does not prove theorem-level Chronos closure.

It does not prove H4.1/FGL closure.

It does not prove P vs NP.

## Next Missing Gate

\[
\boxed{\mathrm{CPDL}}
\]

Define a repository-native validity predicate

\[
P_{\mathrm{Chr}}:T_{\mathrm{Chr}}(n)\to\mathrm{Prop}
\]

and then form

\[
C_n^{\mathrm{Chr}}:=\{X:T_{\mathrm{Chr}}(n):P_{\mathrm{Chr}}(X)\}.
\]

## Machine-Check Tokens

CHRONOS_CPOL_TYPE_GATE

CPOL_TYPE_GATE_CLOSED_ONLY

T_CHR_DEFINED

T_CHR_SINGLETON_CARRIER

NONEMPTY_PROVED

DECIDABLE_EQ_PROVED

CANONICAL_WITNESS_PROVED

DECIDABLE_EQ_NONEMPTY_PROVED

THEOREM_CLOSURE_FALSE

CHRONOS_CLOSURE_FALSE

H4_1_FGL_CLOSURE_FALSE

P_VS_NP_CLAIM_FALSE

NO_C_N_CHR_CONSTRUCTION

NO_CPDL_CLAIM

NO_CCSL_CLAIM

NO_CERTIFICATE_EMBEDDING_CLAIM
