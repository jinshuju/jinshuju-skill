---
name: jinshuju-skill
description: 金数据（Jinshuju，jinshuju.net）操作技能 —— 创建/复制/编辑/删除表单与主题，建考试与测评，建改多维表格，增删改查与批量修改数据、写数据评论，把本地 Excel/CSV 导入表单，建视图筛选与对外查询页，在服务端统计数据（条数/分组/趋势/分布画像）与跨表单搜关键字，上传图片附件，查询账户套餐、团队成员与收款商户。触发词：金数据、Jinshuju、jinshuju.net、form_token、表单、报名表、问卷、数据录入、数据查询、批量修改、数据导入、数据统计、数据分析、跨表单搜索。
version: "2.0.0"
author: "Jinshuju"
---

# 金数据 Skill（Jinshuju）

本 Skill 指导 AI 通过金数据 MCP Server 操作用户托管在 **jinshuju.net** 上的在线表单、表格与数据。所有工具由 MCP 提供，用户完成 OAuth 授权后即可调用。

## 何时使用

满足任一**平台信号**才触发：用户提到「金数据 / Jinshuju / jinshuju.net」、给出 `form_token`、或要操作一张已托管在金数据上的表单、表格或数据（建表、改字段、改主题、增删改查 entries、导出、批量修改）、查询本账户套餐与团队成员。

**不要**用于：用代码开发表单/问卷系统、处理与导入金数据无关的本地 Excel/CSV、图片票据 OCR、与金数据平台无关的通用数据处理。此时不调用任何 MCP 工具。

## 参数以 MCP 为准

金数据 MCP 的工具由开放 API v1 的 openapi.yaml 自动生成，随 API 同步更新。**参数、取值、返回结构以工具自带的描述为准**，本 Skill 只讲场景和顺序。

- 参数描述写着 `Shape: schema "X"` 的，调 `get_schema("X")` 读结构，不要猜
- 建表单：先 `get_schema("FieldInput")`，它的 `x-variants` 把字段类型映射到各自的 schema（如 `RadioButton → RadioButtonInput`），再 `get_schema` 看该类型的属性
- 报错会给出 HTTP 状态和服务端的 `error_description` / `errors`，通常列出了可用的字段 / operator / 取值，照着改再试

## 核心概念

- **form_token**：表单唯一标识，`list_forms` 返回的 `token`。表格用 `table_token`；表格的行数据仍用数据工具，`form_token` 传表 token。
- **字段 api_code**：每个字段的机器名（如 `field_1`），写入 / 更新 / 过滤数据都用它，不用中文标题。先 `get_form` 拿字段结构。选项值传选项 api_code 或选项文字都行。
- **serial_number**：单条数据的整数流水号，`get_entry` / `update_entry` / `delete_entry` 用它定位。
- **OAuth scope**：`forms` / `form_setting` / `read_entries` / `write_entries` / `user` / `billing_account`。缺 scope 时会报错说明需要哪个，提示用户重新授权并勾选。

## 可用工具

| 类别 | 工具 |
|------|------|
| 表单 | `list_forms`（`q` 按名称搜）、`get_form`、`create_form`、`edit_form`、`copy_form`、`delete_form`（进回收站）、`move_form`、`list_form_cooperators`、`edit_theme` |
| 字段 | `check_field_data`（删字段 / 选项前查有没有数据）、`preview_field_type_change`（改类型前预览数据损失）、`get_field_rules` / `edit_field_rules`（显示规则） |
| 考试 / 测评 | `create_exam_form` / `edit_exam_form`、`create_evaluation_form` / `edit_evaluation_form` |
| 数据 | `list_entries`、`get_entry`、`create_entry`、`update_entry`、`delete_entry`、`create_entries`（≤200）、`patch_entries`（≤200，不能写附件）、`import_entries_from_file` |
| 统计 / 搜索 | `count_entries`、`aggregate_entries`、`get_form_data_summary`、`list_form_entry_stats`、`search_entries_in_forms` |
| 我提交的 | `list_my_submitted_forms`、`list_my_submitted_entries`、`search_my_submitted_entries` |
| 数据评论 | `list_entry_comments`、`create_entry_comment`、`update_entry_comment`、`delete_entry_comment` |
| 视图 | `list_form_views`、`get_form_view`、`create_form_view`、`edit_form_view`、`delete_form_view`、`list_form_view_entries` |
| 表格 | `list_tables`、`get_table`、`create_table`、`edit_table`、`move_table` |
| 对外查询页 | `get_opensearch_field_suggestions`、`list_opensearch_queries`、`get_opensearch_query`、`create_opensearch_query`、`edit_opensearch_query` |
| 文件夹 / 账户 | `list_folders`、`create_folder`、`get_current_user`、`get_current_billing_account`、`list_account_users`、`get_merchant` |
| 上传 | `prepare_entry_attachment_upload`、`prepare_form_image_upload`、`prepare_import_file_upload`；没有 shell 时用 `upload_entry_attachment`、`upload_form_image`、`upload_import_file`（Base64） |
| Schema | `get_schema` |

## 典型工作流

1. **建表单**：`get_schema("FieldInput")` → 查要用的字段类型 → `create_form` → 返回表单链接与 `form_token`。考试 / 测评用 `create_exam_form` / `create_evaluation_form`。
2. **查数据**：`list_forms` 找 `form_token` → `get_form` 拿字段 api_code → `list_entries` 用 `filters` 下推过滤，`fields` 裁列，`sort` 排序，`next` 翻页。
3. **统计**：只要条数用 `count_entries`；分组 / 求和 / 趋势用 `aggregate_entries`；整表画像用 `get_form_data_summary`。不要翻页拉明细自己算。
4. **写 / 改数据**：`get_form` 拿 api_code → `create_entry` / `create_entries` / `update_entry` / `patch_entries`。
5. **导入文件**：`prepare_import_file_upload` 拿 `upload_url` 上传，得到 `attachment_id` → `import_entries_from_file(attachment_id, columns)`。对话里粘贴的表格文本直接 `create_entries`。
6. **带附件 / 图片**：`prepare_*_upload` 拿一次性 `upload_url`，`curl -F file=@<path> <upload_url>` 上传，把返回的 `attachment_id` 写进对应字段；没有 shell 时用 `upload_*` 传 Base64。

## 注意事项

- 写入 / 更新 / 过滤一律用字段 api_code，拿不准就先 `get_form`。
- 删除（数据、表单、字段 / 选项、视图、评论）和批量修改执行前，向用户复述影响范围并取得确认。删字段 / 选项前先 `check_field_data`。
- 分页走响应里的 `next`，原样回传。
- `like` 是子串匹配，不要加 `%`。
- `import_entries_from_file` 是后台任务：调一次即返回，告知用户"已开始、进度看数据页"后停手；报错 = 一行都没导入，改参数只重试一次。
- 聚合类工具不支持按 `creator_id` / `serial_number` 过滤；多值字段（多选/级联/矩阵/地址/表格）不能当分组维度，它们的分布用 `get_form_data_summary`；日期维度必须带 `bucket`。
- `search_entries_in_forms` 里带 `unavailable` 的表单是**没搜成**，必须单独重试，不能汇报成"没命中"。
- 选项的 `quota` 省略 = 不限量，正整数 = 名额上限；**勿传 `0`**（0 = 名额已满）。
- 限流（HTTP 429）时按 `Retry-After` 等待，告诉用户"接口请求频繁，稍后重试"。
