#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required_files=(
  "$REPO_ROOT/README.md"
  "$REPO_ROOT/CLAUDE.md"
  "$REPO_ROOT/SKILL.md"
  "$REPO_ROOT/config/platforms.yaml"
  "$REPO_ROOT/config/hotspot-sources.yaml"
  "$REPO_ROOT/scripts/setup.sh"
  "$REPO_ROOT/scripts/quickstart.py"
  "$REPO_ROOT/scripts/generate-publish-pack.py"
  "$REPO_ROOT/docs/phase1-scaffold.md"
  "$REPO_ROOT/skills/ip-publisher/SKILL.md"
  "$REPO_ROOT/skills/ip-profile/SKILL.md"
  "$REPO_ROOT/skills/hotspot-fetcher/SKILL.md"
  "$REPO_ROOT/skills/article-generator/SKILL.md"
  "$REPO_ROOT/skills/humanizer/SKILL.md"
  "$REPO_ROOT/skills/cover-generator/SKILL.md"
  "$REPO_ROOT/skills/multi-publisher/SKILL.md"
  "$REPO_ROOT/skills/github-open-source-site-rework/SKILL.md"
  "$REPO_ROOT/ip_publisher/cli/run_phase1.py"
  "$REPO_ROOT/ip_publisher/workflows/phase1_generate_and_audit.py"
  "$REPO_ROOT/ip_publisher/schemas/article_request.schema.json"
  "$REPO_ROOT/ip_publisher/schemas/article_draft.schema.json"
  "$REPO_ROOT/ip_publisher/schemas/audit_report.schema.json"
  "$REPO_ROOT/ip_publisher/publisher/publish_package.py"
  "$REPO_ROOT/ip_publisher/auditor/structure_audit.py"
  "$REPO_ROOT/data/tasks/demo-request.json"
)

for file in "${required_files[@]}"; do
  [ -f "$file" ] || { echo "Missing file: $file"; exit 1; }
done

echo "All core files exist."
python3 "$REPO_ROOT/scripts/generate-publish-pack.py" \
  --platform xiaohongshu wechat_official zhihu \
  --topic "Smoke Test" \
  --angle "先把一个话题拆成三平台版本，再统一整理成发布包" \
  --body "这是一条用于验证发布包生成脚本的自检正文。它需要被改写成更适合小红书、公众号和知乎的三个版本。" \
  --tags 内容工作流,发布包 \
  --output-dir outputs/smoke-test >/dev/null

python3 "$REPO_ROOT/scripts/quickstart.py" \
  --yes \
  --product-name "Quickstart Smoke Test" \
  --primary-keywords "Quickstart Smoke Test,自动生成文章" \
  --secondary-keywords "内容审核,多平台发布" \
  --hotspot "可信内容工作流开始替代一键直发幻想" \
  --hotspot-summary "这是 quickstart 的非交互测试热点摘要，用来验证脚本可以产出 7 平台发布包。" \
  --outline-brief "围绕 quickstart 如何把知识库、关键词、热点和大纲串起来，解释先审核再发布的原因。" \
  --must-include-sections 核心结论,知识库价值,审核引擎,发布边界 \
  --audience "内容运营团队" \
  --content-type technical \
  --output-root outputs/quickstart-smoke-test >/dev/null

PYTHONPYCACHEPREFIX="$REPO_ROOT/.pycache" python3 -m ip_publisher.cli.run_phase1 \
  --request "$REPO_ROOT/data/tasks/demo-request.json" \
  --kb-dir "$REPO_ROOT/data/kb_raw" \
  --index-db "$REPO_ROOT/data/kb_index/phase1-test.db" \
  --output-root "$REPO_ROOT/outputs/phase1-smoke-test" >/dev/null

echo "Publish-pack and quickstart smoke tests passed."
echo "Phase 1 generate-and-audit smoke test passed."
echo "Try: bash scripts/setup.sh"
echo "Then run: python3 scripts/quickstart.py"
