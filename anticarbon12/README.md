# Anti-carbon-12 feasibility framework

**Status: EXPLORATORY / NOT A PREDICTION**

This directory isolates a literature-and-data feasibility study of anti-carbon-12 production from the repository's established Chronos/URF proof surfaces. It does not alter or extend any Chronos theorem, and it makes no claim that anti-carbon-12 has been observed or that a production yield has been established.

## Research question

Can a defensible, uncertainty-aware estimate for anti-carbon-12 production be obtained by validating a light-antinucleus coalescence model against published data and then supplying a justified carbon-12 nuclear-overlap model?

The existence of antimatter and the possibility of an anti-carbon nucleus do not establish a measurable production rate. An extrapolation from mass number A=2–4 to A=12 is not accepted merely because a formula can be evaluated at A=12.

## Scope and stopping rule

Start with a reproducible data audit, not a yield calculation. Stop and report the missing object whenever a gate below fails. Do not turn a failed gate into a numerical prediction.

### Gate 0 — provenance and literature

- Record the exact paper/version, dataset or figure, DOI/URL, access date, units, collision system, energy, event/centrality class, and kinematic cuts.
- Distinguish measured points, digitized points, model curves, and values transcribed from tables.
- Preserve source files and SHA-256 hashes; do not silently replace a source or hand-edit extracted values.
- Search the literature for direct anti-carbon or heavier antinucleus limits and measurements before making a novelty claim.

Primary starting points:
- ALICE, *Production of light nuclei and antinuclei in pp collisions at sqrt(s) = 13 TeV*, JHEP 01 (2022) 106, https://doi.org/10.1007/JHEP01(2022)106
- Official ALICE figure archive: https://alice-figure.web.cern.ch/node/20650
- ALICE B2 data figure: https://alice-figure.web.cern.ch/system/files/figures/lbariogl/cB2data_3.pdf
- ALICE B3 data figure: https://alice-figure.web.cern.ch/system/files/figures/lbariogl/cB3data_3.pdf
- Argonne Wigner-distribution resources: https://www.phy.anl.gov/theory/research/wigner/

These are starting sources, not proof that every required datum or nuclear wavefunction input is available.

### Gate 1 — extract and replay A=2–4 data

- Extract B2 and B3 points with x/y values, statistical uncertainties, systematic uncertainties, correlations where published, and the relevant kinematic bin definitions.
- Keep digitization uncertainty separate from experimental uncertainty.
- Recompute plotted ratios from source tables where possible; otherwise record the digitization procedure and tolerances.
- Compare the extracted points with the published values and figures. Save a machine-readable table and a receipt containing source hashes, extraction method/version, row counts, and residual checks.
- Do not combine independent errors in quadrature if the publication supplies correlated components or covariance information.

**Pass condition:** independent replay reproduces all selected data points within a declared, justified extraction tolerance, with uncertainty categories and units intact.

### Gate 2 — validate the light-nucleus model

- Implement the exact convention and units used by the selected publication before comparing model curves with B2/B3.
- State every source-size, wavefunction, coalescence, spin/statistical, and kinematic assumption.
- Fit or calibrate only on a declared subset; retain held-out bins for a predictive check.
- Report residuals and uncertainty coverage, not only a visual match.
- Compare plausible source and wavefunction choices. A model that reproduces A=2 but fails A=3 is not approved for extrapolation.

**Pass condition:** a versioned implementation independently reproduces the published A=2–4 comparison to declared tolerances and reports its domain of validity and failure cases.

### Gate 3 — establish the A=12 nuclear input

- Specify what nuclear object the calculation requires: a complete many-body wavefunction or a demonstrably valid approximation to the relevant 12-body phase-space overlap.
- Document the Hamiltonian, state, normalization, antisymmetrization, spin/isospin structure, and uncertainty.
- Do not treat a one-body density or one-body Wigner distribution as sufficient evidence for the complete 12-body overlap without a derivation connecting them.
- State the approximation error and how it propagates into the yield. If this cannot be bounded or credibly estimated, stop.

**Pass condition:** the required A=12 overlap is defined, sourced, normalized, and independently checkable, with a stated uncertainty model.

### Gate 4 — conditional yield and uncertainty

Only after Gates 0–3 pass:
- Define the collision system, energy, event normalization, acceptance, efficiency, and kinematic integration range.
- Propagate experimental, digitization, source-model, nuclear-wavefunction, and numerical uncertainties separately before combining them according to a justified dependence model.
- Report sensitivity to alternative admissible model choices and a prediction interval or upper limit, not an unsupported point estimate.
- Include a machine-readable receipt with code/version, input hashes, parameter values, units, random seeds if applicable, and independent replay instructions.

**Pass condition:** independent rerun reproduces the reported output and uncertainty; no essential input is an untracked placeholder.

## Required status vocabulary

- `NOT_STARTED`: no artifact yet.
- `BLOCKED`: a required source, definition, or independent check is missing.
- `FAIL`: a specified validation check did not pass.
- `PASS_BOUNDED`: only the explicitly named gate passed.
- `CONDITIONAL`: result depends on enumerated assumptions.
- `PREDICTION_VALIDATED_WITHIN_SCOPE`: reserved for a yield that passes every gate and independent replay. This status does not imply experimental detection.

Every receipt must distinguish observed source data, digitized data, model output, and assumptions. A passing software test validates only the assertions it checks.

## Initial status

- Gate 0: `BLOCKED` — literature and source inventory still needs a dated, reproducible audit.
- Gate 1: `NOT_STARTED` — no point-level B2/B3 extraction receipt has been produced here.
- Gate 2: `NOT_STARTED` — no independent A=2–4 model replay has been produced here.
- Gate 3: `BLOCKED` — a validated, uncertainty-controlled A=12 many-body overlap has not been established here.
- Gate 4: `BLOCKED` — no defensible anti-carbon-12 yield is authorized.

**Current conclusion:** a bounded feasibility study is worth doing because its early gates can determine whether a credible extrapolation is possible. A numerical anti-carbon-12 production rate is not currently justified.

## Suggested artifact layout

As implementation begins, keep each stage independently replayable:

- `sources/manifest.json` — bibliographic metadata and source hashes.
- `data/b2_points.csv`, `data/b3_points.csv` — extracted values with units and uncertainty columns.
- `src/extract_figures.py` — deterministic extraction or transcription validation.
- `src/coalescence.py` — model equations with unit tests and explicit conventions.
- `src/validate_light_nuclei.py` — A=2–4 replay and held-out residual checks.
- `src/anticarbon_overlap.py` — only after a valid A=12 nuclear input is sourced.
- `receipts/` — per-gate JSON receipts and hashes.
- `tests/` — tests for units, source schema, residuals, failure paths, and receipt replay.

Do not create empty placeholder outputs that can be mistaken for completed evidence.


## Dated audit update — 2026-10-22

The source manifest and bounded audit receipt are in `sources/manifest.json` and `receipts/alice-pp13tev-source-audit-2026-10-22.json`.

- Gate 0: `PASS_BOUNDED` for identifying the primary paper, version, official figure links, kinematic context, and HEPData record. This is not a complete literature novelty search, and source-file SHA-256 hashes remain uncomputed because the source bytes were not retrieved.
- Gate 1: `BLOCKED`. The HEPData record was identified as `ins1928822`, but the current retrieval path returned HTTP 403. No B2/B3 point table was imported; no point counts, coordinates, uncertainties, digitization tolerance, or residuals are claimed.
- Gate 2: `BLOCKED` for independent replay. The paper-level comparison gives a concrete caution: its Gaussian deuteron model describes B2 comparatively well, but its Gaussian helion B3 prediction is almost a factor of two above the data at low pT/A, apart from the last interval. Thus the unqualified Gaussian A=3 baseline is not validated for extrapolation.
- Gate 3: `BLOCKED`. No normalized, independently checkable A=12 many-body phase-space overlap and uncertainty model has been established.
- Gate 4: `BLOCKED`. No anti-carbon-12 yield is authorized.

**Stop decision:** stop before A=12 and before yield computation. Continue only with obtaining the point-level HEPData export or a documented, calibrated figure digitization that keeps statistical, systematic, and digitization uncertainties distinct. The paper itself notes that the general B2 overlap recipe does not extend to B3 for arbitrary wave functions and that ab initio calculations are needed for those cases. A numerical formula evaluable at A=12 is not, by itself, evidence for a validated prediction.

Primary paper version reviewed: arXiv:2109.13026v2 (2022-04-05); published as JHEP 01 (2022) 106. The paper defines B_A using the invariant nucleus spectrum divided by the A-th power of the invariant proton spectrum evaluated at pT/A. In its Appendix A, B2 is expressed as an overlap integral of the deuteron Wigner density and the two-nucleon source correlation for a Gaussian source. These conventions must be implemented explicitly before any numerical comparison.


### Publisher-PDF access correction — 2026-10-22

The version-of-record PDF is accessible through the Springer web PDF viewer (32 pages); Figure 2 is on PDF page index 9 and Figure 3 on index 10. The PDF confirms the axes, plotted uncertainty boxes/bars, and the paper's own model comparison. However, the binary PDF could not be downloaded into the working container, so no SHA-256 or programmatic pixel calibration was performed.

**Provenance correction:** `ins1928822` is now treated as an unverified candidate identifier, not as a confirmed HEPData record. The direct candidate URL returned HTTP 403 and the search route could not be accessed through this retrieval path. No table payload or point-level values were retrieved. The earlier source manifest and receipts have been corrected accordingly.

The next viable path is a documented manual digitization from the publisher PDF, using axis calibration, retaining the image/screenshot provenance and digitization tolerance, and independently repeating the extraction. Until then, point-level numerical replay remains blocked. Do not call a screenshot-derived estimate exact or independently validated.
