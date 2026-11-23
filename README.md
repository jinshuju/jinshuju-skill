# 金数据 TRAE Plugin（Jinshuju）

用自然语言在[金数据](https://jinshuju.net)上搭建表单与数据表格、批量管理数据，替代登录后台手动操作。

金数据（jinshuju.net）是中国领先的在线表单与数据收集平台，提供表单搭建、数据收集、支付收款、数据表格（AI 表格）等能力。

## 能力列表

| 能力 | 说明 |
|---|---|
| 表单搭建 | 创建 / 复制 / 编辑在线表单与主题，含自动判分的考试表单、选项计分的测评表单 |
| 表单数据管理 | 查询、新增（单条或批量）、更新、删除、批量修改表单数据（entries） |
| 数据表格 | 创建 / 编辑数据表与列（含公式列），增删改查与批量维护行数据 |
| 文件上传 | 用上传凭证上传本地图片或附件 |
| 账户信息 | 查询账户套餐额度与团队成员 |

## 包内结构与关系

```
jinshuju/
├── .trae-plugin/plugin.json      # 插件清单
├── skills/
│   ├── jinshuju-form/            # Skill：表单搭建与表单数据管理
│   │   ├── SKILL.md
│   │   └── references/           # 工具说明、字段规则、示例
│   └── jinshuju-table/           # Skill：数据表格与行数据管理
│       ├── SKILL.md
│       └── references/
├── .mcp.json                     # Remote MCP：https://jinshuju.net/mcp
├── connector.json                # Remote MCP Connector（OAuth 授权）
├── icon.svg                      # 插件图标（金数据官方图标）
└── LICENSE                       # MIT
```

- **MCP** 提供全部工具调用能力：`.mcp.json` 声明的 `jinshuju` 是一个 HTTP Remote MCP（Streamable HTTP），服务地址 `https://jinshuju.net/mcp`，无本地命令与本地依赖。
- **Connector** 负责认证：`connector.json` 声明 `remote_mcp` 类型 Connector，指向 `.mcp.json` 中的 `jinshuju` server，`auth_policy` 为 `ON_INVOKE`。
- **Skill** 提供任务路由与使用知识：`jinshuju-form` 处理在线表单场景，`jinshuju-table` 处理数据表格场景；两者共用同一个 MCP 的 entries 工具，SKILL.md 中已写明各自的触发与排除条件。

## 认证方式

金数据 MCP 为标准 Remote MCP OAuth：首次调用工具时由 TRAE 触发 OAuth 授权，用户在金数据完成登录授权后，运行时在 MCP 请求中携带授权结果。插件包内不含任何真实凭据，也无需用户手动填写 API Key。

平台侧 Connector Provider Template 所需的 Remote MCP 服务地址：

```json
{
  "mcp": {
    "server_url": "https://jinshuju.net/mcp"
  }
}
```

## 依赖与运行

- 无本地命令、无本地运行时依赖（纯 HTTP Remote MCP），支持系统不限（Universal）。
- 外部服务：金数据（https://jinshuju.net），由金数据官方运营。
- 项目来源：https://github.com/jinshuju/jinshuju-skill

## 验证方式

1. 安装插件后，对 AI 说："帮我做一个训练营报名表，299 元一位，限 60 人报名"。
2. 首次调用会弹出金数据 OAuth 授权，完成登录授权。
3. AI 应通过 `create_form` 等工具建出表单并返回表单链接。

## 已知限制

- 需要金数据账号；部分能力（如支付表单、批量数据量上限）受账户套餐限制，可通过 `get_current_billing_account` 工具查询额度。
- 工具仅操作用户已授权账户内的表单与数据。

## 许可证

MIT，见 [LICENSE](./LICENSE)。
