"""Source-specific *finite* audit fixtures for the 2026-04-07 universality PDF.

Not a general formal proof or an LLM.  Two-tape deterministic machine:
read-only input tape, blank work tape, head positions 0, state q0;
read first input bit and halt, without moving.  Transcript is precisely
Y0=c0; Y1=(c0,c1), where c_t=(state, head positions, scanned symbols).
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
from typing import Any

SOURCE_FILENAME = "Universality_Bridge_for_Deterministic_Polynomial_Time_Computation_via_Normalized__k__Tape_Transcript_Systems.pdf"


def source_digest(path: str | Path) -> str:
    """Bind results to actual bytes; missing source => fail closed."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)
    return sha256(p.read_bytes()).hexdigest()


def inputs(n: int):
    if type(n) is not int or not 1 <= n <= 12:
        raise ValueError("only 1 <= n <= 12 is supported")
    return (''.join(bits) for bits in product('01', repeat=n))


def full_conf(x: str, t: int = 0):
    _valid_x(x)
    if t not in (0, 1):
        raise ValueError("trivial halting machine only has 0 and 1")
    return ('q0' if t == 0 else 'qhalt', (0, 0), x, '_')


def _valid_x(x: Any):
    if not isinstance(x, str) or not x or len(x) > 12 or any(z not in '01' for z in x):
        raise ValueError("must be 1..12 input bits")


def frames(x: str, t: int = 0):
    _valid_x(x)
    if t not in (0, 1):
        raise ValueError("only 0/1 rounds supported")
    # q0/qhalt, positions of input/work heads, symbols under those heads
    c0 = ('q0', (0, 0), (x[0], '_'))
    c1 = ('qhalt', (0, 0), (x[0], '_'))
    return (c0,) if t == 0 else (c0, (c0, c1))


def reconstruction_counterexample(a: str, b: str, t: int) -> bool:
    """Same observed transcript; distinct complete configurations."""
    try:
        _valid_x(a); _valid_x(b)
        if len(a) != len(b) or t not in (0, 1):
            return False
        return a != b and frames(a, t) == frames(b, t) and full_conf(a, t) != full_conf(b, t)
    except (ValueError, TypeError):
        return False


def _conditional_entropy(xvalues: list[str], observation) -> Fraction:
    """Exact H(X|obs) for uniform X and deterministic observation in this fixture.
    Each fiber cardinality is a power of 2, so logarithms are exact integers.
    """
    fibers = defaultdict(int)
    for x in xvalues:
        fibers[observation(x)] += 1
    weighted = 0
    for c in fibers.values():
        if c & (c-1):
            raise ValueError("non-power-of-two fiber; exact entropy not implemented")
        weighted += c*(c.bit_length()-1)
    return Fraction(weighted, len(xvalues))


def entropy_accounting(n: int, rounds: int = 1) -> dict:
    if not isinstance(n, int) or not 1 <= n <= 12 or rounds not in (0, 1):
        raise ValueError("bounded exact fixture only")
    values = list(inputs(n))
    hx = Fraction(n)
    h_y0 = _conditional_entropy(values, lambda x: frames(x, 0))
    h_yfull = _conditional_entropy(values, lambda x: frames(x, rounds))
    initial_info = hx - h_y0
    subsequent_info = h_y0 - h_yfull
    return {
        'n':n,'rounds':rounds,
        'h_input_bits':int(hx),
        'h_conditional_initial_bits':int(h_y0),
        'h_conditional_final_bits':int(h_yfull),
        'initial_information_bits':int(initial_info),
        'later_information_bits':int(subsequent_info),
        'source_omitted_identity_gap_bits':int(hx-subsequent_info-h_yfull),
        'corrected_chain_rule_exact': hx == initial_info + subsequent_info + h_yfull,
        'enumerated_inputs':len(values),
    }


def initial_reconstruction_tradeoff(n:int) -> dict:
    """If Y0 includes full x, exact Conf0 reconstruction becomes possible,
    but all H(X) has already been revealed in the initial transcript.
    """
    if type(n) is not int or not 2 <= n <= 12:
        raise ValueError("bounded fixture only")
    values = list(inputs(n))
    old_y0 = {frames(x,0) for x in values}
    repaired_y0 = {(x,frames(x,0)) for x in values}
    return {
        'input_count':len(values),
        'old_initial_transcript_classes':len(old_y0),
        'repaired_initial_transcript_classes':len(repaired_y0),
        'old_decoder_injective':len(old_y0)==len(values),
        'repaired_decoder_injective':len(repaired_y0)==len(values),
        'repaired_initial_information_bits':n,
        'repaired_remaining_input_entropy_bits':0,
    }


def polynomial_compatibility(n: int, log_bound: int) -> dict:
    """A lower bound on T of H/log(n) alone cannot exclude T=n^2.
    This is a *logical insufficiency demonstration*, not a SAT algorithm.
    """
    if type(n) is not int or type(log_bound) is not int or n < 2 or n > 1_000_000 or log_bound < 1:
        raise ValueError("invalid size/bandwidth")
    h_upper=n   # H(X) <= log2 |{0,1}^n| = n
    t_linear=n
    t_quadratic=n*n
    return {'input_bits':n,'entropy_upper_bits':h_upper,
            'per_step_capacity_bits':log_bound,
            'candidate_linear_steps':t_linear,
            'candidate_quadratic_steps':t_quadratic,
            'linear_capacity_compatible':t_linear*log_bound>=h_upper,
            'capacity_sufficient_for_full_entropy':t_quadratic*log_bound>=h_upper}


def evaluate_bridge_response(response: object, case_id: str) -> dict:
    """Require a structured status and an independently checked witness.
    No general theorem proving and no substring grading.
    """
    def fail(reason):
        return {'case':case_id,'pass':False,'reason':reason}
    if not isinstance(response,dict) or response.get('case_id')!=case_id:
        return fail('case ID or response format invalid')
    if case_id == 'bridge_reconstruction':
        if set(response) != {'case_id','status','witness','repair'} or response.get('status')!='REFUTED_AS_STATED' or response.get('repair')!='SUPPLY_INPUT_EXTERNALLY_OR_INCLUDE_IN_INITIAL_FRAME':
            return fail('status, schema or repair mismatch')
        w=response.get('witness')
        if not isinstance(w,dict) or set(w)!={'x','x_prime','time'}:return fail('witness schema invalid')
        ok=reconstruction_counterexample(w['x'],w['x_prime'],w['time'])
        return {'case':case_id,'pass':ok,'reason':'verified transcript collision' if ok else 'no valid transcript collision'}
    if case_id == 'bridge_chain_rule':
        if set(response) != {'case_id','status','witness','repair'} or response.get('status')!='REFUTED_AS_STATED' or response.get('repair')!='INCLUDE_INITIAL_MUTUAL_INFORMATION':
            return fail('status, schema or repair mismatch')
        w=response.get('witness')
        if not isinstance(w,dict) or set(w)!={'input_bits','rounds'}:return fail('witness schema invalid')
        try: r=entropy_accounting(w['input_bits'],w['rounds'])
        except (TypeError,ValueError):return fail('invalid entropy fixture')
        ok = r['source_omitted_identity_gap_bits']>0 and r['corrected_chain_rule_exact']
        return {'case':case_id,'pass':ok,'reason':'exact rational entropy identity and missing term' if ok else 'incorrect entropy witness','audit':r}
    if case_id == 'bridge_initial_tradeoff':
        if set(response) != {'case_id','status','witness','missing_obligation'} or response.get('status')!='INITIAL_INFORMATION_ALREADY_EXHAUSTS_INPUT_ENTROPY' or response.get('missing_obligation')!='NONTRIVIAL_INFORMATION_TARGET_NOT_INITIALIZED_AWAY':
            return fail('status or schema invalid')
        w=response.get('witness')
        if not isinstance(w,dict) or set(w)!={'input_bits'}:return fail('witness schema invalid')
        try: r=initial_reconstruction_tradeoff(w['input_bits'])
        except (TypeError,ValueError):return fail('invalid tradeoff witness')
        ok=(not r['old_decoder_injective'] and r['repaired_decoder_injective']
            and r['repaired_remaining_input_entropy_bits']==0)
        return {'case':case_id,'pass':ok,'reason':'initial information tradeoff checked' if ok else 'tradeoff not established','audit':r}
    if case_id == 'bridge_sat_boundary':
        if set(response) != {'case_id','status','witness','missing_obligation'} or response.get('status')!='DOES_NOT_ESTABLISH_SUPERPOLYNOMIAL_SAT_HARDNESS' or response.get('missing_obligation')!='INDEPENDENT_SUPERPOLYNOMIAL_OR_NONTRIVIAL_REDUCTION':
            return fail('status or schema mismatch')
        w=response.get('witness')
        if not isinstance(w,dict) or set(w)!={'input_bits','per_step_capacity_bits'}:return fail('witness schema invalid')
        try:r=polynomial_compatibility(w['input_bits'],w['per_step_capacity_bits'])
        except (TypeError,ValueError):return fail('invalid complexity parameters')
        return {'case':case_id,'pass':r['capacity_sufficient_for_full_entropy'],
                'reason':'polynomial running time compatible with capacity lower bound','audit':r}
    return fail('unknown bridge case')


BRIDGE_CASES={'bridge_reconstruction','bridge_chain_rule','bridge_initial_tradeoff','bridge_sat_boundary'}
