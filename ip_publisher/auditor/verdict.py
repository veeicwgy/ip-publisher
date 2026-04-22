from __future__ import annotations


def build_verdict(scores: dict, blockers: list[dict], warnings: list[dict], thresholds: dict) -> tuple[str, str]:
    overall = scores["overall"]
    if blockers:
        return "reject", "revise_and_regenerate"
    if warnings or overall < thresholds["pass_score"]:
        if overall >= thresholds["manual_review_score"]:
            return "manual_review", "manual_review"
        return "reject", "revise_and_regenerate"
    return "pass", "publish_pack"
