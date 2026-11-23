# 金数据 Skill

[![skills.sh](https://skills.sh/b/jinshuju/jinshuju-skill)](https://skills.sh/jinshuju/jinshuju-skill)

金数据官方 Skill，基于金数据 MCP Server，让 AI 助手通过自然语言完成表单搭建、数据管理、账户查询与工作流自动化。

## 适合谁使用

- 希望通过 AI 助手查询、整理或维护金数据表单数据的团队
- 希望让 AI Agent 创建表单、修改字段或处理日常数据工作的开发者
- 正在将金数据接入 MCP、Agent 或自动化工作流的用户

## 快速开始

### 1. 配置 MCP 连接器

金数据 MCP Server 地址：

```text
https://jinshuju.net/mcp
```

推荐使用 OAuth 方式授权；如果你的 AI 客户端暂不支持 OAuth，也可以在请求头里带访问令牌（`Authorization: Bearer <token>`）。旧的 API Key / Secret（Basic）方式已不再支持。

详细配置方式请查看：[金数据 MCP Server 文档](https://open.jinshuju.net/mcp/)。

### 2. 安装 Skill

推荐使用 [skills CLI](https://www.skills.sh/) 一键安装：

```bash
# 装到当前项目（默认）
npx skills add jinshuju/jinshuju-skill

# 装到用户全局，并指定 AI 客户端
npx skills add jinshuju/jinshuju-skill -g -a claude-code
```

支持 Claude Code、Codex、Cursor、OpenCode 等 50+ 客户端。

也可以手动安装：将 `skills/jinshuju/` 目录放入你的 AI 客户端 Skill 目录，重启客户端使其加载。

### 3. 验证

在对话里发送：

> 列一下我金数据里的表单

如果 AI 助手能返回你的表单列表，说明连接成功。

## 支持的能力

- **表单管理**：创建 / 复制 / 移动 / 编辑 / 删除表单，调整主题；支持 39 种字段类型（含矩阵、商品、公式、关联表单、预约等），头图可由 AI 根据表单内容自动生成；考试与测评表单
- **多维表格**：建表、增删改列（含公式、编号、关联、查找引用、汇总列）
- **数据管理**：查询、新增（单条或批量导入）、批量修改与删除数据，写数据评论，支持字段值条件下推过滤（等值 / 区间 / 模糊 / 集合等）；Excel / CSV 文件导入
- **统计与搜索**：服务端计数、分组、趋势与整表画像，跨表单搜关键字
- **视图与对外查询页**：表格 / 看板视图，让访客自助查数据
- **账户与团队**：查看当前用户、企业套餐与用量、团队成员、收款商户

## 使用示例

```text
用户：帮我建一个“2026 春季产品发布会”报名表，要姓名、手机号、公司、职位
助手：（调用 create_form 创建表单并返回链接与 form_token）

用户：给这个表单换个蓝紫色科技感的头图
助手：（调用 edit_theme.generate_header_image，AI 按表单主题生成头图）

用户：统计一下本月报名里手机号以 138 开头的有几条
助手：（list_entries 用 filters 把 like / created_at 条件下推到数据库，分页拉回）

用户：把这些人的“跟进状态”全部改成“已联系”
助手：（先展示命中记录并二次确认，确认后用 patch_entries 批量更新）

用户：我这个月还剩多少短信额度？什么时候到期？
助手：（调用 get_current_billing_account，从 plan / usage 字段拿到套餐 / 短信余额 / 到期日）
```

更多场景参见 [`references/examples.md`](skills/jinshuju/references/examples.md)，工具分类参见 [`references/tools.md`](skills/jinshuju/references/tools.md)。

## 目录结构

```text
.
├── skills/jinshuju/
│   ├── SKILL.md              # 能力定义与使用规范
│   ├── references/
│   │   ├── tools.md          # MCP 工具地图（参数以 MCP 自带描述与 get_schema 为准）
│   │   ├── guide.md          # 安装配置、效果展示、常见误区
│   │   └── examples.md       # 典型场景的 Prompt 与调用示例
│   └── scripts/
│       └── setup.py          # MCP 连接器安装辅助脚本
├── connector/jinshuju/       # Connector 包：MCP 连接配置 + 精简版 Skill
├── expert/
│   ├── jinshuju-form-expert/ # 表单专家（Agent + 内置 Skill + MCP 依赖）
│   └── jinshuju-table-expert/# 表格专家（Agent + 内置 Skill + MCP 依赖）
└── icons/
    └── icon.svg              # 品牌图标
```

## 维护状态

本仓库由金数据团队维护。问题与建议请提交至本仓库 Issues。

## License

MIT
