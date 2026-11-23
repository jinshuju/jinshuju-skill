# 金数据表格 MCP 工具地图

金数据 MCP 共 65 个工具（本 skill 只用到数据表相关的部分，表单相关见 jinshuju-form），由开放 API v1 的 [openapi.yaml](https://jinshuju.net/api/v1/openapi.yaml) 自动生成，和 API 保持同步。

**本文件只说明每个工具用在什么场景。** 参数名、取值范围、返回结构都以 MCP 自带的工具描述为准；参数描述里写着 `Shape: schema "X"` 的，调 `get_schema("X")` 读结构（也可以读资源 `jinshuju://schemas/X`）。

## 通用约定

- **定位**：表结构工具（`get_table` / `edit_table` / `move_table`）用 `table_token`；行数据、统计、视图、评论、上传等工具的 `form_token` 参数**也传表 token**；单行用整数 `serial_number`。
- **翻页**：默认每页 50 条，`limit` 最大 1000（`list_folders` / `list_account_users` 最大 100）；把上一页的 `next` 原样回传。`page` 可以跳页 / 并行读（`(page-1)×limit` ≤ 10000）。`limit: 0` 只返回 `total`。
- **filters**：数组 `[{field, operator, value}]`，多条为 AND。operator 有 `eq` `ne` `gt` `gte` `lt` `lte` `between` `not_between` `any_in` `none_in` `like` `not_like` `null` `not_null` `within_last`；每种字段只接受其中一部分，传错会 400 并列出可用的。
  - `like` 是子串匹配，不要加 `%`
  - `within_last` 的 value 形如 `{"unit": "day", "n": 7}`
  - 数据接口里还能用 `created_at`、`creator_id`（`eq`，只能一次）、`serial_number`（`eq` / `any_in` / `none_in`）
- **entry 写法**：键是字段 `api_code`（或 `api_code_alias`）；各字段类型的值写法见 `create_entry` 的 `entry` 参数描述里的表格。
- **错误**：返回 HTTP 状态和服务端的 `error_description` / `errors`，照着改再试；429 按 `Retry-After` 等待。
- **令牌范围**：个人令牌只能看到自己创建或被共享的表单；账户令牌能看到整个账户。

## 表格（多维表）

| 工具 | 用途 |
|---|---|
| `list_tables` / `get_table` | 列 / 读表格（`get_table` 对表单 token 返回 404） |
| `create_table` | 建表格；列类型只有 15 种，见工具描述；`with_default_entries: true` 补 3 行空行 |
| `edit_table` | 增量改表格：`fields` 下的 `add` / `remove` / `update` / `update_choices` |
| `check_field_data` | 删列 / 选项前查有没有数据 |
| `preview_field_type_change` | 改列类型前预览会保留 / 清掉多少数据 |
| `move_table` | 移进 `kind=table` 的文件夹；`folder_token: null` 移出 |

表格数据的读写、统计用下面的行数据工具，`form_token` 传表 token。

## 行数据

| 工具 | 用途 |
|---|---|
| `list_entries` | 列数据：`filters`、`keyword`（全字段模糊搜）、`fields`（裁列）、`sort`、`include_labels`（值带上字段标签） |
| `get_entry` | 按 `serial_number` 读一条 |
| `create_entry` | 新建一条；被显示规则隐藏的值会出现在 `ignored_fields` |
| `update_entry` | 部分更新一条（只改传入的字段）；附件字段按整组替换 |
| `delete_entry` | 删除一条。需用户确认 |
| `create_entries` | 批量新建 ≤200 条；部分成功，按下标返回 `errors`；不幂等 |
| `patch_entries` | 批量部分更新 ≤200 行 `{serial_number, entry}`；按 serial_number 返回 `failed_rows`；**不能写附件字段** |
| `import_entries_from_file` | 把已上传的 Excel / CSV（`attachment_id`）按 `columns` 映射导入；后台执行，201 即已开始 |

## 统计 / 搜索

| 工具 | 用途 |
|---|---|
| `count_entries` | 只数条数。`form_token` 传数组可一次数 ≤10 张表单（此时 filters 只能用 `created_at` / `updated_at` / `creator_id`，不支持 keyword） |
| `aggregate_entries` | 服务端聚合：`metrics`（1~20 个，`count` / `count_non_empty` / `count_empty` / `count_unique` / `sum` / `avg` / `min` / `max` / `stddev` / `median` / `p25` / `p75` / `p90`），`dimensions`（≤2 个，日期必须带 `bucket`） |
| `get_form_data_summary` | 整表画像：每个可分析字段的分布 / 统计 + 概览，几 KB |
| `list_form_entry_stats` | 某日期段内各表格收到多少新行（`kind: "table"` 只数表格），可按 `day` / `week` / `month` 分桶 |
| `search_entries_in_forms` | 一个关键字搜 ≤10 张表单，返回每张的命中数和流水号（不含内容）；`unavailable` 表示没搜成 |

## 数据评论

| 工具 | 用途 |
|---|---|
| `list_entry_comments` | 列一条数据的评论 |
| `create_entry_comment` | 写评论；`@[<user_id>]` 只能 @ 表单协作者；`parent_id` 回复某条评论；不能带附件 |
| `update_entry_comment` | 改自己的评论 |
| `delete_entry_comment` | 删评论（作者、表单创建者或管理员）。需用户确认 |

## 视图

| 工具 | 用途 |
|---|---|
| `list_form_views` / `get_form_view` | 列 / 读视图 |
| `create_form_view` / `edit_form_view` | 建 / 改视图，结构见 `FormViewInput`（`view_type`：grid / kanban / stats / form，form 是对外填写页，默认未发布） |
| `delete_form_view` | 删视图（预设视图删不掉，也不能删光）。需用户确认 |
| `list_form_view_entries` | 按视图的筛选 / 排序 / 列取数 |

## 文件夹 / 账户

| 工具 | 用途 |
|---|---|
| `list_folders` / `create_folder` | 文件夹；`kind` 为 `form` 或 `table`，两种不能混放 |
| `get_current_user` | 当前用户（账户令牌返回账户所有者） |
| `get_current_billing_account` | 套餐、本月用量与额度、绑定的收款账户 |
| `list_account_users` | 团队成员 |

## 上传

| 工具 | 用途 |
|---|---|
| `prepare_entry_attachment_upload` | 拿一次性 `upload_url`，`curl -F file=@<path> <upload_url>` 上传，得到 `attachment_id` 写进附件字段 |
| `prepare_import_file_upload` | 同上，用于导入的 xlsx / xls / csv |
| `upload_entry_attachment` / `upload_import_file` | 没有 shell 时用 Base64 直接上传小文件 |

`upload_url` 30 分钟内有效、只能用一次。

## Schema

| 工具 | 用途 |
|---|---|
| `get_schema` | 按名称读 openapi schema，例如 `NumberFieldColumnInput`、`RelationFieldColumnInput`、`FormulaFieldColumnInput`、`FormViewInput` |
