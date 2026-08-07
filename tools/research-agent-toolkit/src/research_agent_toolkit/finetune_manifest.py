from __future__ import annotations

import hashlib
import json
from pathlib import Path


def prepare_jsonl(input_jsonl: str | Path, output_jsonl: str | Path) -> dict:
    """Validate/copy chat-style JSONL and emit a reproducible manifest.

    This prepares data only. It does not run fine-tuning.
    """
    src = Path(input_jsonl)
    dst = Path(output_jsonl)
    valid = 0
    with src.open(encoding="utf-8") as inp, dst.open("w", encoding="utf-8") as out:
        for lineno, line in enumerate(inp, 1):
            if not line.strip():
                continue
            obj = json.loads(line)
            messages = obj.get("messages")
            if not isinstance(messages, list) or not messages:
                raise ValueError(f"line {lineno}: missing nonempty messages list")
            for msg in messages:
                if msg.get("role") not in {"system", "user", "assistant"} or not isinstance(msg.get("content"), str):
                    raise ValueError(f"line {lineno}: invalid message")
            out.write(json.dumps({"messages": messages}, ensure_ascii=False) + "\n")
            valid += 1
    digest = hashlib.sha256(dst.read_bytes()).hexdigest()
    return {"records": valid, "sha256": digest, "output": str(dst)}
