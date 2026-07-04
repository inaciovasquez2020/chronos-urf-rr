# Physics Admission Standard

## Purpose

This repository separates formal infrastructure from scientific results.

A result enters the scientific layer only when it establishes either:

1. a derived law of the formal physical model, or
2. a quantitative prediction that is experimentally testable in principle.

Infrastructure, interfaces, witnesses, proof targets, kernel stabilization, parser repairs, arithmetic support, and build-system maintenance remain classified as infrastructure unless they directly support an admitted scientific theorem.

## Repository Layers

| Layer | Meaning |
|---|---|
| Infrastructure | Engineering or formalization support only |
| Formal Mathematics | Lean-verified theorem derived from stated assumptions |
| Formal Physics | Derived theorem relating interpreted physical observables |
| Experimental Prediction | Quantitative measurable consequence suitable for empirical comparison |
| Empirically Supported Result | Prediction additionally supported by documented experimental evidence |

## Admission Criteria

A theorem may enter the Formal Physics layer only if all of the following hold:

1. It is Lean-verified.
2. It is derived from explicitly stated assumptions.
3. It is not merely a definition, structure field, witness, proof target, axiom, or restatement of an assumption.
4. It establishes a mathematically substantive relationship among interpreted observables.
5. The governing model is explicitly identified.
6. The assumptions and domain of validity are documented.
7. The observable interpretation is documented separately from the Lean proof.

A theorem may enter the Experimental Prediction layer only if it additionally provides:

1. a measurable observable,
2. a quantitative prediction,
3. a stated experimental or observational regime,
4. a comparison baseline or comparison protocol.

Agreement with existing theory is admissible. Novel disagreement is not required.

## Interpretive Boundary

Lean verification establishes that a theorem follows from formal assumptions.

It does not establish that those assumptions describe nature.

The evidentiary chain is:

```text
Formal assumptions
→ Lean-verified theorem
→ mathematical consequence of the model
→ physical interpretation
→ empirical comparison
Each stage after formal verification requires separate scientific justification.
Non-Admissible as Physics
The following are not scientific physics results by themselves:
input surfaces,
interfaces,
witnesses,
proof targets,
parser repairs,
kernel stabilization,
arithmetic normalization,
helper lemmas used only for proof automation,
verification scripts,
build or CI maintenance.
They may be merged as infrastructure, but they must not be presented as physical laws or experimental predictions.
Theorem Specification
Every theorem proposed for Formal Physics or Experimental Prediction status must document:
theorem identifier,
model identifier,
Lean file and theorem name,
exact formal statement,
assumptions,
dependent definitions,
proof status,
mathematical result,
observable mapping,
physical interpretation,
quantitative consequence, if any,
domain of validity,
limiting behavior, if analyzed,
experimental status,
repository classification.
Scientific Claim Rule
The repository may claim:
Lean verified the theorem;
the theorem follows from stated assumptions;
the theorem is a consequence of the specified formal model.
The repository may not claim:
the assumptions are physically correct;
the theorem is a law of nature;
the model is experimentally confirmed;
unless those claims are independently documented.
