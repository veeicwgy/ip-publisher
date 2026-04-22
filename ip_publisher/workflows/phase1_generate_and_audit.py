from __future__ import annotations

import json
from pathlib import Path

import yaml

from ..auditor.claim_extractor import extract_claims
from ..auditor.grounding import audit_grounding
from ..auditor.keyword_audit import audit_keywords
from ..auditor.outline_audit import audit_outline
from ..auditor.platform_rules import audit_platform_variants
from ..auditor.quality_audit import audit_quality
from ..auditor.structure_audit import audit_structure
from ..auditor.verdict import build_verdict
from ..generator.draft_writer import build_base_draft
from ..generator.platform_adapter import build_platform_variants
from ..kb.chunker import chunk_documents
from ..kb.loaders import load_documents
from ..kb.retriever import retrieve_relevant_chunks
from ..kb.store import index_chunks, load_chunk_map
from ..planner.hotspot_merger import merge_hotspot_brief
from ..planner.outline_builder import build_outline
from ..publisher.publish_package import build_publish_package, finalize_publish_package
from ..storage.artifact_store import write_artifacts

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = PACKAGE_ROOT / "schemas"
CONFIG_ROOT = PACKAGE_ROOT / "config"


def _load_schema(name: str) -> dict:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


def _assert_type(value: object, expected: str, pointer: str) -> None:
    mapping = {
        "object": dict,
        "array": list,
        "string": str,
        "number": (int, float),
        "boolean": bool,
        "integer": int,
    }
    if expected not in mapping:
        return
    if not isinstance(value, mapping[expected]):
        raise ValueError(f"{pointer} should be {expected}, got {type(value).__name__}")


def _validate_node(value: object, schema: dict, pointer: str) -> None:
    schema_type = schema.get("type")
    if schema_type:
        _assert_type(value, schema_type, pointer)
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{pointer} should be one of {schema['enum']}, got {value!r}")
    if schema_type == "object":
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                raise ValueError(f"{pointer}.{key} is required")
        for key, child_value in value.items():
            child_schema = properties.get(key) or schema.get("additionalProperties")
            if isinstance(child_schema, dict):
                _validate_node(child_value, child_schema, f"{pointer}.{key}")
    elif schema_type == "array":
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate_node(item, item_schema, f"{pointer}[{index}]")


def _validate_payload(payload: dict, schema_name: str) -> None:
    _validate_node(payload, _load_schema(schema_name), "$")


def _load_thresholds() -> dict:
    data = yaml.safe_load((CONFIG_ROOT / "audit_thresholds.yaml").read_text(encoding="utf-8"))
    return data["thresholds"]


def run_phase1(
    request_path: Path,
    kb_dir: Path,
    index_db: Path,
    output_root: Path,
) -> dict:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    _validate_payload(request, "article_request.schema.json")

    documents = load_documents(kb_dir)
    chunks = chunk_documents(documents)
    index_chunks(index_db, chunks)

    retrieved_chunks = retrieve_relevant_chunks(index_db, request)
    if not retrieved_chunks:
        raise RuntimeError("No knowledge-base chunks matched this request.")

    outline = build_outline(request)
    draft = build_base_draft(request, outline, retrieved_chunks)
    draft["retrieved_chunks"] = retrieved_chunks
    draft["hotspot_brief"] = merge_hotspot_brief(request)
    draft["platform_variants"] = build_platform_variants(request, draft)
    draft["publish_package"] = build_publish_package(request, draft)
    _validate_payload(draft, "article_draft.schema.json")

    thresholds = _load_thresholds()
    chunk_map = load_chunk_map(index_db)
    claims = extract_claims(draft)
    grounding_score, grounding_blockers, grounding_warnings = audit_grounding(
        claims,
        chunk_map,
        thresholds["grounding_overlap"],
    )
    keyword_score, keyword_blockers, keyword_warnings, keyword_metrics = audit_keywords(request, draft)
    outline_score, outline_blockers, outline_warnings = audit_outline(request, draft)
    platform_score, platform_blockers, platform_warnings, platform_metrics = audit_platform_variants(draft)
    structure_score, structure_blockers, structure_warnings = audit_structure(request, draft, thresholds)
    _, quality_blockers, quality_warnings, quality_metrics = audit_quality(request, draft, thresholds)
    blockers = grounding_blockers + keyword_blockers + outline_blockers + platform_blockers + structure_blockers + quality_blockers
    warnings = grounding_warnings + keyword_warnings + outline_warnings + platform_warnings + structure_warnings + quality_warnings
    scores = {
        "grounding": grounding_score,
        "keyword_fit": keyword_score,
        "outline_fit": outline_score,
        "platform_fit": platform_score,
        "ai_structure": structure_score,
        "fact_density": min(
            quality_metrics["fact_density"] / max(thresholds["min_fact_density"], 0.01),
            1.0,
        ),
        "authority_signal": min(
            quality_metrics["authority_signal_count"] / max(thresholds["min_authority_signals"], 1),
            1.0,
        ),
    }
    scores["overall"] = sum(scores.values()) / len(scores)
    status, next_action = build_verdict(scores, blockers, warnings, thresholds)
    audit_report = {
        "task_id": request["task_id"],
        "status": status,
        "scores": scores,
        "metrics": {
            **quality_metrics,
            **keyword_metrics,
            **platform_metrics,
        },
        "blockers": blockers,
        "warnings": warnings,
        "next_action": next_action,
    }
    draft["publish_package"] = finalize_publish_package(draft["publish_package"], audit_report)
    _validate_payload(draft, "article_draft.schema.json")
    _validate_payload(audit_report, "audit_report.schema.json")

    artifact_paths = write_artifacts(output_root, request, draft, audit_report)
    return {
        "artifacts": artifact_paths,
        "draft": draft,
        "audit_report": audit_report,
    }
