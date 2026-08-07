from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def _ics_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def export_ics(events: list[dict], path: str | Path) -> None:
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Research Agent Toolkit//EN"]
    for i, event in enumerate(events):
        start = event["start"]
        if isinstance(start, str):
            start = datetime.fromisoformat(start)
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        stamp = start.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        uid = event.get("uid", f"rat-{i}-{stamp}")
        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{_ics_escape(uid)}",
            f"DTSTAMP:{stamp}",
            f"DTSTART:{stamp}",
            f"SUMMARY:{_ics_escape(event['summary'])}",
            f"DESCRIPTION:{_ics_escape(event.get('description', ''))}",
            "END:VEVENT",
        ])
    lines.append("END:VCALENDAR")
    Path(path).write_text("\r\n".join(lines) + "\r\n")
