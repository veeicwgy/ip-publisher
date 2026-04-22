from __future__ import annotations


def audit_quality(request: dict, draft: dict, thresholds: dict) -> tuple[float, list[dict], list[dict], dict]:
    del request
    claims = draft.get("claims", [])
    grounded_claims = [claim for claim in claims if claim.get("source_chunk_ids")]
    citable_claims = len(grounded_claims)
    section_count = max(len(draft.get("sections", [])), 1)
    fact_density = citable_claims / section_count
    authority_signal_count = int((draft.get("structure_signals") or {}).get("authority_signal_count", 0))

    blockers: list[dict] = []
    warnings: list[dict] = []
    if citable_claims < thresholds["min_citable_claims"]:
        blockers.append(
            {
                "code": "CITABLE_CLAIMS_TOO_FEW",
                "message": f"可引用声明数不足：当前 {citable_claims}，至少需要 {thresholds['min_citable_claims']}。",
                "location": "claims",
                "suggestion": "增加基于知识库片段的可回溯断言，而不是只写泛化描述。",
            }
        )
    if fact_density < thresholds["min_fact_density"]:
        blockers.append(
            {
                "code": "FACT_DENSITY_LOW",
                "message": f"事实密度偏低：当前 {fact_density:.2f}，至少需要 {thresholds['min_fact_density']:.2f}。",
                "location": "body",
                "suggestion": "让每个关键段落至少落一条可回溯事实或数据点。",
            }
        )
    if authority_signal_count < thresholds["min_authority_signals"]:
        warnings.append(
            {
                "code": "AUTHORITY_SIGNAL_WEAK",
                "message": f"权威信号不足：当前 {authority_signal_count}，建议至少 {thresholds['min_authority_signals']}。",
                "location": "structure",
                "suggestion": "补充知识来源覆盖数、可引用声明数、实体标注与审核门槛等权威信号。",
            }
        )

    claim_score = min(citable_claims / max(thresholds["min_citable_claims"], 1), 1.0)
    density_score = min(fact_density / max(thresholds["min_fact_density"], 0.01), 1.0)
    authority_score = min(authority_signal_count / max(thresholds["min_authority_signals"], 1), 1.0)
    metrics = {
        "citable_claims": citable_claims,
        "fact_density": fact_density,
        "authority_signal_count": authority_signal_count,
    }
    return (claim_score + density_score + authority_score) / 3, blockers, warnings, metrics
