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
  "$REPO_ROOT/skills/ip-publisher/SKILL.md"
  "$REPO_ROOT/skills/ip-profile/SKILL.md"
  "$REPO_ROOT/skills/hotspot-fetcher/SKILL.md"
  "$REPO_ROOT/skills/article-generator/SKILL.md"
  "$REPO_ROOT/skills/humanizer/SKILL.md"
  "$REPO_ROOT/skills/cover-generator/SKILL.md"
  "$REPO_ROOT/skills/multi-publisher/SKILL.md"
)

for file in "${required_files[@]}"; do
  [ -f "$file" ] || { echo "Missing file: $file"; exit 1; }
done

echo "All core files exist."
echo "Try: bash scripts/setup.sh"
echo "Then say: 帮我写一篇小红书文章"
