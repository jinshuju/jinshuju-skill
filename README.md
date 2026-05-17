# 金数据 Skill

金数据（[Jinshuju](https://jinshuju.net)）官方 Skill。基于金数据 MCP，让 AI 助手通过自然语言完成表单搭建、数据管理与账单查询，**替代登录后台手工操作**。

## 功能概览

- **表单管理**：创建 / 复制 / 移动 / 编辑表单，调整主题；支持 **39 种字段类型**（含矩阵、商品、公式、关联表单、预约等），头图可由 AI 根据表单内容自动生成
- **数据管理**：查询、新增、批量修改与删除表单数据，支持字段值条件下推过滤（等值 / 区间 / 模糊 / 集合等）
- **账户与团队**：查看当前用户、企业套餐与用量、列出团队成员
- **账单查询**：查看电子发票与付款记录

## 目录结构

```
.
├── skills/jinshuju/
│   ├── SKILL.md              # 能力定义与使用规范
│   ├── references/
│   │   ├── tools.md          # 18 个 MCP 工具的完整输入 / 输出 / 错误参考
│   │   ├── guide.md          # 安装配置、效果展示、常见误区
│   │   └── examples.md       # 典型场景的 Prompt 与调用示例
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

API Key/Secret 的获取路径：金数据主页右上角个人头像 -> 个人中心 -> API

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

用户：给这个表单换个蓝紫色科技感的头图
助手：（调用 edit_theme.generate_header_image，AI 按表单主题生成头图）

用户：统计一下本月报名里手机号以 138 开头的有几条
助手：（list_entries 用 filters 把 like / created_at 条件下推到数据库，分页拉回）

用户：把这些人的"跟进状态"全部改成"已联系"
助手：（先展示命中记录并二次确认，确认后逐条调用 update_entry）

用户：我这个月还剩多少短信额度？什么时候到期？
助手：（调用 get_current_billing_account，从 plan / usage 字段拿到套餐 / 短信余额 / 到期日）
```

更多场景参见 [`references/examples.md`](skills/jinshuju/references/examples.md)，
每个工具的完整输入 / 输出参见 [`references/tools.md`](skills/jinshuju/references/tools.md)。

## 反馈

问题与建议请提交至本仓库 Issues。

## License

MIT
