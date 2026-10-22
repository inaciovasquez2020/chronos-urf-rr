# ALICE B2/B3 data status

No point-level CSV is committed yet. This is intentional: the HEPData record `ins1928822` was identified from the official ALICE publications page, but its current retrieval path returned HTTP 403. The official Figure 2 PDFs were accessible through the ALICE figure archive, and the arXiv paper's Figure 2 was visually inspected, but visual inspection alone is not a point-level extraction.

## Required schema for the eventual files

Each row must identify the plotted point and include at least:

- `observable`: `B2` or `B3`
- `species`: nucleus/antinucleus selection as defined by the source
- `multiplicity_class`: exact ALICE class
- `pt_per_A_GeV_c`
- `value`
- `stat_low`, `stat_high`
- `syst_low`, `syst_high`
- `visibility_scale_factor`: 1 unless the plotted curve was explicitly scaled for visibility
- `source_table_or_figure`
- `extraction_method`: tabulated, source-data export, or digitized
- `digitization_uncertainty` and `digitization_method` when digitized
- `source_sha256` only when the exact source bytes have actually been hashed

Preserve asymmetric uncertainties if the source provides them. Do not infer absent covariance information or replace a published uncertainty with a combined total. In Figure 2 the vertical bars represent statistical uncertainty and boxes represent systematic uncertainty; the B2 curves for HM II and HM III are scaled by factors shown in the legend for visibility. Undo these plotting factors before numerical comparisons.

## Why no manual estimates are supplied

The log-scaled y axes and overlaid error boxes make approximate visual coordinates inadequate for a claimed replay. If digitization becomes the fallback, retain the original image, record axis calibration points and software/version, estimate digitization uncertainty, and independently compare against a second extraction. Do not label digitized coordinates as official tabulated data.

## Current result

`BLOCKED`: point counts, numerical coordinates, statistical/systematic uncertainty columns, and residual checks remain unavailable. Do not run a coalescence fit or extrapolate to A=12 from an empty or approximate dataset.
