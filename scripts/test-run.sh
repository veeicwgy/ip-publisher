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
  "$REPO_ROOT/skills/ip-publisher/SKILL.md"
  "$REPO_ROOT/skills/ip-profile/SKILL.md"
  "$REPO_ROOT/skills/hotspot-fetcher/SKILL.md"
  "$REPO_ROOT/skills/article-generator/SKILL.md"
  "$REPO_ROOT/skills/humanizer/SKILL.md"
  "$REPO_ROOT/skills/cover-generator/SKILL.md"
  "$REPO_ROOT/skills/multi-publisher/SKILL.md"
  "$REPO_ROOT/skills/github-open-source-site-rework/SKILL.md"
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
  --topic "Quickstart Smoke Test" \
  --angle "先跑通三平台改写，再决定后续怎么发布" \
  --body "这是 quickstart 的非交互测试正文，用来验证脚本可以直接产出三平台发布包。" \
  --tags 多平台改写,发布包 \
  --platforms xiaohongshu wechat_official zhihu \
  --output-dir outputs/quickstart-smoke-test >/dev/null

echo "Publish-pack and quickstart smoke tests passed."
echo "Try: bash scripts/setup.sh"
echo "Then run: python3 scripts/quickstart.py"
