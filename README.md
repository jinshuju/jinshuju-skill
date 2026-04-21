# 金数据 Skill

金数据（[Jinshuju](https://jinshuju.net)）官方 Skill。基于金数据 MCP，让 AI 助手通过自然语言完成表单搭建、数据管理与账单查询，**替代登录后台手工操作**。

## 功能概览

- **表单管理**：创建 / 复制 / 编辑表单、调整主题，支持 AI 生成头图
- **数据管理**：查询、新增、批量修改与删除表单数据
- **账单查询**：查看电子发票与付款记录

## 目录结构

```
.
├── skills/jinshuju/
│   ├── SKILL.md              # 能力定义与使用规范
│   ├── references/
│   │   ├── guide.md          # 字段类型、主键与工具调用指引
│   │   └── examples.md       # 典型场景示例
│   └── scripts/
│       └── setup.py          # MCP 连接器安装辅助脚本
└── icons/
    └── icon.svg              # 品牌图标
```

## 快速开始

### 1. 获取金数据 API 凭证

登录[金数据后台](https://jinshuju.net) → **个人设置 → API / 开发者**，创建并复制 `API Key` / `API Secret`。

### 2. 配置 MCP 连接器

金数据 MCP 服务端点：`https://jinshuju.net/mcp`

支持两种认证方式，任选其一：

**方式 A · HTTP Basic（API Key/Secret）**

```bash
python3 skills/jinshuju/scripts/setup.py --print-json YOUR_API_KEY YOUR_API_SECRET
```

把输出的 JSON 片段粘贴到 AI 客户端的 MCP 配置中。

**方式 B · OAuth 2.0**

在 AI 客户端的连接器管理中添加自定义连接器：

- Name：`jinshuju`
- URL：`https://jinshuju.net/mcp`

点击添加后按提示授权即可，无需手动生成凭证。

### 3. 安装 Skill

将 `skills/jinshuju/` 目录放入你的 AI 客户端 Skill 目录，重启客户端使其加载。

### 4. 验证

在对话里发送：

> 列一下我金数据里的表单

## 使用示例

```
用户：帮我建一个"2026 春季产品发布会"报名表，要姓名、手机号、公司、职位
助手：（调用 create_form 创建表单并返回链接与 form_token）

用户：统计一下本月报名里手机号以 138 开头的有几条
助手：（调用 list_entries 拉取数据，本地过滤后以 Markdown 表格展示）

用户：把这些人的"跟进状态"全部改成"已联系"
助手：（先展示命中记录并二次确认，确认后逐条调用 update_entry）
```

更多场景参见 [`references/examples.md`](skills/jinshuju/references/examples.md)。

## 反馈

问题与建议请提交至本仓库 Issues。

## License

MIT
