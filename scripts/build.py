#!/usr/bin/env python3
"""
AiDocPlus-PromptTemplates 构建脚本
扫描 data/ 目录，生成 prompt-templates.generated.ts 和 template-categories.generated.ts
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(REPO_DIR, "data")
DIST_DIR = os.path.join(REPO_DIR, "dist")

os.makedirs(DIST_DIR, exist_ok=True)


def ts_string(s: str) -> str:
    if "\n" in s:
        escaped = s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
        return f"`{escaped}`"
    else:
        return json.dumps(s, ensure_ascii=False)


def ts_string_array(arr: list) -> str:
    items = ", ".join(json.dumps(x, ensure_ascii=False) for x in arr)
    return f"[{items}]"


def find_templates(data_dir: str):
    templates = []
    for root, dirs, files in os.walk(data_dir):
        if "manifest.json" in files and "content.md" in files:
            manifest_path = os.path.join(root, "manifest.json")
            content_path = os.path.join(root, "content.md")
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            with open(content_path, "r", encoding="utf-8") as f:
                content = f.read()
            templates.append((manifest, content))
    templates.sort(key=lambda t: (t[0].get("majorCategory", ""), t[0].get("order", 0)))
    return templates


def load_categories(data_dir: str):
    meta_path = os.path.join(data_dir, "_meta.json")
    if not os.path.exists(meta_path):
        return {}
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return meta.get("categories", [])


def generate_templates_ts(templates):
    entries = []
    for manifest, content in templates:
        lines = []
        lines.append("  {")
        lines.append(f"    id: {ts_string(manifest['id'])},")
        lines.append(f"    name: {ts_string(manifest.get('name', ''))},")
        lines.append(f"    category: {ts_string(manifest.get('majorCategory', 'general'))},")
        lines.append(f"    content: {ts_string(content.strip())},")
        lines.append(f"    isBuiltIn: true,")
        if manifest.get("description"):
            lines.append(f"    description: {ts_string(manifest['description'])},")
        if manifest.get("variables"):
            var_names = [v["name"] if isinstance(v, dict) else v for v in manifest["variables"]]
            lines.append(f"    variables: {ts_string_array(var_names)},")
        lines.append("  },")
        entries.append("\n".join(lines))

    return f"""/**
 * 自动生成文件 — 请勿手动编辑
 * 由 AiDocPlus-PromptTemplates/scripts/build.py 生成
 */
import type {{ PromptTemplate }} from '../index';

export const BUILT_IN_TEMPLATES: PromptTemplate[] = [
{chr(10).join(entries)}
];
"""


def generate_categories_ts(categories):
    entries = []
    for cat in categories:
        key = cat["key"]
        name = cat["name"]
        icon = cat.get("icon", "📋")
        entries.append(f"  {ts_string(key)}: {{ name: {ts_string(name)}, icon: {ts_string(icon)}, isBuiltIn: true }},")

    return f"""/**
 * 自动生成文件 — 请勿手动编辑
 * 由 AiDocPlus-PromptTemplates/scripts/build.py 生成
 */
import type {{ TemplateCategoryInfo }} from '../index';

export const TEMPLATE_CATEGORIES: Record<string, TemplateCategoryInfo> = {{
{chr(10).join(entries)}
}};
"""


def main():
    print("🔨 构建提示词模板数据...")
    templates = find_templates(DATA_DIR)
    categories = load_categories(DATA_DIR)

    if not templates:
        print("⚠️  未找到任何模板数据")
        sys.exit(1)

    # 生成 prompt-templates.generated.ts
    ts_content = generate_templates_ts(templates)
    output_path = os.path.join(DIST_DIR, "prompt-templates.generated.ts")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ts_content)
    print(f"   ✅ {output_path}")

    # 生成 template-categories.generated.ts
    cat_content = generate_categories_ts(categories)
    cat_output = os.path.join(DIST_DIR, "template-categories.generated.ts")
    with open(cat_output, "w", encoding="utf-8") as f:
        f.write(cat_content)
    print(f"   ✅ {cat_output}")

    print(f"✅ 构建完成: {len(templates)} 个模板, {len(categories)} 个分类")


if __name__ == "__main__":
    main()
