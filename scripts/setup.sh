#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_DIR="$HOME/.ip-publisher"
DEPS_DIR="$CONFIG_DIR/deps"
PROFILE_PATH="$CONFIG_DIR/profile.yaml"

mkdir -p "$CONFIG_DIR" "$DEPS_DIR"

python3 "$REPO_ROOT/scripts/install-deps.py"

clone_repo() {
  local url="$1"
  local dir="$2"
  if [ ! -d "$dir/.git" ]; then
    git clone --depth 1 "$url" "$dir"
  fi
}

clone_repo https://github.com/oaker-io/wewrite.git "$DEPS_DIR/wewrite"
clone_repo https://github.com/op7418/Humanizer-zh.git "$DEPS_DIR/Humanizer-zh"
clone_repo https://github.com/jimliu/baoyu-skills.git "$DEPS_DIR/baoyu-skills"
clone_repo https://github.com/wechatsync/Wechatsync.git "$DEPS_DIR/Wechatsync"

if [ ! -f "$PROFILE_PATH" ]; then
  cp "$REPO_ROOT/config/ip-profile-template.yaml" "$PROFILE_PATH"
  if [ -t 0 ]; then
    read -rp "请输入你的 IP 名称: " ip_name
    read -rp "请输入你的职业/领域: " profession
    read -rp "请输入你的写作风格: " writing_style
    read -rp "请输入你的目标受众: " target_audience
    IP_NAME="$ip_name" \
    PROFESSION="$profession" \
    WRITING_STYLE="$writing_style" \
    TARGET_AUDIENCE="$target_audience" \
    PROFILE_PATH="$PROFILE_PATH" \
    python3 - <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["PROFILE_PATH"])
text = path.read_text(encoding="utf-8")
replacements = {
    'name: ""': f'name: {json.dumps(os.environ.get("IP_NAME", ""), ensure_ascii=False)}',
    'profession: ""': f'profession: {json.dumps(os.environ.get("PROFESSION", ""), ensure_ascii=False)}',
    'writing_style: ""': f'writing_style: {json.dumps(os.environ.get("WRITING_STYLE", ""), ensure_ascii=False)}',
    'target_audience: ""': f'target_audience: {json.dumps(os.environ.get("TARGET_AUDIENCE", ""), ensure_ascii=False)}',
}
for source, target in replacements.items():
    text = text.replace(source, target, 1)
path.write_text(text, encoding="utf-8")
PY
  fi
fi

for target in "$HOME/.claude/skills" "$HOME/.config/claude/skills" "$HOME/.openclaw/skills"; do
  mkdir -p "$target"
  for skill_dir in "$REPO_ROOT"/skills/*; do
    name="$(basename "$skill_dir")"
    rm -rf "$target/$name"
    cp -R "$skill_dir" "$target/$name"
  done
done

echo "IP Publisher 安装完成。"
echo "人设文件: $PROFILE_PATH"
echo "现在可以对 Claude 或 OpenClaw 说：帮我写一篇小红书文章"
