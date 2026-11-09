#!/usr/bin/env python3
"""Deterministic, offline, read-only source-specific witness audit.

Run at the isolated URF-AI candidate root:
  python tools/run_universality_bridge_audit.py --source /path/to/Universality...pdf
Requires only standard-library Python. Does not run Lean or an LLM.
"""
from __future__ import annotations
import argparse, hashlib, json, platform, sys
from pathlib import Path
from urf_ai.bridge_cases import (
    source_digest, reconstruction_counterexample, entropy_accounting,
    initial_reconstruction_tradeoff, polynomial_compatibility,
    BRIDGE_CASES, evaluate_bridge_response,
)
from urf_ai.assistant import RECORDS

SOURCE_SHA256 = '34096bfa667267624b5b6ad3b76ccb7b0d9eca8e90f129f85ad4b8b9a7eabc30'

def run(source:Path)->dict:
    observed=source_digest(source)
    if observed!=SOURCE_SHA256:
        raise ValueError('source SHA256 differs from reviewed PDF; refuse to reuse case labels')
    collision_n=[]
    for n in range(2,13):
        a='0'*n;b='0'+'1'*(n-1)
        assert reconstruction_counterexample(a,b,0)
        assert reconstruction_counterexample(a,b,1)
        collision_n.append(n)
    entropy=[entropy_accounting(n,1) for n in range(1,13)]
    assert all(r['corrected_chain_rule_exact'] and r['source_omitted_identity_gap_bits']==1 for r in entropy)
    tradeoffs=[initial_reconstruction_tradeoff(n) for n in range(2,13)]
    assert all(not r['old_decoder_injective'] and r['repaired_decoder_injective'] and r['repaired_remaining_input_entropy_bits']==0 for r in tradeoffs)
    compatibility=[polynomial_compatibility(2**j,j) for j in range(3,14)]
    assert all(r['linear_capacity_compatible'] for r in compatibility)
    cases={id:evaluate_bridge_response(RECORDS[id],id)['pass'] for id in sorted(BRIDGE_CASES)}
    assert all(cases.values())
    return {'schema':'urf-ai.universality-source-regression/v1',
            'status':'COMPUTATION_PASS_SOURCE_SPECIFIC_NOT_LEAN_OR_LLM',
            'source_sha256':observed,
            'source_bytes':source.stat().st_size,
            'python_version':platform.python_version(),
            'mutation':'NONE',
            'reconstruction_collision_input_lengths':collision_n,
            'reconstruction_collision_time_indices':[0,1],
            'entropy_sizes_checked':[r['n'] for r in entropy],
            'entropy_omitted_term_gap_bits_each':[r['source_omitted_identity_gap_bits'] for r in entropy],
            'initial_reconstruction_tradeoff_lengths':[n for n in range(2,13)],
            'linear_time_compatibility_input_lengths':[r['input_bits'] for r in compatibility],
            'semantic_cases':cases,
            'new_source_theorem_lean_verified':False,
            'gpt6_baseline_executed':False,
            'gpt6_urf_arm_executed':False}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    args=parser.parse_args()
    result=run(args.source)
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
