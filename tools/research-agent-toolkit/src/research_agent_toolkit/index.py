from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
from pathlib import Path

TOKEN = re.compile(r"[A-Za-z0-9_]+")


def _tokens(text: str) -> list[str]:
    return [x.lower() for x in TOKEN.findall(text)]


def hashed_embedding(text: str, dims: int = 256) -> list[float]:
    vec = [0.0] * dims
    for tok in _tokens(text):
        digest = hashlib.blake2b(tok.encode(), digest_size=8).digest()
        raw = int.from_bytes(digest, "little")
        idx = raw % dims
        sign = -1.0 if (raw >> 63) else 1.0
        vec[idx] += sign
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def extract_text(path: str | Path) -> str:
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        try:
            import fitz  # type: ignore
        except Exception as exc:
            raise RuntimeError("PDF extraction requires optional PyMuPDF package") from exc
        doc = fitz.open(path)
        return "\n".join(page.get_text() for page in doc)
    return path.read_text(errors="replace")


def chunks(text: str, size: int = 1800, overlap: int = 200):
    if size <= overlap:
        raise ValueError("size must exceed overlap")
    start = 0
    while start < len(text):
        yield text[start:start + size]
        if start + size >= len(text):
            break
        start += size - overlap


def init_db(db: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY,
            source TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            sha256 TEXT NOT NULL,
            text TEXT NOT NULL,
            embedding TEXT NOT NULL,
            UNIQUE(source, ordinal, sha256)
        )
    """)
    return conn


def index_file(db: str | Path, path: str | Path) -> int:
    path = Path(path)
    text = extract_text(path)
    conn = init_db(db)
    count = 0
    with conn:
        for ordinal, chunk in enumerate(chunks(text)):
            sha = hashlib.sha256(chunk.encode()).hexdigest()
            emb = json.dumps(hashed_embedding(chunk), separators=(",", ":"))
            before = conn.total_changes
            conn.execute(
                "INSERT OR IGNORE INTO chunks(source, ordinal, sha256, text, embedding) VALUES(?,?,?,?,?)",
                (str(path), ordinal, sha, chunk, emb),
            )
            count += conn.total_changes - before
    conn.close()
    return count


def search(db: str | Path, query: str, limit: int = 5) -> list[dict]:
    q = hashed_embedding(query)
    conn = init_db(db)
    rows = conn.execute("SELECT source, ordinal, text, embedding FROM chunks").fetchall()
    conn.close()
    scored = []
    for source, ordinal, text, embedding in rows:
        score = cosine(q, json.loads(embedding))
        scored.append({"score": score, "source": source, "ordinal": ordinal, "text": text})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]
