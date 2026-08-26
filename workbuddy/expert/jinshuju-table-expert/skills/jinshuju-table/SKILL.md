---
name: jinshuju-table
slug: jinshuju-table
displayName: 金数据AI表格
description: "通过金数据（Jinshuju，jinshuju.net）MCP 操作用户托管在金数据平台上的数据表格：创建 / 编辑 / 移动数据表与列（含自动计算的公式列）；查询、新增（单条或批量）、更新、批量更新、删除行数据，或把本地上传的 Excel / CSV 批量导入数据表；用上传凭证把本地文件写入附件列；在服务端统计行数据（条数、分组、按天 / 周 / 月的趋势、整表列分布画像），跨表搜关键字；查询账户套餐额度与团队成员。仅在用户操作其金数据数据表时使用——触发信号：提到 金数据表格 / Jinshuju 表格 / 数据表，或要在金数据上建表、加改列、批量维护行数据。不要用于：用代码开发表格系统、把本地文件当普通文档分析（与导入到金数据数据表无关时）、搭建对外收集的表单 / 问卷、图片 / 票据 OCR，以及与金数据平台无关的通用数据处理。"
version: 1.2.0
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

数据表格与用于对外收集的「在线表单」是不同产品：数据表用 `create_table` / `edit_table` 建改；行数据（entries）两者共用同一批 entries 工具。本 skill 只处理数据表格。

## When to Use

本 skill **仅处理金数据数据表格（jinshuju.net）** 的表结构与行数据管理，且需满足以下任一**平台信号**才触发：

- 用户明确提到"金数据表格"、"Jinshuju 表格"、"数据表"
- 用户要在金数据上**建数据表、加/改列、移动表、增删改查或批量维护行数据**
- 用户上传了 Excel / CSV 并要把它**导入到金数据的某张数据表**
- 用户要查询本账户的套餐额度、团队成员

## When NOT to Use

以下场景**不要**用本 skill，直接退出、交给通用能力处理：

- 用代码 / 程序开发表格、数据库系统
- 纯本地处理文件、Excel / CSV、文档分析（**若目标是把这份表格导入到金数据某数据表，则属于本 skill**，用 `import_entries_from_file`）
- 搭建对外收集的**表单 / 问卷 / 报名表**（那是金数据表单产品，另有专家 / skill）
- 图片、账单、票据的 OCR / 识别
- 与金数据平台无关的通用数据处理

判断不属于金数据数据表操作时，**不要调用任何 MCP 工具**，按通用能力回答即可。

## Quick Reference

| 场景 | MCP 工具 |
|------|----------|
| 列出数据表 | `list_tables` |
| 查看数据表详情（列结构） | `get_table` |
| 创建数据表 | `create_table` |
| 改表名 / 增删改列 | `edit_table` |
| 列出文件夹（找表格文件夹 token） | `list_folders` |
| 新建文件夹 | `create_folder` |
| 移动数据表到文件夹 | `move_table` |
| 把本地上传的 Excel / CSV 导入数据表（后台任务） | `import_entries_from_file` |
| 列出行数据（可裁列 / 排序 / 关键字搜索） | `list_entries`（`form_token` 传表 token） |
| 只要行数，不拉数据 | `count_entries` |
| 服务端统计（求和 / 均值 / 分位 / 分组 / 按天周月趋势） | `aggregate_entries` |
| 整张表的数据画像（每列的分布 / 填充率） | `get_form_data_summary` |
| 在多张表 / 表单里搜同一个关键字（≤10 张） | `search_entries_in_forms` |
| 查看单行 | `get_entry` |
| 新建行（单条） | `create_entry` |
| 批量新建行（一次最多 200 行） | `create_entries` |
| 更新行（单条） | `update_entry` |
| 批量更新行（一次最多 200 行，PATCH） | `patch_entries` |
| 删除行（单条） | `delete_entry` |
| 上传文件写入附件列 | `prepare_entry_attachment_upload` |
| 当前用户信息 | `get_current_user` |
| 当前企业账户/套餐 | `get_current_billing_account` |
| 列出团队成员 | `list_account_users` |

## Procedure

### 原则

> ⚠️ **绝不绕过 MCP**：金数据 MCP 工具不可用（未连接 / 授权失败 / 调用持续报错）时**立即停止**，**禁止**改用浏览器自动化（Playwright 等）、直接调 GraphQL / REST API、curl 或模拟后台操作来替代。正确做法见下方「MCP 不可用时」。

1. **先看再动**：操作未知数据表前，先 `get_table` 拿列结构——每列的 `api_code`、选项列的 `choices[].api_code`。`create_entry` / `update_entry` 的键**必须是列 `api_code`**，传中文列名会被服务端丢弃。

2. **条件下推优先**：`list_entries` 的 `filters=[{field, operator, value}]` 把条件下推到数据库，比拉全量再本地筛选快几个数量级；不知道值在哪一列就用 `keyword` 一次搜整张表所有可搜列。只展示几列就传 `fields` 裁列，要排序就传 `sort=[{api_code, order}]` 交给服务端。单次上限 50 行，超过用 `next` 翻页（传了 `sort` 时 `next` 是行偏移量，否则是 serial_number 游标）。

3. **统计不拉全量**：问"多少行 / 合计多少 / 哪类最多 / 趋势怎么样"时**不要**翻页拉行数据回来自己算——只要行数用 `count_entries`；要具体数字、分组、按天 / 周 / 月趋势用 `aggregate_entries`（公式列也能聚合）；要整张表每列的分布 / 填充率用 `get_form_data_summary`。这三个工具的 `form_token` 同样填**表 token**，响应大小与行数无关。
   ⚠️ `get_table` **不返回**列的 `operators` / `analytics` 自描述（那是 `get_form` 才有的），所以函数与列类型是否匹配以报错为准——报错会列出该列支持的函数，照着改。

4. **先列再改**：批量操作前先 `list_entries` 拉出命中行展示给用户，**用户确认后**再执行——批量更新用 `patch_entries` 一次提交（≤200/批）；删除仍逐行循环 `delete_entry`，每 20 行汇报一次进度。

5. **永不主动开 PUT**：`update_entry` 默认 `is_put=false`（PATCH，只改提供的列）。`is_put=true` 会把未提供列全部清空，只有用户明确说"整行替换"且已列全所有列时才允许，且需二次确认。

6. **脱敏展示**：输出手机号/邮箱默认打码（`138****1234`），除非用户明确要求原文。

7. **不静默吞错**：列类型不支持、套餐限制、权限不足的报错原文回显并给出替代方案。

### 典型任务流

**① 新建数据表**
```
1. create_table，传 name + fields（列定义列表）
   - 列类型见「支持的列类型」；单选/多选列（RadioButton / CheckBox）传 choices
   - 需要跨列自动计算传 FormulaField（公式列）
   - 建完暂时没数据进：传 with_default_entries:true 补几行空行（空网格看着像坏了）；
     紧接着要 create_entries / 导入数据就别开，免得真实数据落在空行下面
   - 要放进文件夹：folder_token 只能是 kind="table" 的表格文件夹（先 list_folders 找）
2. 返回表结构与 token
```

**② 加 / 改列**
```
1. get_table → 记下现有列的 api_code
2. edit_table，用 fields 原子操作：
   - add: 新增列（同 create_table 的列定义）
   - remove: 传要删列的 api_code 数组（删有数据的列会永久清除该列数据，先确认）
   - update: 改列属性，带 api_code 保持 identity
   - update_choices: 增删改选项（改名用 update 保留 api_code）
```

**③ 条件查询 / 导出行**
```
1. get_table → 记下列 api_code 和选项 api_code
2. list_entries（form_token 传表 token）用 filters 下推条件（选项列传 api_code 不是 label）
3. next 翻页拿全部数据
4. Markdown 表格展示，表头用 get_table 的列 label，敏感列脱敏
5. 询问用户是否需要生成 CSV artifact
```

**④ 批量更新行**
```
1. get_table → 拿目标列 api_code + 目标选项 api_code
2. list_entries + filters 拉出命中集，展示前 10 行 + 总数
3. 用户确认后，用 patch_entries 一次提交（每行 { serial_number, entry }，PATCH 只改提供列，每批 ≤200 自行分批）
4. 读返回的 updated_count + failed_rows（按 serial_number），向用户汇总成功/失败
```

**⑤ 批量导入行**
```
1. get_table → 拿目标列 api_code + 选项 api_code
2. 把每行整理成 { api_code: value } 对象（选项传 api_code）
3. create_entries 一次提交（每批 ≤200，超过自行分批循环）
4. 读返回的 created_count + errors（按下标），向用户汇总成功/失败
   注意：不幂等，重复提交会产生重复行；失败后不要整批重发，按 errors 下标只补失败行
```

**⑥ 从本地上传的表格文件导入行**（用户在对话里上传了 Excel / CSV）
```
1. 先读文件（read_raw_content）看表头，get_table 拿目标列 api_code
2. 组好 column_mapping（每列 → field_api_code；表头唯一时用 column_label，
   有重名/空表头才用 sheet_column_index）；需要去重传 unique_field_code
3. import_entries_from_file 调用一次即返回——它是后台任务
4. 告诉用户"导入已开始，进度看数据页"，然后停手：
   别轮询、别重复调用、别自己再逐行写数据
   报错 = 一行都没导入（校验在起任务前完成）：读错误、改参数、只重试一次
   （仍是占位空行的空表会先清掉那些空行）
```

**⑦ 移动数据表到文件夹**
```
1. list_folders 找 kind="table" 的表格文件夹 token（表单文件夹放不了表格）
2. move_table，传 table_token + folder_token；省略 folder_token（或传空串）= 移回根目录
```

**⑧ 行数据统计 / 分析**
```
1. count_entries 先探范围（form_token 填表 token，带上要分析的 filters）
2. aggregate_entries 让服务端算：
   metrics=[{"func":"sum","field":"field_4"}]（1~20 个；公式列也能聚合）
   dimensions=[{"field":"field_status"}] 按 1~2 列分组（单选列、日期列可分组；多选列会被拒）
   日期列维度必须带 bucket:"day"/"week"/"month"
   结果按第一个指标降序，limit 默认 20 / 上限 200；看 row_count + truncated 判断是否只是一段
3. get_form_data_summary 一次拿整张表画像：每列的 buckets / stats + answered / null_count
4. 单选列维度的键返回 {api_code, label}，展示用 label；维度值 null = 该列没填的那一组
5. 只有用户要看具体行时才 list_entries，并用 fields 只取要展示的列
```

### 支持的列类型

| 列类型 | 说明 |
|--------|------|
| `TextArea` | 文本 |
| `NumberField` | 数字（显示精度用 `displayPrecision`，不可设存储 `precision`） |
| `DateTimeField` | 日期时间（`precision`：month / day / minute / second） |
| `BooleanField` | 布尔（勾选） |
| `MobileField` | 手机号 |
| `EmailField` | 邮箱 |
| `LinkField` | 链接 |
| `RadioButton` | 单选（传 `choices`） |
| `CheckBox` | 多选（传 `choices`） |
| `AttachmentField` | 附件（上传限制固定，不接受 max_file_quantity / max_size） |
| `FormulaField` | 公式列，自动计算（只读；`formula_display` 控制展示；不可设存储精度） |

### 关键格式规范

**entry payload 的键是列 `api_code`，不是中文列名：**

| 列类型 | 正确值格式 |
|----------|-----------|
| TextArea | 纯字符串 `"备注内容"` |
| MobileField | 纯字符串 `"13812345678"` |
| EmailField | 纯字符串 `"a@b.com"` |
| LinkField | 纯字符串 URL `"https://…"` |
| NumberField | 数字 `123` 或字符串 `"123"` |
| DateTimeField | ISO 字符串 `"2026-05-01 14:30"` |
| BooleanField | 布尔 `true` / `false` |
| RadioButton | 选项 api_code `"status_done"`（不是 label "已完成"） |
| CheckBox | api_code 数组 `["tag_a", "tag_b"]` |
| AttachmentField | 上传凭证返回的引用（先 `prepare_entry_attachment_upload`） |
| FormulaField | 只读，写入被忽略 |

**list_entries filters operator 速查：**

| operator | 适用列 | value 形式 |
|----------|----------|-----------|
| `eq` / `ne` | 所有 | 标量 |
| `gt` / `gte` / `lt` / `lte` | 数字、日期 | 标量 |
| `between` / `not_between` | 数字、日期 | `[min, max]` |
| `within_last` | 日期类（含 `created_at`） | `{"unit":"day"/"week"/"month","n":正整数}`，截至此刻往回数 |
| `any_in` / `none_in` | 文本、选项 | 数组 |
| `like` / `not_like` | 文本、选项 | 子串（**不带 % 通配符**） |
| `null` / `not_null` | 所有 | 省略 |

> 特殊字段：`created_at`（创建时间，配 `gte` / `between` / `within_last` 等）；`creator_id`（创建者用户 id，**只支持 `eq`**，value 是行返回的 `creator_id` 字符串）——按创建者查行用它，但聚合类工具不支持按它过滤。
>
> 列名写错会被**拒**并列出该表实际列，不会静默返回 0 行。排序传 `sort=[{api_code, order}]`（`asc` / `desc`），不必再在对话侧倒序。

## Pitfalls

- **entry 键写成中文列名** → 服务端静默丢弃，报 "Entry attributes cannot be empty"；键必须是列 `api_code`
- **选项列传 label**（如 `"已完成"`）→ 400 invalid choice；传 `choices[].api_code`
- **`is_put=true` 做部分更新** → 未提供列全部清空；部分更新永远保持默认 `is_put=false`
- **`like` 带 SQL 通配符**（`"张%"` / `"%张%"`）→ 按字面匹配 `%`，永远查不到；直接传 `"张"`
- **`operator` 与列类型不匹配** → 400，错误信息会列出该列可用 operator，照着改
- **简单列值包成对象**（`{"value": "abc"}`）→ 直接传字符串
- **批量新建行循环调 `create_entry`** → 改用 `create_entries` 一次提交（≤200 行/批）；它部分成功、按下标返回 `errors`、不幂等（重复调会生成重复行）
- **批量更新行循环调 `update_entry`** → 改用 `patch_entries`（一次 ≤200 行，每行 `{ serial_number, entry }`，PATCH 只改提供列，按 serial_number 返回 `failed_rows`）；`delete_entry` 仍无批量版，逐行循环
- **给附件列设上传限制**（`max_file_quantity` / `max_size`）→ 表格附件列限制固定，传了会被拒
- **给数字 / 公式列设 `precision`** → 表格数字 / 公式列不支持存储精度；显示格式用 `displayPrecision`
- **给非日期时间列传 `precision`** → `precision`（month/day/minute/second）仅 `DateTimeField` 可用
- **给 `RadioButton` / `CheckBox` 之外的列传 `choices`** → 仅这两类支持选项，其他列传 choices 无效
- **写入 `FormulaField`** → 公式列只读，写入被忽略；它的值由公式自动算
- **改选项文案用 remove + add** → 会换 api_code，历史数据引用失效；改名用 `fields.update_choices` 的 update（保留 api_code）
- **删列 / 删选项不先确认数据** → 删有数据的列 / 选项会永久清除数据且不可恢复；`fields.remove` / `update_choices.remove` 前先向用户说明影响、确认后再删
- **FormulaField 引用同一请求新增的列** → 新列还没有 api_code，公式里用 `<gd-field data-cid="...">` 引用其 `cid`，不要猜 api_code
- **把 table token 当 entry 定位符** → `get_entry` / `update_entry` / `delete_entry` 靠 **`serial_number`**（整数）定位单行，不是 token
- **给选项列设 `quota:0` 想表示"不限量"** → `0` 是"名额已满"，该选项会显示但置灰不可选；不限量就**省略 `quota`**，正整数才是名额上限
- **`create_table` 建空表不传 `with_default_entries`** → 空网格看着像坏了；暂时没数据进就传 `true` 补空行，紧接着要导数据就别开（免得真实数据落在空行下面）
- **把数据表移进表单文件夹** → 数据表只能进 `kind="table"` 的文件夹，先 `list_folders` 找；`move_table` 省略 `folder_token` 表示移回根目录
- **`import_entries_from_file` 后去轮询 / 重复调用 / 自己再逐行写数据** → 它是后台任务，调一次即返回；只需告诉用户"已开始、进度看数据页"然后停手。它报错 = 一行都没导入（校验在起任务前完成），读错误改参数、只重试一次
- **要统计却翻页拉全量行数据自己算** → 用 `count_entries` / `aggregate_entries` / `get_form_data_summary`，统计留在服务端（`form_token` 填表 token）
- **拿多选列当 `dimensions`** → 被拒（一行会落进多个组）；多选列的分布用 `get_form_data_summary`
- **日期列维度不传 `bucket`** → 每个存储值各成一组，出不来趋势；按 `day` / `week` / `month` 分桶
- **把分组结果当全量** → 分组按第一个指标降序、受 `limit` 截断（默认 20 / 上限 200）；看 `row_count` 和 `truncated`
- **给 `aggregate_entries` / `get_form_data_summary` 传 `keyword` 或按 `creator_id` 过滤** → 这两个工具没有 `keyword` 参数，`creator_id` 过滤会被拒
- **想从 `get_table` 里读列的可用聚合函数** → 它不返回 `analytics` / `operators`（那是 `get_form` 才有的）；用错函数看报错，报错会列出该列支持的函数
- **传了 `sort` 还把 `next` 当 serial_number 用** → 有 `sort` 时 `next` 是行偏移量；两种情况都把上一页的 `next` 原样回传
- **限流报错（HTTP 429 / code 14003）把原始 JSON 抛给用户** → 改为告知"接口请求频繁，请等 1–2 分钟后重试"，放慢节奏、合并可批量的请求；不要立刻疯狂重试

## Verification

操作完成后确认：
- **创建/编辑数据表**：返回中包含有效表 token 与预期的列结构（列 `api_code`、类型）
- **move_table**：`get_table` / `list_tables` 显示表已在目标文件夹（或已回到根目录）
- **import_entries_from_file**：调用成功即代表任务已入队；不在本轮核对行数，让用户去数据页看进度
- **create_entry**：返回包含 `serial_number`（整数）
- **create_entries**：返回 `created_count` 与提交行数一致，`errors` 为空（有部分失败时按下标核对原因）
- **update_entry**：返回的列值与提交值一致
- **patch_entries**：返回 `updated_count` 与提交行数一致，`failed_rows` 为空（有部分失败时按 serial_number 核对 reason）
- **delete_entry**：后续 `get_entry` 返回 404 或该行不再出现在 `list_entries`
- **aggregate_entries**：`columns` 与传入的 metrics / dimensions 顺序一一对应，分组时核对 `row_count` 与 `truncated` 再下结论
- **get_form_data_summary**：`overview.total_entries` 与同 filters 下的 `count_entries` 一致
- **批量操作**：向用户汇报"共 N 行，成功 X 行，失败 Y 行"

## MCP 配置

金数据 MCP 端点：`https://jinshuju.net/mcp`（表单与表格共用同一端点）

**方式 A · HTTP Basic（API Key/Secret）**
```bash
echo -n "YOUR_API_KEY:YOUR_API_SECRET" | base64
```
```json
{
  "mcpServers": {
    "jinshuju-table": {
      "url": "https://jinshuju.net/mcp",
      "headers": { "Authorization": "Basic <BASE64>" }
    }
  }
}
```

**方式 B · OAuth 2.0**
```json
{
  "mcpServers": {
    "jinshuju-table": { "url": "https://jinshuju.net/mcp" }
  }
}
```

常见配置错误：漏 `/mcp` 后缀、用 `http://`、`Authorization` 缺 `Basic ` 前缀、用 `command/args`（stdio 写法，金数据是远程 HTTP MCP 不支持）。

### MCP 不可用时

工具未连接 / 授权失败 / 持续报错时，按顺序降级，**不要**用任何非标方式替代：

1. 告知用户"金数据 MCP 未就绪"，不要假装已完成操作。
2. 对照上面的「常见配置错误」引导排查（端点、`Basic ` 前缀、OAuth 授权等）。
3. 仍不行，就给出在金数据后台（jinshuju.net）手动操作的步骤指引。

> 超宽表（几十列）即使 MCP 正常，也建议先 `create_table` 建核心列，再用 `edit_table` 分批补列，降低超长请求被截断 / 超时的风险。
