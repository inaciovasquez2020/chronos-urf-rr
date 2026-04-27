# Theorem-level frontiers — 2026-04-27

Status: Conditional.

Source-level proof-hole inventory is closed, but theorem-level Chronos/H4.1 closure is not proved.

## Verified surfaces

- Source-level axiom/admit/sorry elimination: Proved.
- Petersen 2-lift finite-instance FGL certificate: Proved.
- Trusted 2R ball-cycle axiom: Removed.
- CycloneSignedLift admits: Discharged.

## Remaining theorem-level frontiers

### 1. General FGL row-separation

Status: Conditional.

Target:

\[
\forall x\in E,\quad x\notin W_{k,R,B}\oplus\langle 1\rangle
\Rightarrow
Mx\neq 0.
\]

Equivalent kernel form:

\[
\ker(M)\subseteq W_{k,R,B}\oplus\langle 1\rangle.
\]

Current proved surface:

- one Petersen 2-lift finite-instance certificate.

Missing object:

- uniform proof for all admissible finite patches \((k,R,B)\), or a complete exported matrix family with certified rank/kernel containment for each declared patch.

### 2. R1 Long-Chord Exclusion

Status: Conditional.

Target:

Long chords cannot collapse the finite-patch local witness quotient without being detected by the admissible test family.

Missing object:

- formal exclusion lemma connecting long-chord geometry to nonzero quotient/test response.

### 3. R2 Diameter-Separation Filling Obstruction

Status: Conditional.

Target:

Diameter-separated local cycles cannot be filled by bounded-radius local witnesses without producing a detectable obstruction.

Missing object:

- formal filling obstruction lemma for separated finite-patch cycle supports.

### 4. R3 Uniform Local-Type Capacity

Status: Conditional.

Target:

The admissible local-type/test family has sufficient uniform capacity to separate all non-witness finite-patch quotient directions.

Missing object:

- uniform local-type capacity bound independent of the particular finite patch instance.

## Non-claims

The following are not proved:

- General H4.1.
- General FGL row-separation.
- R1 Long-Chord Exclusion.
- R2 Diameter-Separation Filling Obstruction.
- R3 Uniform Local-Type Capacity.
- Unconditional Chronos/URF theorem-level closure.
