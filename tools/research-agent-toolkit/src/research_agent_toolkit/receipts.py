from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path


@dataclass
class SessionReceipt:
    session_id: str
    objective: str
    decisions: list[dict] = field(default_factory=list)
    mutations: list[dict] = field(default_factory=list)
    verifications: list[dict] = field(default_factory=list)
    result: str | None = None
    boundary: str | None = None

    def write(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(asdict(self), indent=2, sort_keys=True) + "\n")
