from __future__ import annotations

from ..kb.normalize import extract_keywords


def _overlap_ratio(claim: str, source_text: str) -> float:
    claim_tokens = {token.lower() for token in extract_keywords(claim)}
    source_tokens = {token.lower() for token in extract_keywords(source_text)}
    if not claim_tokens:
        return 0.0
    return len(claim_tokens & source_tokens) / len(claim_tokens)


def audit_grounding(claims: list[dict], chunk_map: dict[str, dict], threshold: float) -> tuple[float, list[dict], list[dict]]:
    warnings: list[dict] = []
    blockers: list[dict] = []
    grounded = 0
    for claim in claims:
        source_ids = claim.get("source_chunk_ids", [])
        if not source_ids:
            blockers.append(
                {
                    "code": "UNGROUNDED_CLAIM",
                    "message": f"断言缺少来源：{claim['text']}",
                    "location": claim.get("claim_id", ""),
                    "suggestion": "为该断言补充可回溯 chunk_id，或删除该断言。",
                }
            )
            continue
        source_texts = [chunk_map[source_id]["text"] for source_id in source_ids if source_id in chunk_map]
        if not source_texts:
            blockers.append(
                {
                    "code": "MISSING_SOURCE_CHUNK",
                    "message": f"断言引用了不存在的来源片段：{', '.join(source_ids)}",
                    "location": claim.get("claim_id", ""),
                    "suggestion": "重新生成来源映射，确保引用的 chunk_id 已入库。",
                }
            )
            continue
        best_overlap = max(_overlap_ratio(claim["text"], source_text) for source_text in source_texts)
        if best_overlap >= threshold:
            grounded += 1
        else:
            warnings.append(
                {
                    "code": "LOW_GROUNDING_OVERLAP",
                    "message": f"断言与来源片段重合度偏低：{claim['text']}",
                    "location": claim.get("claim_id", ""),
                    "suggestion": "收紧改写幅度，避免把知识库片段改写成无证据的新表述。",
                }
            )
    total = len(claims) or 1
    return grounded / total, blockers, warnings
