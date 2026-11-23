---
name: jinshuju-table
slug: jinshuju-table
displayName: 金数据AI表格
description: "通过金数据（Jinshuju，jinshuju.net）MCP 操作用户托管在金数据平台上的数据表格：创建 / 编辑 / 移动数据表与列（含公式、编号、关联、查找引用、汇总等自动计算列）；查询、新增（单条或批量）、更新、批量更新、删除行数据，给行写评论，或把本地 Excel / CSV 批量导入数据表；上传本地文件写入附件列；建视图与对外填写页；在服务端统计行数据（条数、分组、按天 / 周 / 月的趋势、整表列分布画像），跨表搜关键字；查询账户套餐额度与团队成员。仅在用户操作其金数据数据表时使用——触发信号：提到 金数据表格 / Jinshuju 表格 / 数据表，或要在金数据上建表、加改列、批量维护行数据。不要用于：用代码开发表格系统、把本地文件当普通文档分析（与导入到金数据数据表无关时）、搭建对外收集的表单 / 问卷、图片 / 票据 OCR，以及与金数据平台无关的通用数据处理。"
version: 2.0.0
author: Jinshuju
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [Tables, Database, Data Management, Productivity, 金数据表格]
    category: productivity
    related_skills: []
---

# 金数据表格（Jinshuju Tables）

金数据（jinshuju.net）的**数据表格**是以「列 + 行」组织的结构化数据表（类似多维表格 / 在线数据库）。通过金数据 MCP，你可以用自然语言完成数据表搭建与行数据管理的全流程，**替代登录后台手动操作**。

数据表格与用于对外收集的「在线表单」是不同产品：数据表用 `create_table` / `get_table` / `edit_table` 建改；行数据（entries）两者共用同一批数据工具，`form_token` 参数传**表 token**。本 skill 只处理数据表格。

## When to Use

本 skill **仅处理金数据数据表格（jinshuju.net）** 的表结构与行数据管理，且需满足以下任一**平台信号**才触发：

- 用户明确提到"金数据表格"、"Jinshuju 表格"、"数据表"
- 用户要在金数据上**建数据表、加 / 改列、移动表、增删改查或批量维护行数据**
- 用户上传了 Excel / CSV 并要把它**导入到金数据的某张数据表**
- 用户要查询本账户的套餐额度、团队成员

## When NOT to Use

以下场景**不要**用本 skill，直接退出、交给通用能力处理：

- 用代码 / 程序开发表格、数据库系统
- 纯本地处理文件、Excel / CSV、文档分析（**若目标是把这份表格导入到金数据某数据表，则属于本 skill**）
- 搭建对外收集的**表单 / 问卷 / 报名表**（那是金数据表单产品，另有专家 / skill）
- 图片、账单、票据的 OCR / 识别
- 与金数据平台无关的通用数据处理

判断不属于金数据数据表操作时，**不要调用任何 MCP 工具**，按通用能力回答即可。

## 参数以 MCP 为准

金数据 MCP 的工具由开放 API v1 的 openapi.yaml 自动生成，随 API 同步更新。**每个工具的参数、取值、返回结构以 MCP 自带的工具描述为准**，本 skill 只讲"什么场景用哪个工具、按什么顺序、哪里容易踩坑"，不重复参数细节。

- `create_table` 的列定义按类型分支：`get_schema("<Type>ColumnInput")` 看该类型的列能设哪些属性（如 `NumberFieldColumnInput`、`RelationFieldColumnInput`），**不要猜**
- 参数描述里写着 `Shape: schema "X"` 的，同样调 `get_schema("X")`（视图看 `FormViewInput`）
- 报错会带 HTTP 状态和服务端的 `error_description` / `errors`，通常直接列出可用的列 / operator / 取值——照着改参数再试

工具清单与分类见 [`references/tools.md`](references/tools.md)。

## Quick Reference

| 场景 | MCP 工具 |
|------|----------|
| 找数据表（拿 table_token） | `list_tables`（`q` 按名称模糊搜） |
| 看表结构（列 api_code） | `get_table` |
| 建表 | `create_table` |
| 改表名 / 增删改列 | `edit_table` |
| 删列 / 选项前查有没有数据 | `check_field_data` |
| 改列类型前预览数据损失 | `preview_field_type_change` |
| 文件夹 / 移动表 | `list_folders` / `create_folder` / `move_table` |
| 列行数据（筛选 / 裁列 / 排序 / 关键字） | `list_entries` |
| 单行 | `get_entry` / `create_entry` / `update_entry` / `delete_entry` |
| 批量新建 / 批量更新（≤200 行/次） | `create_entries` / `patch_entries` |
| 只要行数 | `count_entries` |
| 服务端统计（求和 / 均值 / 分位 / 分组 / 趋势） | `aggregate_entries` |
| 整表画像 | `get_form_data_summary` |
| 跨表搜关键字（≤10 张） | `search_entries_in_forms` |
| 行评论 | `list_entry_comments` / `create_entry_comment` / `update_entry_comment` / `delete_entry_comment` |
| 视图（含对外填写页） | `list_form_views` / `get_form_view` / `create_form_view` / `edit_form_view` / `delete_form_view` / `list_form_view_entries` |
| 导入 Excel / CSV | `prepare_import_file_upload`（或 `upload_import_file`）→ `import_entries_from_file` |
| 上传附件 | `prepare_entry_attachment_upload`（无 shell 时用 `upload_entry_attachment`） |
| 账户 | `get_current_user` / `get_current_billing_account` / `list_account_users` |
| 读参数结构 | `get_schema` |

## Procedure

### 原则

> ⚠️ **绝不绕过 MCP**：金数据 MCP 工具不可用（未连接 / 授权失败 / 调用持续报错）时**立即停止**，**禁止**改用浏览器自动化（Playwright 等）、直接调 REST API、curl 或模拟后台操作来替代。正确做法见下方「MCP 不可用时」。（唯一例外：`prepare_*_upload` 明确要求用 `curl -F` 把本地文件传到它给的一次性 `upload_url`。）

1. **先看再动**：操作未知数据表前，先 `get_table` 拿列结构。写行数据时 entry 的键**必须是列 `api_code`**，传中文列名会被丢弃；选项值可以传选项 api_code 或选项文字。

2. **条件下推优先**：`list_entries`（`form_token` 传表 token）用 `filters` 把条件下推到数据库；不知道值在哪一列就用 `keyword` 一次搜整张表。用 `fields` 只取需要的列、用 `sort` 让服务端排序。默认每页 50 行、`limit` 最大 1000；翻页把上一页的 `next` 原样回传。

3. **统计不拉全量**：问"多少行 / 合计多少 / 哪类最多 / 趋势怎么样"时**不要**翻页拉行数据回来自己算——行数用 `count_entries`；具体数字、分组、按天 / 周 / 月趋势用 `aggregate_entries`；整表每列的分布用 `get_form_data_summary`。列支持哪些聚合函数、能不能分组，用 `get_table(include_analytics=true)` 看每列的 `analytics`。

4. **先列再改**：批量操作前先 `list_entries` 拉出命中行展示给用户，**用户确认后**再执行——批量更新用 `patch_entries`（≤200/批）；删除逐行循环 `delete_entry`，每 20 行汇报一次进度。

5. **删除要确认**：`delete_entry`、删列 / 选项、`delete_form_view`、`delete_entry_comment` 都必须得到用户显式确认。删列 / 选项前先 `check_field_data`，有数据时把影响告诉用户。

6. **脱敏展示**：输出手机号 / 邮箱默认打码（`138****1234`），除非用户明确要求原文。

7. **不静默吞错**：列类型不支持、套餐限制、权限不足的报错原文回显并给出替代方案。

### 典型任务流

**① 新建数据表**
```
1. 对要用的列类型 get_schema("<Type>ColumnInput")
2. create_table(name, fields)
   - 列类型只有 15 种，见下方「支持的列类型」；单选 / 多选列传 choices
   - 建完暂时没数据进：传 with_default_entries:true 补 3 行空行；紧接着要写数据就别开
   - 要放进文件夹：folder_token 只能是 kind="table" 的文件夹（list_folders 看 kind）
3. 返回表结构与 token
```

**② 加 / 改列**
```
1. get_table → 记下现有列的 api_code
2. edit_table，用 fields 增量操作：add / remove / update / update_choices
   - 删列 / 删选项前先 check_field_data，有数据要用户确认
   - 改列类型前先 preview_field_type_change；会清数据的改动要带 confirm_data_loss:true
   - 改选项文字用 update_choices.update（保留 api_code）
```

**③ 条件查询 / 导出行**
```
1. get_table → 记下列 api_code 和选项 api_code
2. list_entries（form_token 传表 token）用 filters 下推条件；只要几列传 fields；
   不想再对照 get_table 翻译表头可传 include_labels:true
3. next 翻页拿全部数据
4. Markdown 表格展示，敏感列脱敏
5. 询问用户是否需要生成 CSV
```

**④ 批量更新行**
```
1. get_table → 拿目标列 api_code
2. list_entries + filters 拉出命中集，展示前 10 行 + 总数
3. 用户确认后 patch_entries 一次提交（每行 { serial_number, entry }，每批 ≤200）
   注意：patch_entries 不能写附件列，附件只能逐行 update_entry
4. 读返回的 failed_rows，向用户汇总成功 / 失败
```

**⑤ 批量写入行（对话里给的 / 粘贴的表格）**
```
1. get_table → 拿目标列 api_code
2. 每行整理成 { api_code: value }
3. create_entries 一次提交（每批 ≤200）
4. 读返回的 errors（按下标）汇总；不幂等，失败后只补 errors 里的行
```

**⑥ 从本地 Excel / CSV 文件导入**
```
1. 读本地文件看表头；get_table 拿目标列 api_code
2. prepare_import_file_upload(form_token=表 token) → curl -F file=@<path> <upload_url>，拿 attachment_id
   （没有 shell 时用 upload_import_file 传 Base64；粘贴的表格文本走 ⑤）
3. import_entries_from_file(attachment_id, columns=[{field_api_code, column_label | sheet_column_index}])
   需要去重传 unique_field_code
4. 返回 201 = 后台任务已开始：告诉用户"导入已开始，进度看数据页"，然后停手；
   报错 = 一行都没导入，按错误改映射后重试一次
```

**⑦ 移动数据表到文件夹**
```
1. list_folders 找 kind="table" 的文件夹（没有就 create_folder(name, kind:"table")）
2. move_table(table_token, folder_token)；移出文件夹传 folder_token:null
```

**⑧ 行数据统计 / 分析**
```
1. count_entries 先探范围（form_token 填表 token）
2. get_table(include_analytics=true) 看列的 agg_funcs / groupable
3. aggregate_entries：metrics 1~20 个；dimensions 最多 2 列，日期列必须带 bucket（day/week/month）
   结果按第一个指标降序，limit 默认 20 / 上限 200；看 row_count + truncated
4. get_form_data_summary 一次拿整表画像
5. 维度值 null = 该列没填的那一组，别丢
```

**⑨ 视图与对外填写页**
```
1. create_form_view(form_token=表 token, view={...})，结构见 get_schema("FormViewInput")
   view_type：grid / kanban / stats / form（form = 对外填写页，只有表格支持）
2. 填写页默认 published:false，链接不可用；确认后再 edit_form_view 发布
3. 按视图取数用 list_form_view_entries
```

### 支持的列类型

| 列类型 | 说明 |
|--------|------|
| `TextArea` | 文本 |
| `NumberField` | 数字（小数位用 `display_precision`，不能用 `precision`） |
| `DateTimeField` | 日期时间 |
| `BooleanField` | 勾选 |
| `MobileField` / `EmailField` / `LinkField` | 手机号 / 邮箱 / 链接 |
| `RadioButton` / `CheckBox` | 单选 / 多选（传 `choices`，没有"其他"选项） |
| `AttachmentField` | 附件（不接受数量 / 大小限制） |
| `FormulaField` | 公式（只读）：`formula` 里已有列写 api_code，同一请求新建的列写 `$(cid)` |
| `SequenceField` | 自动编号（只读） |
| `RelationField` | 关联另一张表（默认双向，会在对方表建反向列） |
| `LookupField` / `RollupField` | 通过关联列查找引用 / 汇总对方表的列（只读） |

各类型的完整属性用 `get_schema("<Type>ColumnInput")` 查。

## Pitfalls

- **entry 键写成中文列名** → 被丢弃，全丢光时报 `Entry attributes cannot be empty` 并列出被丢的键；键必须是列 `api_code`
- **简单列值包成对象**（`{"value": "abc"}`）→ 直接传字符串；各类型写法见 `create_entry` 的 `entry` 描述里的表格
- **写入公式 / 编号 / 查找引用 / 汇总列** → 只读，写入被忽略
- **`like` 带 SQL 通配符**（`"张%"`）→ 按字面匹配 `%`，查不到；直接传 `"张"`
- **operator 与列类型不匹配** → 400，错误信息列出可用 operator
- **批量新建循环调 `create_entry`** → 用 `create_entries`（≤200 行/批，部分成功，不幂等）
- **批量更新循环调 `update_entry`** → 用 `patch_entries`；但它**不能写附件列**
- **`update_entry` 改附件列只传新文件** → 附件按整组替换，要保留旧文件就把读到的 URL / attachment id 一起传回
- **给附件列设数量 / 大小限制** → 被拒
- **给数字 / 公式列传 `precision`** → 被拒；表格列用 `display_precision`
- **用 `get_form` / `edit_form` / `move_form` 操作数据表** → 用 `get_table` / `edit_table` / `move_table`
- **建 `RelationField` 关联到表单或没有管理权限的表** → 只能关联另一张你能管理的表格
- **`LookupField` / `RollupField` 的关联列还没建好** → 先建 `RelationField` 并关联上，再引用它的 api_code
- **改选项文案用 remove + add** → 会换 api_code；改名用 `update_choices.update`
- **删列 / 选项不先查数据** → 有数据的会被永久清除；先 `check_field_data`
- **`create_table` 建空表不传 `with_default_entries`** → 空网格看着像坏了；紧接着要写数据就别开
- **把数据表移进表单文件夹** → 只能进 `kind="table"` 的文件夹；移出文件夹必须显式传 `folder_token: null`
- **`import_entries_from_file` 后重复调用 / 自己再逐行写** → 它是后台任务，调一次即可
- **要统计却翻页拉全量行数据自己算** → 用 `count_entries` / `aggregate_entries` / `get_form_data_summary`
- **多选列当 `dimensions`** → 被拒；多选列的分布用 `get_form_data_summary`
- **日期列维度不传 `bucket`** → 出不来趋势
- **把分组结果当全量** → 看 `row_count` 和 `truncated`
- **聚合类工具按 `creator_id` / `serial_number` 过滤** → 被拒
- **评论里 @ 非协作者** → 整条评论被拒
- **限流（HTTP 429）把原始 JSON 抛给用户** → 告知"接口请求频繁，稍后重试"，按 `Retry-After` 等待，合并可批量的请求

## Verification

操作完成后确认：
- **创建 / 编辑数据表**：返回表 token 与预期的列结构（列 `api_code`、类型）
- **move_table**：`get_table` / `list_tables` 显示表已在目标文件夹
- **import_entries_from_file**：调用成功即任务已入队；让用户去数据页看进度
- **create_entry**：返回包含 `serial_number`
- **create_entries**：`errors` 为空（部分失败时按下标核对原因）
- **patch_entries**：`failed_rows` 为空（部分失败时按 serial_number 核对 reason）
- **aggregate_entries**：分组时核对 `row_count` 与 `truncated` 再下结论
- **批量操作**：向用户汇报"共 N 行，成功 X 行，失败 Y 行"

## MCP 配置

金数据 MCP 端点：`https://jinshuju.net/mcp`（表单与表格共用同一端点，远程 HTTP）。

**方式 A · OAuth（推荐）**：客户端里添加连接器、填上面的地址，按提示登录金数据授权即可。
```json
{ "mcpServers": { "jinshuju-table": { "url": "https://jinshuju.net/mcp" } } }
```

**方式 B · 访问令牌**：在请求头里带 `Authorization: Bearer <访问令牌>`。
```json
{
  "mcpServers": {
    "jinshuju-table": {
      "url": "https://jinshuju.net/mcp",
      "headers": { "Authorization": "Bearer YOUR_ACCESS_TOKEN" }
    }
  }
}
```
个人访问令牌在「个人资料 → API」（https://next.jinshuju.net/profile/api）创建；账户访问令牌在「系统设置 → 账户 API」（https://next.jinshuju.net/system/api_licence）创建。只支持本地 MCP 的客户端可用 `npx -y @jinshuju/mcp`，令牌放在环境变量 `JINSHUJU_ACCESS_TOKEN`。

常见配置错误：漏 `/mcp` 后缀、用 `http://`、`Authorization` 缺 `Bearer ` 前缀、还在用旧的 `Basic`（API Key / Secret）凭证——旧凭证已不再支持，换成访问令牌或 OAuth。

### MCP 不可用时

工具未连接 / 授权失败 / 持续报错时，按顺序降级，**不要**用任何非标方式替代：

1. 告知用户"金数据 MCP 未就绪"，不要假装已完成操作。
2. 对照上面的「常见配置错误」引导排查（端点、`Bearer ` 前缀、OAuth 授权等）。
3. 仍不行，就给出在金数据后台（jinshuju.net）手动操作的步骤指引。

> 超宽表（几十列）即使 MCP 正常，也建议先 `create_table` 建核心列，再用 `edit_table` 分批补列，降低超长请求被截断 / 超时的风险。
