from __future__ import annotations

import json
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Event:
    ts_ns: int
    event: str
    span_id: str
    parent_span_id: str | None
    attrs: dict


class JsonlTracer:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: str, span_id: str, attrs: dict | None = None, parent_span_id: str | None = None) -> None:
        record = Event(time.time_ns(), event, span_id, parent_span_id, attrs or {})
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(record), sort_keys=True) + "\n")

    @contextmanager
    def span(self, name: str, attrs: dict | None = None, parent_span_id: str | None = None):
        span_id = uuid.uuid4().hex
        started = time.perf_counter_ns()
        self.emit("span.start", span_id, {"name": name, **(attrs or {})}, parent_span_id)
        try:
            yield span_id
        except Exception as exc:
            self.emit("span.error", span_id, {"name": name, "error": repr(exc)}, parent_span_id)
            raise
        else:
            self.emit("span.end", span_id, {"name": name, "duration_ns": time.perf_counter_ns() - started}, parent_span_id)
