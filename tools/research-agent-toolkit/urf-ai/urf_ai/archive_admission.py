"""Conservative finite fold admissibility precheck; never proves global solvability.

Does not infer mathematical impossibility from the absence of a safe reduction.
The caller must independently justify whether the enumerated domain is complete.
"""
from __future__ import annotations


def finite_fold_precheck(states: object, folded: object, outcomes: object,
                         *, complete_domain: bool = False, max_states: int = 256) -> dict:
    """Check F(x)=F(y) => Sigma(x)=Sigma(y) on explicitly enumerated states.

    Input must be finite dictionaries keyed by unique non-bool integers or strings;
    values are immutable integer/string/bool labels. `complete_domain` is a
    caller assertion, NOT an independently audited completeness certificate.
    This routine never returns a PROVED/VERIFIED theorem status.
    """
    def verdict(code: str, reason: str) -> dict:
        return {"status": code, "reason": reason, "scope": "FINITE_ENUMERATED_ONLY",
                "proof_status": "NOT_LEAN_VERIFIED"}
    if type(complete_domain) is not bool or type(max_states) is not int or not (1 <= max_states <= 4096):
        return verdict("DEFER", "invalid completeness flag or resource budget")
    if not isinstance(states, (tuple, list)) or not isinstance(folded, dict) or not isinstance(outcomes, dict):
        return verdict("DEFER", "expected finite states and label mappings")
    if len(states) == 0 or len(states) > max_states:
        return verdict("INCOMPLETE", "empty or over-budget candidate domain")
    if any(type(x) not in (int, str) for x in states) or len(set(states)) != len(states):
        return verdict("DEFER", "invalid or duplicate state identifiers")
    if (any(type(key) not in (int, str) for key in folded) or
            any(type(key) not in (int, str) for key in outcomes)):
        return verdict("DEFER", "unsupported mapping key types")
    if set(folded) != set(states) or set(outcomes) != set(states):
        return verdict("INCOMPLETE", "candidate lacks exact state coverage")
    if (any(type(value) not in (int, str) for value in folded.values()) or
            any(type(value) not in (int, str, bool) for value in outcomes.values())):
        return verdict("DEFER", "unsupported fold or outcome labels")
    fibers: dict[object, list[object]] = {}
    for state in states:
        fibers.setdefault(folded[state], []).append(state)
    for fiber in fibers.values():
        if len({outcomes[state] for state in fiber}) > 1:
            return verdict("REJECT_UNSOUND_FOLD", "a folded fiber mixes distinct solution outcomes")
    if not any(len(fiber) > 1 for fiber in fibers.values()):
        return verdict("NO_NONTRIVIAL_REDUCTION_IN_CANDIDATE", "candidate is injective; other solutions are not excluded")
    if not complete_domain:
        return verdict("INCOMPLETE", "sound on sample only; full domain coverage not attested")
    return verdict("SOUND_ON_ATTESTED_FINITE_DOMAIN", "fiber outcomes agree; completeness is caller asserted")
