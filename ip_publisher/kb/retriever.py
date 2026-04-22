from __future__ import annotations

from pathlib import Path

from .store import list_chunks, search_chunks


def build_search_query(request: dict) -> str:
    bits = [
        request.get("product", {}).get("name", ""),
        *request.get("seo", {}).get("primary_keywords", []),
        request.get("hotspot", {}).get("title", ""),
        request.get("outline", {}).get("brief", ""),
    ]
    return " ".join(bit for bit in bits if bit).strip()


def retrieve_relevant_chunks(db_path: Path, request: dict, limit: int = 8) -> list[dict]:
    scope = request.get("kb_scope", {})
    doc_ids = scope.get("doc_ids") or None
    tags = scope.get("tags") or None
    queries = [
        build_search_query(request),
        request.get("product", {}).get("name", ""),
        *request.get("seo", {}).get("primary_keywords", []),
    ]
    for query in queries:
        if not query:
            continue
        rows = search_chunks(
            db_path=db_path,
            query=query,
            doc_ids=doc_ids,
            tags=tags,
            limit=limit,
        )
        if rows:
            if doc_ids:
                covered = {row["doc_id"] for row in rows}
                missing = [doc_id for doc_id in doc_ids if doc_id not in covered]
                if missing:
                    extras = list_chunks(db_path=db_path, doc_ids=missing, limit=max(limit - len(rows), 1))
                    seen = {row["chunk_id"] for row in rows}
                    rows.extend([row for row in extras if row["chunk_id"] not in seen])
            return rows[:limit]
    return list_chunks(db_path=db_path, doc_ids=doc_ids, tags=tags, limit=limit)
