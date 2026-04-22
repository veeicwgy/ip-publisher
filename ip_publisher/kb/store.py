from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS chunks (
    chunk_id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    section_id TEXT NOT NULL,
    heading TEXT,
    text TEXT NOT NULL,
    source_uri TEXT,
    tags TEXT
);

CREATE VIRTUAL TABLE IF NOT EXISTS chunk_fts USING fts5(
    chunk_id UNINDEXED,
    doc_id UNINDEXED,
    heading,
    text,
    tags UNINDEXED
);
"""


def _connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db(db_path: Path) -> None:
    with _connect(db_path) as conn:
        conn.executescript(SCHEMA_SQL)


def index_chunks(db_path: Path, chunks: list[dict]) -> None:
    initialize_db(db_path)
    with _connect(db_path) as conn:
        conn.execute("DELETE FROM chunks")
        conn.execute("DELETE FROM chunk_fts")
        rows = [
            (
                chunk["chunk_id"],
                chunk["doc_id"],
                chunk["section_id"],
                chunk.get("heading", ""),
                chunk["text"],
                chunk.get("source_uri", ""),
                ",".join(chunk.get("tags", [])),
            )
            for chunk in chunks
        ]
        conn.executemany(
            """
            INSERT INTO chunks (chunk_id, doc_id, section_id, heading, text, source_uri, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.executemany(
            """
            INSERT INTO chunk_fts (chunk_id, doc_id, heading, text, tags)
            VALUES (?, ?, ?, ?, ?)
            """,
            [(row[0], row[1], row[3], row[4], row[6]) for row in rows],
        )


def search_chunks(
    db_path: Path,
    query: str,
    doc_ids: list[str] | None = None,
    tags: list[str] | None = None,
    limit: int = 8,
) -> list[dict]:
    initialize_db(db_path)
    with _connect(db_path) as conn:
        filters: list[str] = []
        params: list[object] = [query]
        if doc_ids:
            filters.append("c.doc_id IN ({})".format(",".join("?" for _ in doc_ids)))
            params.extend(doc_ids)
        elif tags:
            tag_clause = "(" + " OR ".join("c.tags LIKE ?" for _ in tags) + ")"
            filters.append(tag_clause)
            params.extend([f"%{tag}%" for tag in tags])
        where_filters = f" AND {' AND '.join(filters)}" if filters else ""
        sql = f"""
        SELECT c.*, bm25(chunk_fts) AS score
        FROM chunk_fts
        JOIN chunks c ON c.chunk_id = chunk_fts.chunk_id
        WHERE chunk_fts MATCH ?{where_filters}
        ORDER BY score
        LIMIT ?
        """
        params.append(limit)
        try:
            rows = conn.execute(sql, params).fetchall()
        except sqlite3.OperationalError:
            rows = []
        if not rows:
            like_filters = filters.copy()
            like_sql = f"""
            SELECT c.*, 9999 AS score
            FROM chunks c
            WHERE (c.heading LIKE ? OR c.text LIKE ?){f" AND {' AND '.join(like_filters)}" if like_filters else ""}
            LIMIT ?
            """
            like_params: list[object] = [f"%{query}%", f"%{query}%"]
            if doc_ids:
                like_params.extend(doc_ids)
            elif tags:
                like_params.extend([f"%{tag}%" for tag in tags])
            like_params.append(limit)
            rows = conn.execute(like_sql, like_params).fetchall()
        return [dict(row) for row in rows]


def list_chunks(
    db_path: Path,
    doc_ids: list[str] | None = None,
    tags: list[str] | None = None,
    limit: int = 8,
) -> list[dict]:
    initialize_db(db_path)
    with _connect(db_path) as conn:
        filters: list[str] = []
        params: list[object] = []
        if doc_ids:
            filters.append("doc_id IN ({})".format(",".join("?" for _ in doc_ids)))
            params.extend(doc_ids)
        elif tags:
            filters.append("(" + " OR ".join("tags LIKE ?" for _ in tags) + ")")
            params.extend([f"%{tag}%" for tag in tags])
        where = f"WHERE {' AND '.join(filters)}" if filters else ""
        rows = conn.execute(
            f"""
            SELECT *
            FROM chunks
            {where}
            LIMIT ?
            """,
            [*params, limit],
        ).fetchall()
    return [dict(row) for row in rows]


def load_chunk_map(db_path: Path) -> dict[str, dict]:
    initialize_db(db_path)
    with _connect(db_path) as conn:
        rows = conn.execute("SELECT * FROM chunks").fetchall()
    return {row["chunk_id"]: dict(row) for row in rows}
