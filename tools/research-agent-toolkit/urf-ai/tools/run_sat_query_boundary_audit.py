#!/usr/bin/env python3
"""Source-SHA-pinned, deterministic SAT/query finite audit (stdout JSON only)."""
from __future__ import annotations
import argparse, json, platform
from pathlib import Path
from urf_ai.bridge_cases import source_digest
from urf_ai.sat_query_boundary import (
    sat_family_receipt, copy_machine_entropy_regression, SAT_QUERY_CASES,
)
from urf_ai.assistant import answer

SOURCE_SHA256='34096bfa667267624b5b6ad3b76ccb7b0d9eca8e90f129f85ad4b8b9a7eabc30'

def run(source:Path)->dict:
    actual=source_digest(source)
    if actual!=SOURCE_SHA256:
        raise ValueError('reviewed PDF source SHA-256 mismatch; fail closed')
    families=[sat_family_receipt(m) for m in range(1,13)]
    copier=[copy_machine_entropy_regression(n) for n in range(1,11)]
    adapter={c:{'validation':answer(c)['validation']['pass'],
                'claim_state':answer(c)['governance']['claim_state']}
             for c in sorted(SAT_QUERY_CASES)}
    if not all(x['validation'] and x['claim_state']=='OPEN' for x in adapter.values()):
        raise RuntimeError('source-scoped adapter validation or OPEN boundary failed')
    if sum(x['encoded_instances'] for x in families)!=8190:
        raise RuntimeError('finite enumerated SAT instance count differs from 8190')
    return {
        'schema':'urf-ai.sat-query-boundary/v1',
        'status':'COMPUTATION_PASS_BOUNDED_NOT_LEAN_OR_GPT6',
        'source_sha256':actual,
        'source_bytes':source.stat().st_size,
        'python_version':platform.python_version(),
        'cnf_encoding':'single_propositional_variable_m_independent_sign_bits',
        'family_sizes':list(range(1,13)),
        'total_cnf_inputs_enumerated':8190,
        'family_results':families,
        'copier_results':copier,
        'adapter_cases':adapter,
        'derived_theorem_verification':'PAPER_PROOF_NOT_FORMALIZED',
        'unrestricted_SAT_lower_bound':'OPEN',
        'gpt6_baseline_executed':False,
        'gpt6_urf_assisted_executed':False,
        'repository_mutation':'NONE',
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.source),sort_keys=True,indent=2))

if __name__=='__main__':main()
