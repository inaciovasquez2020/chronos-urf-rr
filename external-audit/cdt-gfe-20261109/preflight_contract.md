# CDT-SM-01 Stage 0 preflight — proposed, not implemented

**Status: OPEN / SYNTHETIC ONLY.** Frozen July 12 2026 v1 algorithm SHA-256: `4291599bea04eb267dc832ad673f22aff27a6a008cbb2ace96c2746ddafa4ccc`. Current draft v2: PR [#1335](https://github.com/inaciovasquez2020/chronos-urf-rr/pull/1335) at `93a32286f67c2ec6730fce832b1ecddc4fc05d49`, source Git blob `e40b4ca214073a66bc57e781e1b955bae8c87f5a`. Snapshot here is an audit fixture, **not** a promoted classifier.

## Frozen protocol requirements

- Exactly **16 ordered blocks**, four per blind code B1/B2/B3/B4. Fixed code order: `B1 B3 B2 B4 B2 B4 B1 B3 B3 B1 B4 B2 B4 B2 B3 B1`.
- Nominal duration 8 hours/block, at least **6 accepted hours per block**. Recording 16 `eta` values does **not** prove 16 authenticated six-hour blocks.
- Currently `run_start_rule.currently_authorized=false`; G1 (fabrication/inspection), G2 (magnetic dummy calibration), G3 (coupon manufacture/assays), G4 (analysis and blind lock) PENDING; G5 (16-block run) BLOCKED. Physical data and the authorized B-to-C mapping are absent.
- A result must never exceed `SINGLE_LAB_CANDIDATE_ONLY`, and independent replication remains required. **No physical claim has been made.**

## Proposed typed pre-execution contract (not yet approved)

1. `ProtocolLock(id,version,source_sha256,analysis_sha256)` verified against the frozen source; never rewrite locked v1.
2. `BlockRecord(index,blind_code,accepted_intervals,accepted_hours,quality_flags,inclusion_decision,data_digest,acquisition_id)` with authenticated time intervals and auditable exclusions; no missing, duplicated, reordered or unaudited blocks.
3. `MeasurementRecord(block_id,timestamp,eta,uncertainty,units,raw_source_digest)`, with a **reviewed and locked** measurement-to-block aggregation, finite numeric values, strictly positive finite uncertainty/threshold and finite derived statistics. Reject bool/string/nonfinite values; fail closed on overflow.
4. `UnblindingAuthorization(mapping_digest,approver,unlock_event)` authenticated independently of caller-supplied fixture mappings; `GateEvidence(G1..G5,certificates,authorization)` must not be inferred from user-supplied PASS strings.
5. Synthetic/physical outputs must use **disjoint types**: `SYNTHETIC_CANDIDATE_ONLY` and `SYNTHETIC_FIXTURE` for demonstrations; `BLOCKED_AUTHORIZATION` for physical requests lacking external approval. The wrapper on PR #1335 does not currently enforce this.
6. Review within-control cancellation: `C3=[+1e-4,-1e-4,0,0]` has mean zero. A robust dispersion/drift or outlier rule would alter acceptance criteria and requires a *separately locked statistical protocol*, not an arbitrary threshold inferred from `u_c`.

## Reproduced software findings

- Original v1 cross-null cancellation can falsely accept `C3=+1e-6,C4=-1e-6`; draft v2 rejects this pair.
- Draft v2 can accept `C1=+inf,C2=-inf`, infinite uncertainty, a negative threshold, and one observation/configuration.
- Finite extreme inputs may produce an unhandled `OverflowError` or an infinite computed difference.
- Within-control mean cancellation remains possible.
- CI in this evidence branch checks expected synthetic behaviors only, **not** safe production operation or authorized experimental completeness.

**Acceptance boundary:** `ISOLATED_TESTS := PASS`; `PRODUCTION_PREFLIGHT := OPEN`; `PHYSICAL_EXECUTION := NOT_AUTHORIZED`; `INDEPENDENT_STATISTICAL_REVIEW := OPEN`. Integration needs explicit code review, preflight provenance authority and protocol approval.
