# Quantum Galileo Interferometer: gravity-model compatibility audit

**Status:** `EXPERIMENTAL_BENCHMARK_IDENTIFIED_MODEL_SPECIFIC_PREDICTION_NOT_YET_DERIVED`  
**Date:** 2026-10-11  
**Repository:** `chronos-urf-rr`  
**Scope:** Compare the existing Regge–Wheeler / Chronos gravity frontier with the 2026 quantum free-fall phase experiment without treating compatibility as evidence for a new theory. The action-specific DFM–MKC comparison is recorded in the [DFM–MKC QGI audit](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/blob/main/docs/status/QGI_FREEFALL_PHASE_DFM_MKC_AUDIT_2026_10_11.md).

## 1. Experimental benchmark

Dobkowski et al., “Observation of the quantum phase of free fall and the consistency with the equivalence principle,” *Science Advances* 12 (2026), DOI: [10.1126/sciadv.aec8045](https://doi.org/10.1126/sciadv.aec8045).

The Quantum Galileo Interferometer (QGI) places ultracold rubidium matter waves into two arms: one is held approximately stationary in the laboratory frame by the apparatus, while the other undergoes ballistic free fall. The arms are recombined and their relative quantum phase is measured. The reported phase agrees with the predicted quantum free-fall phase in the tested low-energy regime [primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13537235/) and [Oxford research summary](https://www.physics.ox.ac.uk/news/scientists-observe-einsteins-gravity-quantum-world).

This is an experimental measurement of a predicted matter-wave phase. The authors describe it as a test of the interface between quantum theory and gravity; it does **not** demonstrate a unified quantum-gravity theory or establish that gravity itself is quantized [primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13537235/).

## 2. Standard-theory reference

The primary paper gives the gauge phase relating the Newtonian/laboratory and freely falling wavefunctions as
\[
\varphi_{\rm gauge}(z,t)=\frac{m}{\hbar}\left(-\frac{g^2t^3}{6}-gzt\right),
\]
in its stated convention (Eq. 1). For the idealized symmetric ballistic segment with endpoints at times \(\pm T\), it gives the relative ballistic phase \(\varphi_{\rm ballistic}=-mg^2T^3/(3\hbar)\) (Eq. 2). The actual QGI observable includes the magnetic-gradient kicks and pulse timing; the paper's full interferometer expression, not the gauge phase alone, must be used for quantitative comparison. Source: [Dobkowski et al., primary paper, Eqs. (1)–(4)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13537235/).

The cubic time dependence is the characteristic free-fall signature. These are standard-theory expressions, not new results of Chronos. The earlier shorthand \(m(g^2T^3/6+gzT)/\hbar\) gives the magnitude of the gauge-phase terms under a sign convention, not the complete measured QGI phase.

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

1. O. Dobkowski et al., “Observation of the quantum phase of free fall and the consistency with the equivalence principle,” *Science Advances* 12(36), eaec8045 (2026), [primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13537235/), [DOI](https://doi.org/10.1126/sciadv.aec8045). Gauge phase and idealized ballistic phase: Eqs. (1)–(2); full apparatus-specific phase is developed later in the article and supplement.
2. University of Oxford, [research summary](https://www.physics.ox.ac.uk/news/scientists-observe-einsteins-gravity-quantum-world), for experimental context and limits.
3. Chronos flagship formalization: [`ReggeWheelerFlagshipExactResidual.lean`](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/main/lean/Chronos/Frontier/ReggeWheelerFlagshipExactResidual.lean).
