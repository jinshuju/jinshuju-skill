# 金数据 MCP 工具地图

金数据 MCP 共 65 个工具（本 skill 只用到表单相关的部分，多维表格见 jinshuju-table），由开放 API v1 的 [openapi.yaml](https://jinshuju.net/api/v1/openapi.yaml) 自动生成，和 API 保持同步。

**本文件只说明每个工具用在什么场景。** 参数名、取值范围、返回结构都以 MCP 自带的工具描述为准；参数描述里写着 `Shape: schema "X"` 的，调 `get_schema("X")` 读结构（也可以读资源 `jinshuju://schemas/X`）。

## 通用约定

- **定位**：表单用 `form_token`（`list_forms` 返回的 `token`，24 位十六进制 id 也行）；单条数据用整数 `serial_number`。
- **翻页**：默认每页 50 条，`limit` 最大 1000（`list_folders` / `list_account_users` 最大 100）；把上一页的 `next` 原样回传。`page` 可以跳页 / 并行读（`(page-1)×limit` ≤ 10000）。`limit: 0` 只返回 `total`。
- **filters**：数组 `[{field, operator, value}]`，多条为 AND。operator 有 `eq` `ne` `gt` `gte` `lt` `lte` `between` `not_between` `any_in` `none_in` `like` `not_like` `null` `not_null` `within_last`；每种字段只接受其中一部分，传错会 400 并列出可用的。
  - `like` 是子串匹配，不要加 `%`
  - `within_last` 的 value 形如 `{"unit": "day", "n": 7}`
  - 数据接口里还能用 `created_at`、`creator_id`（`eq`，只能一次）、`serial_number`（`eq` / `any_in` / `none_in`）
- **entry 写法**：键是字段 `api_code`（或 `api_code_alias`）；各字段类型的值写法见 `create_entry` 的 `entry` 参数描述里的表格。
- **错误**：返回 HTTP 状态和服务端的 `error_description` / `errors`，照着改再试；429 按 `Retry-After` 等待。
- **令牌范围**：个人令牌只能看到自己创建或被共享的表单；账户令牌能看到整个账户。账户令牌没有"当前用户"，调 `list_my_submitted_*` 会 400。

## 表单

| 工具 | 用途 |
|---|---|
| `list_forms` | 列表单。`q` 按名称模糊搜，`filters` / `sort` 可按 `created_at` / `last_entry_created_at` / `entries_count` 筛选排序；`include_transactions` 带收款统计 |
| `get_form` | 表单结构：字段及其 `api_code`、设置。按需加 `include_analytics`（字段可用的聚合函数 / 能否分组）、`include_theme`、`include_field_rules`、`include_exam_setting`、`include_extended_attributes`、`include_transactions` |
| `create_form` | 建表单。字段先 `get_schema("FieldInput")` 再查各类型；设置看 `FormSettingWriteInput`；`layout: "card"` 是一页一题 |
| `edit_form` | 增量改表单：`fields` 下的 `add` / `remove` / `update` / `update_choices`，以及 `setting`、`layout`、`name`、`description`、`field_rules` |
| `copy_form` | 复制表单；`with_notification_rules` 连通知规则一起复制 |
| `delete_form` | 把表单和数据移进回收站（可在产品里恢复）。需用户确认 |
| `move_form` | 移进文件夹；`folder_token: null` 移出 |
| `list_form_cooperators` | 表单协作者和角色（@ 人写评论前用） |
| `get_field_rules` | 字段显示规则（逻辑跳转），每条带 0-based `index` |
| `edit_field_rules` | 按 `index` 增 / 删 / 改显示规则，其他规则不动 |
| `check_field_data` | 删字段 / 选项前查有没有数据（一次最多 100 个目标） |
| `preview_field_type_change` | 改字段类型前预览会保留 / 清掉多少数据 |
| `edit_theme` | 改主题：颜色、背景、头图、字体、提交按钮；`generate_header_image` 用 AI 生成头图（消耗 AI 点数）。结构见 `ThemeInput` |

## 考试 / 测评

| 工具 | 用途 |
|---|---|
| `create_exam_form` | 建考试（自动判分）。题型用 `ExamFieldInput` 里的 SingleSelect / MultiSelect / TrueOrFalse / DropDownSelect / FillInBlank / ShortAnswer / FillInNumber，每题带 answers |
| `edit_exam_form` | 改考试题目和 `exam_setting` |
| `create_evaluation_form` | 建测评（心理测试、能力评估、自评、培训反馈）。计分题每个选项都在 answers 里给分，`answer_setting_mode=relative` |
| `edit_evaluation_form` | 改测评题目和 `evaluation_setting`（报告、分段评语、维度） |

这四个工具都分两步执行（先建 / 改表单，再写场景设置）；第二步失败时表单已经建好，结果里会说明。

## 数据

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
| `list_form_entry_stats` | 某日期段内各表单收到多少提交（`kind: "form"` 只数表单），可按 `day` / `week` / `month` 分桶 |
| `search_entries_in_forms` | 一个关键字搜 ≤10 张表单，返回每张的命中数和流水号（不含内容）；`unavailable` 表示没搜成 |

## 我提交的

| 工具 | 用途 |
|---|---|
| `list_my_submitted_forms` | 当前用户填过的表单 |
| `list_my_submitted_entries` | 当前用户在某张表单提交的数据（只含对填写者公开的字段） |
| `search_my_submitted_entries` | 在自己提交过的数据里搜关键字 |

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
| `create_form_view` / `edit_form_view` | 建 / 改视图，结构见 `FormViewInput`（`view_type`：grid / kanban / stats） |
| `delete_form_view` | 删视图（预设视图删不掉，也不能删光）。需用户确认 |
| `list_form_view_entries` | 按视图的筛选 / 排序 / 列取数 |

## 对外查询页

| 工具 | 用途 |
|---|---|
| `get_opensearch_field_suggestions` | 表单可用于查询 / 展示的字段及推荐字段 |
| `list_opensearch_queries` / `get_opensearch_query` | 列 / 读自己建的查询页 |
| `create_opensearch_query` / `edit_opensearch_query` | 建 / 改查询页，结构见 `OpensearchQueryInput`；`enabled: false` 下线 |

## 文件夹 / 账户

| 工具 | 用途 |
|---|---|
| `list_folders` / `create_folder` | 文件夹；表单放进 `kind=form` 的文件夹 |
| `get_current_user` | 当前用户（账户令牌返回账户所有者） |
| `get_current_billing_account` | 套餐、本月用量与额度、绑定的收款账户 |
| `list_account_users` | 团队成员 |
| `get_merchant` | 小金商户（金数据代收款商户）及开通进度、余额、结算信息 |

## 上传

| 工具 | 用途 |
|---|---|
| `prepare_entry_attachment_upload` | 拿一次性 `upload_url`，`curl -F file=@<path> <upload_url>` 上传，得到 `attachment_id` 写进附件字段 |
| `prepare_form_image_upload` | 同上，用于表单图片；`image_type` 决定 `attachment_id` 能用在哪（选项图、头图、背景、轮播、商品图等） |
| `prepare_import_file_upload` | 同上，用于导入的 xlsx / xls / csv |
| `upload_entry_attachment` / `upload_form_image` / `upload_import_file` | 没有 shell 时用 Base64 直接上传小文件 |

`upload_url` 30 分钟内有效、只能用一次。表单图片也可以直接给公网 URL。

## Schema

| 工具 | 用途 |
|---|---|
| `get_schema` | 按名称读 openapi schema，例如 `FieldInput`、`TextFieldInput`、`FormSettingWriteInput`、`ThemeInput`、`FormViewInput` |
