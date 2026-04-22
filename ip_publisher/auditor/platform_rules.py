from __future__ import annotations


def audit_platform_variants(draft: dict) -> tuple[float, list[dict], list[dict]]:
    variants = draft.get("platform_variants", {})
    blockers: list[dict] = []
    warnings: list[dict] = []
    passed = 0
    total = max(len(variants), 1)
    for platform, variant in variants.items():
        checks = variant.get("checks", {})
        if checks.get("within_limit"):
            passed += 1
            continue
        blockers.append(
            {
                "code": "PLATFORM_LIMIT_EXCEEDED",
                "message": f"{platform} 版本不满足平台长度限制",
                "location": platform,
                "suggestion": "压缩标题或正文，再重新生成平台版本。",
            }
        )
    return passed / total, blockers, warnings
