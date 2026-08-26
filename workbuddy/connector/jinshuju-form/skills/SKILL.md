---
name: jinshuju-form-skill
description: 金数据（Jinshuju，jinshuju.net）表单操作技能 —— 创建/复制/编辑表单与主题，增删改查与批量修改表单数据，把本地上传的 Excel/CSV 导入表单，建视图筛选与对外查询页，在服务端统计数据（条数/分组/趋势/分布画像）与跨表单搜关键字，上传图片附件，查询账户套餐与团队成员。触发词：金数据、Jinshuju、jinshuju.net、form_token、表单、报名表、问卷、数据录入、数据查询、批量修改、数据导入、数据统计、数据分析、跨表单搜索。
version: "1.0.0"
author: "Jinshuju"
---

# 金数据表单 Skill（Jinshuju Forms）

本 Skill 指导 AI 通过金数据 MCP Server 操作用户托管在 **jinshuju.net** 上的在线表单与数据。所有工具由 MCP 提供，用户完成 OAuth 授权后即可调用。

## 何时使用

满足任一**平台信号**才触发：用户提到「金数据 / Jinshuju / jinshuju.net」、给出 `form_token`、或要操作一张已托管在金数据上的表单或数据（建表、改字段、改主题、增删改查 entries、导出、批量修改）、查询本账户套餐与团队成员。

**不要**用于：用代码开发表单/问卷系统、处理本地 Excel/CSV、图片票据 OCR、与金数据平台无关的通用数据处理。此时不调用任何 MCP 工具。

## 核心概念

- **form_token**：表单唯一标识，出现在表单地址 `https://jinshuju.net/f/<form_token>` 中，几乎所有表单级工具都要它。
- **字段 API 名**：每个字段有稳定的机器名（如 `field_1`、`field_2`），写入/更新数据、下推过滤时用字段 API 名而非中文标题。先 `get_form` 拿字段结构。
- **OAuth scope**：`forms` / `form_setting` / `read_entries` / `write_entries` / `user` / `billing_account`。未授权 scope 调用会报 `Insufficient scope: <name> required`，需提示用户在授权时勾选对应权限。

## 可用工具

### 表单管理（scope: forms / form_setting）

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `list_forms` | 列出可访问的表单 | `name`(正则关键字,可选)、`next`、`limit` |
| `list_folders` | 列出文件夹，取 `folder_token` | — |
| `create_folder` | 新建文件夹 | `name` ✅、`kind`(form/table) |
| `get_form` | 取表单完整结构（字段、API 名、类型） | `form_token` ✅ |
| `check_field_data` | 写数据前预检字段值是否合法 | `form_token` ✅、`fields` |
| `create_form` | 新建表单 | `name` ✅、`fields` ✅、`folder_token`(可选) |
| `copy_form` | 复制已有表单 | `form_token` ✅ |
| `move_form` | 移动表单到文件夹 | `form_token` ✅、`folder_token` |
| `edit_form` | 编辑表单字段/设置 | `form_token` ✅ |
| `edit_theme` | 调整表单主题外观 | `form_token` ✅ |

### 考试 / 测评表单（scope: forms）

| 工具 | 用途 |
|------|------|
| `create_exam_form` / `edit_exam_form` | 创建/编辑自动判分的考试表单 |
| `create_evaluation_form` / `edit_evaluation_form` | 创建/编辑选项计分的测评表单 |

### 数据管理 Entries（scope: read_entries / write_entries）

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `list_entries` | 按条件查询数据，支持下推过滤、关键字搜索、裁列、排序 | `form_token` ✅、`filters`、`keyword`、`fields`、`sort`、`next`、`limit` |
| `get_entry` | 取单条数据详情 | `form_token` ✅、`entry_id` ✅ |
| `create_entry` | 新增单条数据 | `form_token` ✅、`entry`(字段 API 名→值) ✅ |
| `create_entries` | 批量新增（导入）数据 | `form_token` ✅、`entries`[] ✅ |
| `update_entry` | 更新单条数据 | `form_token` ✅、`entry_id` ✅、`entry` |
| `delete_entry` | 删除单条数据 | `form_token` ✅、`entry_id` ✅ |
| `import_entries_from_file` | 把本地上传的 Excel/CSV 导入表单（后台任务，调一次即返回，别轮询） | `form_token` ✅、`attachment_id` ✅、`column_mapping` ✅ |

### 统计分析与搜索（scope: read_entries）

统计一律留在服务端，**不要**翻页拉全量明细回来自己算。

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| `count_entries` | 只数条数，不返回数据 | `form_token` ✅、`filters`、`keyword` |
| `aggregate_entries` | 整列统计，可按 1~2 个字段分组、日期按天/周/月分桶 | `form_token` ✅、`metrics`(1~20 个 `{func, field}`) ✅、`dimensions`、`limit`(默认 20/上限 200)、`filters` |
| `get_form_data_summary` | 整张表单画像：每个字段的分布 / 数值统计 / 填答率 | `form_token` ✅、`fields`、`include_overview`、`filters` |
| `search_entries_in_forms` | 一次在 ≤10 张表单里搜同一关键字，返回命中数与流水号 | `form_tokens` ✅、`keyword` ✅ |

可用聚合函数与可分组字段由字段类型决定，读 `get_form` 返回的 `analytics.agg_funcs` / `analytics.groupable`（过滤 operator 读 `operators`），别猜。

### 视图与对外查询（scope: forms / read_entries）

| 工具 | 用途 |
|------|------|
| `list_form_views` / `get_form_view` | 列出 / 查看表单视图 |
| `create_form_view` / `edit_form_view` / `delete_form_view` | 建 / 改 / 删视图（grid 表格、kanban 看板、stats 统计；预设视图与最后一个视图不可删） |
| `list_form_view_entries` | 按视图的筛选 / 排序 / 列偏好列出数据 |
| `list_opensearch_queries` / `get_opensearch_query` | 列出 / 查看对外查询页 |
| `create_opensearch_query` / `edit_opensearch_query` | 建 / 改对外查询页（访客自助查数据；仅表单管理员可操作） |

### 上传（scope: forms / write_entries）

| 工具 | 用途 |
|------|------|
| `prepare_form_image_upload` | 换取表单头图 / 选项图上传凭证 |
| `prepare_entry_attachment_upload` | 换取 entry 附件字段上传凭证 |

### 账户与团队

| 工具 | 用途 | scope |
|------|------|-------|
| `get_current_user` | 当前用户信息 | `user` |
| `get_current_billing_account` | 企业套餐与用量 | `billing_account` |
| `list_account_users` | 团队成员列表 | `billing_account` |
| `list_my_submitted_forms` / `list_my_submitted_entries` | 我作为填写者提交过的表单/数据 | `forms` / `read_entries` |

## 典型工作流

1. **建表**：`create_form`（先想清字段类型；不确定值是否合法可先 `check_field_data`）→ 返回 `form_token` 与 `form_url`。
2. **查数据**：`list_forms` 找到 `form_token` →（可选 `get_form` 确认字段 API 名）→ `list_entries` 带 `filter` 下推过滤。
3. **写/改数据**：`get_form` 拿字段 API 名 → `create_entry` / `create_entries` / `update_entry`，值按字段 API 名组织。
4. **带附件/图片**：先 `prepare_*_upload` 换凭证上传，再把返回的引用写入对应字段。

## 注意事项

- 写入/更新/过滤数据一律用**字段 API 名**（`field_1`…），不要用中文标题猜。拿不准就先 `get_form`。
- 分页统一走响应里的 `next` 游标；`limit` 越界会自动截断。
- 批量修改/删除不可逆，执行前向用户复述影响范围并确认。
- 报 `Insufficient scope` 时，说明缺哪个 scope，提示用户重新授权勾选对应权限。
- `import_entries_from_file` 是后台任务：调一次即返回，告知用户"已开始、进度看数据页"后停手，别轮询或自己再逐行写；它报错 = 一行都没导入，改参数只重试一次。
- 要"多少 / 多少钱 / 最多的是哪个 / 趋势"用 `count_entries` / `aggregate_entries` / `get_form_data_summary`；只有要看具体记录时才 `list_entries`，并用 `fields` 裁列、`sort` 排序。
- `aggregate_entries` / `get_form_data_summary` 没有 `keyword` 参数，也不支持按 `creator_id` 过滤；多值字段（多选/级联/矩阵/地址/表格）不能当分组维度，它们的分布用 `get_form_data_summary`。
- `search_entries_in_forms` 里带 `unavailable` 的表单是**没搜成**（无权限 / 超 99999 条无 ClickHouse / 服务未响应），必须单独重试，**不能**汇报成"没命中"；响应里完全没出现的 token 才是"搜过没命中"。
- 选项的 `quota` 省略 = 不限量，正整数 = 名额上限；**勿传 `0`**（0 = 名额已满、选项置灰不可选）。
