# Quantum Galileo Interferometer: gravity-model compatibility audit

**Status:** `EXPERIMENTAL_BENCHMARK_IDENTIFIED_MODEL_SPECIFIC_PREDICTION_NOT_YET_DERIVED`  
**Date:** 2026-10-11  
**Repository:** `chronos-urf-rr`  
**Scope:** Compare the existing Regge–Wheeler / Chronos gravity frontier with the 2026 quantum free-fall phase experiment without treating compatibility as evidence for a new theory. The action-specific DFM–MKC comparison is recorded in the [DFM–MKC QGI audit](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/blob/main/docs/status/QGI_FREEFALL_PHASE_DFM_MKC_AUDIT_2026_10_11.md).

## 1. Experimental benchmark

Dobkowski et al., “Observation of the quantum phase of free fall and the consistency with the equivalence principle,” *Science Advances* 12 (2026), DOI: [10.1126/sciadv.aec8045](https://doi.org/10.1126/sciadv.aec8045).

The Quantum Galileo Interferometer (QGI) places ultracold rubidium matter waves into two arms: one is held approximately stationary in the laboratory frame by the apparatus, while the other undergoes ballistic free fall. The arms are recombined and their relative quantum phase is measured. The reported phase has the characteristic cubic dependence on free-fall time and agrees with the equivalence-principle prediction in the tested low-energy regime.

This is an experimental measurement of a predicted matter-wave phase. It does **not** demonstrate a complete quantum-gravity theory, establish that gravity is quantized, or by itself indicate a deviation from standard gravity.

## 2. Standard-theory reference

For the coordinate and phase convention used in the cited treatment, the free-fall phase is expressed as

\[
\Delta\phi_{\rm std}(T,z)
= \frac{m}{\hbar}\left(\frac{g^2 T^3}{6}+gzT\right),
\]

where $m$ is the atomic mass, $g$ is the local gravitational acceleration, $T$ is the free-fall time parameter, and $z$ is the corresponding initial vertical coordinate in that convention. Sign and reference-arm conventions can change the sign of a reported relative phase; comparisons must use the paper's full pulse sequence and definitions, not this expression in isolation.

The dimensions are consistent: the bracket has units of action per unit mass, so multiplication by (m/\hbar) yields a dimensionless phase. The $T^3$ term is the distinctive free-fall signature. This formula is a standard-theory benchmark, not a new result of Chronos.

## 3. Comparison with the current Chronos flagship

The current formal flagship proves the algebraic identity

\[
(L-\lambda U)(\Psi_0+\lambda\Psi_1)
=-\lambda^2 U\Psi_1,
\]

given the supplied background equation (L\Psi_0=0) and first-order response equation (L\Psi_1=U\Psi_0). Its exactness criterion is that the second insertion (U\Psi_1) vanishes when \(\lambda\ne0\).

That result is an operator-residual identity for a first-order deformation. It is not yet an atom-interferometer calculation. The existing flagship does not supply the following bridge:

1. A specified modified or effective gravitational action and its metric/background solution for the QGI regime.
2. A derivation of the nonrelativistic matter-wave Hamiltonian (or equivalent phase evolution) from that action, including the atom's coupling to the metric and any additional fields.
3. The phase accumulated on each actual QGI arm, including the support/holding force, pulse phases, and reference conventions.
4. A model-specific predicted phase shift relative to the standard result, with units and parameter values fixed independently of the measured outcome.

Therefore **no distinct numerical prediction from the current Chronos flagship can presently be calculated from the repository's proved equations alone**. Treating the exact quadratic residual as a QGI phase correction would be an invalid identification of different mathematical objects.

## 4. Correct conditional route to a discriminating prediction

If a candidate theory reduces in the experiment's regime to a nonrelativistic Hamiltonian with a potential correction \(\delta\Phi\), a preliminary potential-only contribution would have the form

\[
\delta\phi_{\rm pot}
=-\frac{m}{\hbar}\int_0^{\mathcal T}
\left[
\delta\Phi(x_{\rm fall}(t),t)
-\delta\Phi(x_{\rm ref}(t),t)
\right]dt,
\]

subject to the theory's sign convention and the full interferometer phase accounting. Here \(\mathcal T\) is the complete evolution interval, and the trajectories are the experimentally controlled free-fall and reference arms. This is only a conditional bookkeeping formula: it omits any changes to kinetic terms, metric couplings, internal-state phases, and control-pulse phases unless those are derived to be negligible.

A valid comparison must then:
- derive the correction from the candidate action rather than choose it to fit the result;
- use the published geometry, timing, calibration, and uncertainty budget;
- compute the same observable and convention as the experiment;
- compare the predicted residual with the reported uncertainty and systematic errors;
- retain the standard-theory result as the null model.

A nonzero expression is not sufficient: it must be well-defined, independently parameterized, and large enough to distinguish from the experimental uncertainty.

## 5. Finding and boundary

**Finding:** The QGI result is a useful external benchmark for the gravity program, but it does not currently validate or falsify the existing Regge–Wheeler residual theorem. The relevant model-to-observable bridge has not been derived.

**Not established by this audit:**
- a new quantum-gravity law;
- a deviation from the equivalence principle;
- a QGI prediction from the Chronos flagship;
- an experimental constraint on a Chronos coupling;
- a non-GR observable or antigravity effect.

**Decision:** Do not add a fitted correction, invent a numerical bound, or modify the Lean theorem to imply experimental coverage. The next mathematically meaningful step is to derive the QGI-regime matter-wave phase from a fully specified candidate action. If the action or its QGI-limit equations are not yet available in the repository, stop at this boundary rather than manufacture a prediction.

## References

1. O. Dobkowski et al., “Observation of the quantum phase of free fall and the consistency with the equivalence principle,” *Science Advances* (2026), [doi:10.1126/sciadv.aec8045](https://doi.org/10.1126/sciadv.aec8045).
2. University of Oxford / ScienceDaily, “Scientists observe Einstein’s gravity in the quantum world for the first time,” 8 September 2026, [source](https://www.sciencedaily.com/releases/2026/09/260907201552.htm).
3. Chronos flagship formalization: [`ReggeWheelerFlagshipExactResidual.lean`](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/main/lean/Chronos/Frontier/ReggeWheelerFlagshipExactResidual.lean).
