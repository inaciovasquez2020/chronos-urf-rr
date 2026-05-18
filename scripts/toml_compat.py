from __future__ import annotations

import ast
from typing import Any, BinaryIO, TextIO


class TOMLDecodeError(ValueError):
    pass


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    escaped = False
    out = []
    for ch in line:
        if escaped:
            out.append(ch)
            escaped = False
            continue
        if ch == "\\" and in_double:
            out.append(ch)
            escaped = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            out.append(ch)
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            out.append(ch)
            continue
        if ch == "#" and not in_single and not in_double:
            break
        out.append(ch)
    return "".join(out).strip()


def _split_array_items(body: str) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    in_single = False
    in_double = False
    escaped = False
    depth = 0
    for ch in body:
        if escaped:
            current.append(ch)
            escaped = False
            continue
        if ch == "\\" and in_double:
            current.append(ch)
            escaped = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            current.append(ch)
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            current.append(ch)
            continue
        if not in_single and not in_double:
            if ch in "[{(":
                depth += 1
            elif ch in "]})":
                depth -= 1
            elif ch == "," and depth == 0:
                item = "".join(current).strip()
                if item:
                    items.append(item)
                current = []
                continue
        current.append(ch)
    item = "".join(current).strip()
    if item:
        items.append(item)
    return items


def _parse_value(raw: str) -> Any:
    raw = raw.strip()
    if raw in {"true", "false"}:
        return raw == "true"
    if raw.startswith("[") and raw.endswith("]"):
        body = raw[1:-1].strip()
        if not body:
            return []
        return [_parse_value(item) for item in _split_array_items(body)]
    if raw.startswith('"') or raw.startswith("'"):
        try:
            return ast.literal_eval(raw)
        except Exception as exc:
            raise TOMLDecodeError(str(exc)) from exc
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass
    return raw


def loads(src: str | bytes, *, parse_float: Any = float) -> dict[str, Any]:
    if isinstance(src, bytes):
        src = src.decode("utf-8")

    root: dict[str, Any] = {}
    current = root
    logical_lines: list[str] = []
    buffer = ""

    for raw_line in src.splitlines():
        line = _strip_comment(raw_line)
        if not line:
            continue
        buffer = f"{buffer} {line}".strip() if buffer else line
        if buffer.count("[") > buffer.count("]"):
            continue
        logical_lines.append(buffer)
        buffer = ""

    if buffer:
        raise TOMLDecodeError("unterminated TOML array")

    for line in logical_lines:
        if line.startswith("[") and line.endswith("]"):
            table = line[1:-1].strip()
            if not table:
                raise TOMLDecodeError("empty table name")
            current = root
            for part in table.split("."):
                key = part.strip().strip('"').strip("'")
                current = current.setdefault(key, {})
                if not isinstance(current, dict):
                    raise TOMLDecodeError(f"table conflict: {table}")
            continue

        if "=" not in line:
            raise TOMLDecodeError(f"invalid TOML line: {line}")

        key, raw_value = line.split("=", 1)
        current[key.strip().strip('"').strip("'")] = _parse_value(raw_value)

    return root


def load(fp: BinaryIO | TextIO, *, parse_float: Any = float) -> dict[str, Any]:
    return loads(fp.read(), parse_float=parse_float)
