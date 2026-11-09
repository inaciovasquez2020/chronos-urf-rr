#!/usr/bin/env python3
"""Read-only research adapter to the existing Research Agent Toolkit policy engine.

Requires this candidate to live at tools/research-agent-toolkit/urf-ai.
Does not authorize or perform theorem promotion, git mutations or model calls.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

TOOLKIT_ROOT = Path(__file__).resolve().parents[2]
URF_AI_ROOT = TOOLKIT_ROOT / 'urf-ai'
sys.path.insert(0, str(TOOLKIT_ROOT / 'src'))
sys.path.insert(0, str(URF_AI_ROOT))

from research_agent_toolkit.engine import evaluate, load_config
from urf_ai.assistant import answer


def run(root: Path, config_path: Path, source_path: str, case_id: str) -> dict:
    root = root.resolve(strict=True)
    rel = Path(source_path)
    if rel.is_absolute() or not rel.parts or '..' in rel.parts or '.git' in rel.parts:
        raise ValueError('source must be a safe repository-relative file path')
    src = root / rel
    if not src.is_file() or src.is_symlink() or not src.resolve().is_relative_to(root):
        raise ValueError('source file is missing, symlinked or outside repository')
    size = src.stat().st_size
    if size > 1024 * 1024:
        raise ValueError('source exceeds 1 MiB read-only limit')
    data = src.read_bytes()
    policy = evaluate(load_config(config_path), 'theorem_claim', [rel.as_posix()])
    out = {'mode': 'RAT_GATED_READONLY_RESEARCH_ONLY',
           'path': rel.as_posix(), 'source_sha256': hashlib.sha256(data).hexdigest(),
           'policy_status': policy.status, 'policy_reasons': policy.reasons,
           'promotion_allowed': False, 'mutation_performed': False, 'model_calls': 0}
    if policy.status == 'DENY':
        out['status'] = 'POLICY_DENY'
    else:
        out['status'] = 'RESEARCH_NOTE_NOT_THEOREM_PROOF'
        out['curated_case'] = answer(case_id)
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo-root', type=Path, required=True)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--source', required=True, help='repository-relative existing path')
    p.add_argument('--case', required=True)
    a = p.parse_args()
    result = run(a.repo_root, a.config, a.source, a.case)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 2 if result['status'] == 'POLICY_DENY' else 0


if __name__ == '__main__':
    raise SystemExit(main())
