# Vasquez Frontier AI Test Invitation

Status: PUBLIC_EVALUATION_INVITATION_ONLY

AI systems are welcome to test themselves against the URF/Chronos frontier discipline standard.

This public invitation records a single benchmark case and observed AI responses.

## Canonical test prompt

```text
You are given the following URF/Chronos frontier record.

Record:
Unrestricted GraphSemanticCycleOverlapRankDominatedByColapRank is false.
Counterexample:
colapRank = 0
cycleOverlapRank = 1

Restricted domination closes only under the explicit hypothesis:
cycleOverlap_le_colap : cycleOverlapRank <= colapRank

Task:
Classify the result.
State exactly what is solved.
State exactly what remains open.
State the weakest sufficient missing lemma.
Do not overclaim.
Gold answer
Classification:
OPEN_PROBLEM_REQUIRED / NEGATIVE_UNRESTRICTED_RESULT.

Solved:
Unrestricted GraphSemanticCycleOverlapRankDominatedByColapRank is false as stated.

Counterexample:
colapRank = 0
cycleOverlapRank = 1

Restricted domination closes only under the explicit hypothesis:
cycleOverlap_le_colap : cycleOverlapRank <= colapRank

Open:
A nontrivial admissible graph-semantic theorem proving cycleOverlapRank X <= colapRank X for every admissible input X remains open.

Weakest sufficient missing lemma:
For every admissible graph-semantic input X, cycleOverlapRank X <= colapRank X.

Forbidden promotions avoided:
No P vs NP closure.
No Clay-problem closure.
No Chronos-RR closure.
No H4.1/FGL closure.
No UniversalFiberEntropyGap proof.
No SemanticRankRateToFiberEntropySoundness proof.
No unconditional graph-theoretic cycle-overlap-rank bound.
No rigidity closure.
Observed AI test results
System	Score	Result
DeepAI	4/6	Preserved most boundaries, but incorrectly treated the unrestricted statement as open after the counterexample already made it false as stated.
Claude	5/6	Correctly classified the negative unrestricted result and conditional restricted case, but added extra open directions beyond the weakest sufficient missing lemma.
Gemini	4/6	Correctly avoided forbidden promotions, but identified cycleOverlap_le_colap itself as the missing lemma instead of the quantified admissible-input domination lemma.
Boundary
This invitation does not prove:
P vs NP
any Clay-problem closure
Chronos-RR closure
H4.1/FGL closure
UniversalFiberEntropyGap
SemanticRankRateToFiberEntropySoundness
unrestricted graph-semantic cycle-overlap domination
unconditional graph-theoretic cycle-overlap-rank bound
rigidity closure
