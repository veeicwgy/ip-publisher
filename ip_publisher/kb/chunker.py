from __future__ import annotations

from .normalize import normalize_text


def _split_paragraphs(text: str) -> list[str]:
    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]


def chunk_documents(documents: list[dict], max_chars: int = 420) -> list[dict]:
    chunks: list[dict] = []
    for document in documents:
        for section in document.get("sections", []):
            paragraphs = _split_paragraphs(normalize_text(section.get("text", "")))
            current: list[str] = []
            chunk_index = 1
            for paragraph in paragraphs:
                candidate = "\n\n".join(current + [paragraph]).strip()
                if current and len(candidate) > max_chars:
                    text = "\n\n".join(current).strip()
                    chunks.append(
                        {
                            "chunk_id": f"{document['doc_id']}::{section['section_id']}::{chunk_index}",
                            "doc_id": document["doc_id"],
                            "section_id": section["section_id"],
                            "heading": section.get("heading", ""),
                            "text": text,
                            "source_uri": document.get("source_uri", ""),
                            "tags": document.get("tags", []),
                        }
                    )
                    chunk_index += 1
                    current = [paragraph]
                else:
                    current.append(paragraph)
            if current:
                chunks.append(
                    {
                        "chunk_id": f"{document['doc_id']}::{section['section_id']}::{chunk_index}",
                        "doc_id": document["doc_id"],
                        "section_id": section["section_id"],
                        "heading": section.get("heading", ""),
                        "text": "\n\n".join(current).strip(),
                        "source_uri": document.get("source_uri", ""),
                        "tags": document.get("tags", []),
                    }
                )
    return chunks
