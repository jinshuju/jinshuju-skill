---
name: jinshuju-table-skill
description: 金数据表格（Jinshuju Tables，jinshuju.net）操作技能 —— 创建/编辑/移动数据表与列（含自动计算的公式列），批量增删改查行数据，把本地上传的 Excel/CSV 导入数据表，在服务端统计行数据（条数/分组/趋势/列分布画像）与跨表搜关键字，查询账户套餐与团队成员。触发词：金数据表格、Jinshuju Table、数据表、建表、加一列、行数据、批量修改、数据统计、数据分析。
version: "1.0.0"
author: "Jinshuju"
---

# 金数据表格 Skill（Jinshuju Tables）

本 Skill 指导 AI 通过金数据 MCP Server 操作用户托管在 **jinshuju.net** 上的**数据表格**（表格是一种以「列 + 行」组织的结构化数据表，区别于收集用的在线表单）。所有工具由 MCP 提供，用户完成 OAuth 授权后即可调用。

## 何时使用

满足任一**平台信号**才触发：用户提到「金数据表格 / Jinshuju 表格 / 数据表」、要在金数据上**建数据表、加/改列、批量维护行数据**、要统计某张表的数据、或查询本账户套餐与团队成员。

**不要**用于：用代码开发表格系统、纯本地处理 Excel/CSV（**若目标是导入到金数据某张表，则属于本 skill**）、图片票据 OCR、与金数据平台无关的通用数据处理。此时不调用任何 MCP 工具。

## 核心概念

- **table token / id**：数据表唯一标识，`get_table` / `edit_table` 等表级工具都要它。
- **列 api_code**：每列有稳定机器名（如 `field_1`），写入/更新/过滤行数据时用列 api_code，而非中文列名。先 `get_table` 拿列结构。
- **表 ≠ 表单**：数据表用 `create_table` / `edit_table` 建改；在线收集表单是另一个产品，用 form 那套工具。行数据（entries）与统计工具两者共用，`form_token` 参数直接填**表 token**。
- **OAuth scope**：表格结构工具走 `forms` scope；行数据与统计走 `read_entries` / `write_entries`；账户信息走 `user` / `billing_account`。未授权会报 `Insufficient scope: <name> required`，需提示用户重新授权勾选。

## 可用工具

### 数据表结构（scope: forms）

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `list_tables` | 列出可访问的数据表 | `name`(关键字,可选)、`next`、`limit`(≤50) |
| `get_table` | 取数据表完整结构（列、api_code、类型） | `token` ✅ |
| `create_table` | 新建数据表 | `name` ✅、`fields` ✅、`folder_token`(可选)、`with_default_entries` |
| `edit_table` | 改表名 / 增删改列（原子操作） | `table_token` ✅、`name`、`fields.{add,remove,update,update_choices}` |
| `move_table` | 把表移进/移出文件夹 | `table_token` ✅、`folder_token`(省略=移回根目录) |
| `list_folders` / `create_folder` | 找 / 建文件夹 | `create_folder`：`name` ✅、`kind`(form/table) |

**支持的列类型**：`TextArea` `RadioButton` `CheckBox` `BooleanField` `MobileField` `NumberField` `DateTimeField` `EmailField` `LinkField` `AttachmentField` `FormulaField`。仅 `RadioButton` / `CheckBox` 支持 `choices`。

### 行数据 Entries（scope: read_entries / write_entries）

数据表的行（记录）与表单数据共用同一批工具，用**表 token** 定位。

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `list_entries` | 按条件查询行，支持下推过滤、关键字搜索、裁列、排序 | `form_token`(填表 token) ✅、`filters`、`keyword`、`fields`、`sort`、`next`、`limit`(≤50) |
| `get_entry` | 取单行详情 | `form_token` ✅、`entry_id`(serial_number) ✅、`fields` |
| `create_entry` | 新增单行 | `form_token` ✅、`entry`(列 api_code→值) ✅ |
| `create_entries` | 批量新增行（一次 ≤200） | `form_token` ✅、`entries`[] ✅ |
| `update_entry` | 更新单行（默认 PATCH） | `form_token` ✅、`entry_id` ✅、`entry` |
| `patch_entries` | 批量更新行（一次 ≤200） | `form_token` ✅、每行 `{serial_number, entry}` |
| `delete_entry` | 删除单行 | `form_token` ✅、`entry_id` ✅ |
| `import_entries_from_file` | 把用户上传的 Excel/CSV 导入数据表（后台任务，调一次即返回，别轮询） | `form_token` ✅、`attachment_id` ✅、`column_mapping` ✅ |

### 统计分析（scope: read_entries）

统计留在服务端，响应大小与行数无关。**不要**翻页拉全量行数据回对话侧自己算。

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `count_entries` | 只数行数，不返回数据 | `form_token` ✅、`filters`、`keyword` |
| `aggregate_entries` | 整列统计，可按 1~2 列分组、日期按天/周/月分桶 | `form_token` ✅、`metrics`(1~20 个 `{func, field}`) ✅、`dimensions`、`limit`(默认 20/上限 200)、`filters` |
| `get_form_data_summary` | 整张表画像：每列的分布 / 数值统计 / 填充率 | `form_token` ✅、`fields`、`include_overview`、`filters` |
| `search_entries_in_forms` | 一次在 ≤10 张表/表单里搜同一关键字 | `form_tokens` ✅、`keyword` ✅ |

公式列也能聚合。单选列、日期列可做分组维度，多选列会被拒（它的分布用 `get_form_data_summary`）；日期维度必须带 `bucket`（`day`/`week`/`month`）。⚠️ `get_table` **不返回**列的 `analytics` / `operators` 自描述（那是表单的 `get_form` 才有），函数与列类型是否匹配以报错为准——报错会列出该列支持的函数。

### 上传（scope: write_entries）

| 工具 | 用途 |
|------|------|
| `prepare_entry_attachment_upload` | 换取附件列（AttachmentField）上传凭证 |

### 账户与团队

| 工具 | 用途 | scope |
|------|------|-------|
| `get_current_user` | 当前用户信息 | `user` |
| `get_current_billing_account` | 企业套餐与用量 | `billing_account` |
| `list_account_users` | 团队成员列表 | `billing_account` |

## 典型工作流

1. **建表**：`create_table`（列类型见上表；`RadioButton`/`CheckBox` 传 `choices`）→ 返回表 token 与结构。暂时没数据要进就传 `with_default_entries:true` 补几行空行；紧接着要导数据就别开。
2. **加/改列**：`get_table` 拿现有列 api_code → `edit_table` 用 `fields.add` / `fields.remove`(传 api_code) / `fields.update` 原子改动。
3. **查行**：`list_entries` 带 `filters` 把列值条件下推到数据库（选项列用 `choices[].api_code`）；不知道值在哪一列用 `keyword`；只看几列传 `fields`，要排序传 `sort`。
4. **统计**：先 `count_entries` 探范围 → `aggregate_entries` 做分组 / 分桶统计 → 要整表全貌用 `get_form_data_summary`。只有用户要看具体行时才 `list_entries`。
5. **写/改行**：`get_table` 拿列 api_code → `create_entry` / `create_entries` / `update_entry` / `patch_entries`，值按列 api_code 组织。
6. **带附件**：先 `prepare_entry_attachment_upload` 换凭证上传，再把引用写入附件列。

## 注意事项

- 写入/更新/过滤行数据一律用**列 api_code**（`field_1`…），不要用中文列名猜。拿不准就先 `get_table`。
- 列约束：附件列上传限制固定（不接受 `max_file_quantity`/`max_size`）；数字/公式列存储精度不可设，用 `displayPrecision` 控制显示；`precision` 仅日期时间列可用；公式列只读，写入被忽略。
- 改选项文案用 `update_choices.update`（保留 api_code）；用 remove+add 会换 api_code，历史数据引用失效。选项的 `quota` 省略 = 不限量，正整数 = 名额上限，**勿传 `0`**（0 = 名额已满、置灰不可选）。
- 分页统一走响应里的 `next` 游标；`limit` 越界会自动截断（≤50）。⚠️ 传了 `sort` 时 `next` 是行偏移量，不传时是 `serial_number` 游标，两种都把上一页的 `next` 原样回传。
- 移动数据表只能进 `kind="table"` 的文件夹（先 `list_folders` 找），表单文件夹放不了表格。
- `import_entries_from_file` 是后台任务：调一次即返回，告知用户"已开始、进度看数据页"后停手，别轮询或自己再逐行写；它报错 = 一行都没导入，改参数只重试一次。
- 批量更新用 `patch_entries`，删除仍逐行 `delete_entry`；均不可逆，执行前向用户复述影响范围并确认。
- 套餐 / 额度类失败以工具错误返回（不是 500），把原文告诉用户并给替代方案，不要反复重试。
