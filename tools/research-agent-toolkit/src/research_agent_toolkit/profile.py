from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def build_profile(paths: list[str | Path]) -> dict:
    events = Counter()
    names = Counter()
    errors = 0
    durations = []
    for path in paths:
        for line in Path(path).read_text(errors="replace").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            events[row.get("event", "unknown")] += 1
            attrs = row.get("attrs", {})
            if "name" in attrs:
                names[attrs["name"]] += 1
            if row.get("event") == "span.error":
                errors += 1
            if row.get("event") == "span.end" and "duration_ns" in attrs:
                durations.append(attrs["duration_ns"])
    return {
        "events": dict(events),
        "span_names": dict(names),
        "errors": errors,
        "mean_duration_ns": (sum(durations) / len(durations)) if durations else 0,
    }
