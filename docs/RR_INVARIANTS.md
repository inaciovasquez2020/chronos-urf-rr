# Chronos–URF RR Invariants

## Purpose
This document specifies the invariants enforced by the Chronos–URF
Reference Representation (RR).

The RR serves as the executable sanity layer ensuring that Chronos
results are operationally reproducible and structurally faithful to
URF invariants.

## Core Invariants

### R1. Reference Fidelity
RR outputs must be derivable from Chronos core definitions without
introducing auxiliary assumptions.

### R2. Determinism
Given identical inputs and manifests, RR execution is deterministic.

### R3. Normalization
All inputs are normalized via URF Spine conventions before evaluation.

### R4. Bounded Output
RR outputs must satisfy documented bounds (entropy, rank, or depth)
as stated in Chronos specifications.

### R5. Failure Visibility
Invariant violations must surface as explicit failures (CI or runtime),
never silent degradation.

## Position in Stack
URF Core → URF Spine → Chronos Core → Chronos–URF RR
