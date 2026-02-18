# AiDocPlus-PromptTemplates

AiDocPlus 提示词模板资源仓库，包含 225 个内置提示词模板和分类定义。

## 资源内容

### 模板分类

报告写作、文章创作、邮件撰写、会议纪要、创意写作、技术文档、学术论文、翻译润色、数据分析、营销文案、教育教学、法律文书、公文写作、日常办公、通用

### 模板数量

225 个内置提示词模板，覆盖各类文档写作场景。

## 目录结构

```
data/
├── _meta.json                    # 分类定义
└── {category}/{id}/
    ├── manifest.json             # 模板元数据（名称、分类、标签、变量）
    └── content.md                # 模板内容（支持 {{变量}} 占位符）
scripts/
├── build.sh / build.py           # 构建 → dist/*.generated.ts
├── deploy.sh                     # 部署到 AiDocPlus 构建目标
└── extract_from_source.js        # 一次性提取脚本
```

## 构建和部署

```bash
bash scripts/build.sh      # 生成 prompt-templates.generated.ts + template-categories.generated.ts
bash scripts/deploy.sh      # 部署到 AiDocPlus/packages/shared-types/src/generated/
```

## 模板数据格式

**manifest.json**：
```json
{
  "id": "template-id",
  "name": "模板名称",
  "category": "category-key",
  "description": "模板描述",
  "variables": ["变量1", "变量2"],
  "isBuiltIn": true,
  "tags": ["标签1", "标签2"]
}
```

**content.md**：模板内容，支持 `{{变量名}}` 占位符语法。

## 生成文件

| 文件 | 部署位置 |
|------|----------|
| `prompt-templates.generated.ts` | `AiDocPlus/packages/shared-types/src/generated/` |
| `template-categories.generated.ts` | `AiDocPlus/packages/shared-types/src/generated/` |
