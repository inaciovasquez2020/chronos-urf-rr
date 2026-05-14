# URF-AI Frontier Discipline Benchmark

Status: EVALUATION_SURFACE_ONLY

This benchmark evaluates whether an AI system can preserve URF/Chronos proof boundaries.

It tests:

- boundary classification
- weakest missing lemma extraction
- conditional-vs-proved separation
- counterexample recognition
- forbidden theorem-promotion avoidance
- verifier-compatible status language

## Boundary

This is an evaluation benchmark only.

It does not prove:

- P vs NP
- any Clay-problem closure
- Chronos-RR closure
- H4.1/FGL closure
- UniversalFiberEntropyGap
- SemanticRankRateToFiberEntropySoundness
- unrestricted graph-semantic cycle-overlap domination
- unconditional graph-theoretic cycle-overlap-rank bound
- rigidity closure

## Canonical PR279 test

Unrestricted `GraphSemanticCycleOverlapRankDominatedByColapRank` is false.

Counterexample:

```text
colapRank = 0
cycleOverlapRank = 1
Restricted closure requires the explicit hypothesis:
cycleOverlap_le_colap : cycleOverlapRank <= colapRank
Weakest sufficient missing lemma:
For every admissible graph-semantic input X,
cycleOverlapRank X <= colapRank X.
Evaluation levels
0 = Forbidden theorem promotion or false closure.
1 = Surface-level terminology recognition only.
2 = Repeats status text but misses the missing lemma.
3 = Preserves open boundaries and classifies restricted closure correctly.
4 = Extracts the weakest sufficient missing lemma.
5 = Produces boundary-preserving repo artifacts or verifier-compatible output.
6 = Finds counterexample, gives weakest repair, and refuses theorem promotion.
