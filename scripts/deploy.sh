#!/bin/bash
# AiDocPlus-PromptTemplates deploy.sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
PARENT_DIR="$(dirname "$REPO_DIR")"
TARGET_DIR="${PARENT_DIR}/AiDocPlus"
DIST_DIR="${REPO_DIR}/dist"
DATA_DIR="${REPO_DIR}/data"

echo "[deploy] AiDocPlus-PromptTemplates -> ${TARGET_DIR}"

# 1. 部署 generated TypeScript 文件
GENERATED_DIR="${TARGET_DIR}/packages/shared-types/src/generated"
mkdir -p "$GENERATED_DIR"

for f in prompt-templates.generated.ts template-categories.generated.ts; do
  if [ -f "${DIST_DIR}/${f}" ]; then
    cp "${DIST_DIR}/${f}" "${GENERATED_DIR}/"
    echo "   [ok] ${f} -> generated/"
  else
    echo "   [warn] dist/${f} 不存在，请先运行 build.sh"
  fi
done

# 2. 部署模板数据到 bundled-resources
BUNDLED_DIR="${TARGET_DIR}/apps/desktop/src-tauri/bundled-resources/prompt-templates"
mkdir -p "$BUNDLED_DIR"

# 复制 _meta.json
if [ -f "${DATA_DIR}/_meta.json" ]; then
  cp "${DATA_DIR}/_meta.json" "${BUNDLED_DIR}/"
fi

# 复制所有模板目录（按分类/ID 结构）
TEMPLATE_COUNT=0
find "$DATA_DIR" -name "manifest.json" -not -path "*/_meta.json" | while read -r manifest_file; do
  tmpl_dir="$(dirname "$manifest_file")"
  # 获取相对路径（如 editing/polish-pro）
  rel_path="${tmpl_dir#${DATA_DIR}/}"
  target_dir="${BUNDLED_DIR}/${rel_path}"
  mkdir -p "$target_dir"
  cp "${tmpl_dir}/manifest.json" "$target_dir/"
  [ -f "${tmpl_dir}/content.md" ] && cp "${tmpl_dir}/content.md" "$target_dir/"
done

TOTAL=$(find "$DATA_DIR" -name "manifest.json" -not -path "*/_meta.json" | wc -l | tr -d ' ')
echo "   [ok] ${TOTAL} 个模板 -> bundled-resources/prompt-templates/"
echo "[done] AiDocPlus-PromptTemplates 部署完成"
