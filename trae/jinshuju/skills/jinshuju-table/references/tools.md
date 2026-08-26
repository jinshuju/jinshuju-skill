# 金数据表格 MCP 工具参考

金数据表格 MCP 端点：`https://jinshuju.net/mcp`（与表单共用端点）。表格工具对所有账号开放，不再需要单独开通「新版表格」。以下按 `数据表结构` → `行数据 Entries` → `统计分析` → `上传` → `账户与团队` 分组。

> 通用约定：
> - 表结构工具用**表 token / id** 定位；行数据工具的 `form_token` 参数直接填**表 token**。
> - 行数据读写一律用**列 `api_code`**，选项列用 `choices[].api_code`，不是中文列名 / label。
> - 分页统一走响应里的 `next` 游标；`limit` 越界自动截断。
> - 报 `Insufficient scope: <name> required` 说明缺对应 OAuth scope，提示用户重新授权勾选。

---

## 一、数据表结构（scope: forms）

### list_tables — 列出数据表

列出当前用户可访问的数据表，支持关键字过滤与游标分页。

**输入**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 否 | 表名关键字过滤（不区分大小写） |
| `next` | string | 否 | 翻页游标 |
| `limit` | integer | 否 | 每页条数，默认 / 上限 50 |

**输出**：`{ total, count, data: [表摘要…], next }`。用 `next` 翻下一页；`next` 为空表示到底。

### get_table — 查看数据表详情

取一张数据表的完整结构：列（`api_code`、类型、label、选项 `choices[].api_code`）等。

**输入**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `token` | string | 是 | 表 token 或 id |

**输出**：数据表序列化结构。写 / 改 / 过滤行数据前，先用它拿列 `api_code`。若目标资源不是数据表（是普通表单），会报 `Resource is not a table`。

### create_table — 创建数据表

**输入**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 表名 |
| `fields` | array | 是 | 列定义数组（见下）|
| `folder_token` | string | 否 | 放入指定文件夹 |

**列定义（`fields[]` item）**

| 键 | 类型 | 说明 |
|----|------|------|
| `type` | string | 列类型，见「支持的列类型」；必填 |
| `label` | string | 列名；必填 |
| `cid` | string | 客户端临时 id，用于同一请求内被公式列引用（`<gd-field data-cid="…">`）|
| `choices` | array | 仅 `RadioButton` / `CheckBox`：`[{ value: "选项文字" }]` |
| `precision` | integer/string | 仅 `DateTimeField`：month / day / minute / second |
| `formula_display` | string | 仅 `FormulaField`：公式结果展示方式 |
| 数字格式相关 | — | 数字/公式列的显示格式（如 `displayPrecision`）；不可设存储 `precision` |

**支持的列类型**：`TextArea` `RadioButton` `CheckBox` `BooleanField` `MobileField` `NumberField` `DateTimeField` `EmailField` `LinkField` `AttachmentField` `FormulaField`。

**输出**：新表序列化结构（含各列 `api_code`）。常见报错：`Field type not supported for tables`（列类型不在白名单）、`Attachment upload limits are fixed for table columns`（附件列传了上传限制）、`Storage precision is not supported…`（数字/公式列传了 `precision`）。

### edit_table — 编辑数据表（改名 + 增删改列，原子）

一次请求内对列做增 / 删 / 改 / 选项操作，原子生效。

**输入**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `table_token` | string | 是 | 表 token 或 id |
| `name` | string | 否 | 新表名 |
| `fields` | object | 否 | 列级操作，见下 |

**`fields` 操作**

| 键 | 说明 |
|----|------|
| `add` | 新增列数组，item 同 create_table 的列定义 |
| `remove` | 要删列的 `api_code` 字符串数组（删有数据的列会永久清除该列数据）|
| `update` | 改列属性数组，每项**必须带 `api_code`** 保持 identity（可改 `label`、`precision`、`formula_display`、数字格式）|
| `update_choices` | 选项增删改；改名用 update 保留 `api_code`，避免历史数据引用失效 |

**输出**：更新后的数据表结构。约束报错同 create_table；非数据表会报 `Resource is not a table`。

---

## 二、行数据 Entries（scope: read_entries / write_entries）

数据表的行与表单数据共用同一批 entries 工具，`form_token` 参数填**表 token**。行用 `serial_number`（整数）定位。

### list_entries — 列出行

**输入**：`form_token`(表 token) ✅、`filters`（`[{field, operator, value}]` 下推过滤，多条件 AND）、`keyword`（一次搜整张表所有可搜列，≤200 字符）、`fields`（只返回这些列的 `api_code`，宽表必传）、`sort`（`[{api_code, order}]`，`order` 取 `asc` / `desc`）、`next`（游标）、`limit`（≤50）。
**输出**：`{ total, count, data: [行…], next }`。列值键是列 `api_code`；`serial_number` / `token` 恒返回。

- 排序交给 `sort`，**不要**拉回来再本地排；列名写错（`fields` / `sort` / `filters` 任一处）会被拒并列出该表实际列，不会静默丢列或回落默认排序
- ⚠️ 传了 `sort` 时 `next` 是**行偏移量**，不传时是 `serial_number` 游标——两种都把上一页的 `next` 原样回传
- 聚合 / group by 不在这里做，用下面的「统计分析」三件套

**filters operator 速查**

| operator | 适用列 | value |
|----------|--------|-------|
| `eq` / `ne` | 所有 | 标量 |
| `gt` / `gte` / `lt` / `lte` | 数字、日期 | 标量 |
| `between` / `not_between` | 数字、日期 | `[min, max]` |
| `within_last` | 日期类（含 `created_at`） | `{"unit":"day"/"week"/"month","n":正整数}` |
| `any_in` / `none_in` | 文本、选项 | 数组 |
| `like` / `not_like` | 文本、选项 | 子串（**不带 %**）|
| `null` / `not_null` | 所有 | 省略 |

> 特殊字段：`created_at`（创建时间）；`creator_id`（创建者 id，只支持 `eq`）。

### get_entry — 查看单行

**输入**：`form_token`(表 token) ✅、`entry_id`(serial_number) ✅。**输出**：单行完整详情。

### create_entry — 新建单行

**输入**：`form_token`(表 token) ✅、`entry`（`{列 api_code: 值}`）✅。**输出**：含 `serial_number`。值格式见 SKILL.md「关键格式规范」。

### create_entries — 批量新建行

**输入**：`form_token`(表 token) ✅、`entries`（`[{列 api_code: 值}, …]`，一次 ≤200）✅。
**输出**：`{ created_count, errors: [{index, message}] }`。不幂等，重复提交产生重复行；失败按 `errors` 下标只补失败行。

### update_entry — 更新单行

**输入**：`form_token`(表 token) ✅、`entry_id`(serial_number) ✅、`entry`（要改的列）、`is_put`（默认 `false`=PATCH）。
> ⚠️ `is_put=true` 会清空未提供列，仅"整行替换"时用且需二次确认。

### patch_entries — 批量更新行（PATCH）

**输入**：`form_token`(表 token) ✅、`entries`（`[{ serial_number, entry }, …]`，一次 ≤200）。
**输出**：`{ updated_count, failed_rows: [{serial_number, reason}] }`。PATCH 只改提供列。

### delete_entry — 删除单行

**输入**：`form_token`(表 token) ✅、`entry_id`(serial_number) ✅。无批量版，逐行循环；不可逆，先确认。

---

## 三、统计分析（scope: read_entries）

这三个工具把统计留在服务端，响应大小与行数无关；`form_token` 同样填**表 token**。要"多少行 / 合计多少 / 哪类最多 / 趋势怎么样"时用它们，别翻页拉全量回来自己算。

### count_entries — 只数行数

**输入**：`form_token`(表 token) ✅、`filters`、`keyword`。**输出**：`{ total }`。要分析或翻页前先用它探范围。

### aggregate_entries — 服务端统计（可分组）

**输入**：`form_token`(表 token) ✅、`metrics`（1~20 个 `{ func, field }`）✅、`dimensions`（1~2 个 `{ field, bucket? }`）、`limit`（分组数，默认 20 / 上限 200）、`filters`。

- `func`：`count` / `count_non_empty` / `count_empty` / `count_unique` / `sum` / `avg` / `min` / `max` / `stddev` / `median` / `p25` / `p75` / `p90`，**按列类型受限**——函数与列不匹配会报错并列出该列支持的函数（`get_table` 不返回这份自描述，以报错为准）。公式列也能聚合
- `dimensions`：单选列、日期列可分组；**多选列会被拒**（一行会落进多个组），它的分布用 `get_form_data_summary`。日期列**必须**带 `bucket`（`day` / `week` / `month`，按 `Asia/Shanghai`、周一为一周起点）
- **输出**：`{ columns, rows, total, tz }`；分组时还有 `row_count`（分组总数）和 `truncated`（是否只是按 `limit` 截断的一段）。单选列维度的键是 `{ api_code, label }`，维度值为 `null` 的那组 = 该列没填的行

```json
{ "form_token": "<表 token>",
  "metrics": [{ "func": "sum", "field": "field_4" }, { "func": "avg", "field": "field_2" }],
  "dimensions": [{ "field": "created_at", "bucket": "day" }] }
```

### get_form_data_summary — 整张表数据画像

**输入**：`form_token`(表 token) ✅、`fields`（要画像的列，默认全部可分析列 + `created_at`，上限 60）、`include_overview`（默认 `true`）、`filters`。

**输出**：`overview`（`total_entries` / `today_entries`）+ 每列一项：`kind` 为 `choice` 时给 `buckets`（`api_code` / `label` / `count` / `ratio`），`number` 给 `stats`（`min` / `max` / `sum` / `avg`），`date` 给 `earliest` / `latest`，`text` 给 `count_unique`；每列都有 `answered` 与 `null_count`。

> `aggregate_entries` / `get_form_data_summary` **没有** `keyword` 参数，也不支持按 `creator_id` 过滤（会被拒）。

### search_entries_in_forms — 跨表 / 跨表单搜关键字

**输入**：`form_tokens`（≤10 个表 / 表单 token）✅、`keyword` ✅。
**输出**：`{ total, forms: [{ form_token, name, matched, serial_numbers }] }`——`total` 是命中**行总数**，`serial_numbers` 每张最多列 50 个；没命中的表直接不出现；带 `unavailable` 的表是**没搜成**（无权限 / 超 99999 行无 ClickHouse / 服务未响应），必须单独重试，**不能**当成"没命中"。不接受 `filters`（同一 `api_code` 在不同表指向不同列）。

---

## 四、上传（scope: write_entries）

### prepare_entry_attachment_upload — 附件列上传凭证

为附件列（`AttachmentField`）换取上传凭证，上传本地文件后把返回引用写入该列。

---

## 五、账户与团队

| 工具 | scope | 用途 |
|------|-------|------|
| `get_current_user` | `user` | 当前用户信息 |
| `get_current_billing_account` | `billing_account` | 企业套餐与用量 |
| `list_account_users` | `billing_account` | 团队成员列表 |
