---
name: jinshuju
slug: jinshuju
displayName: 金数据（Jinshuju）
description: "通过金数据（Jinshuju，jinshuju.net）MCP 操作用户托管在金数据平台上的在线表单与表格：创建 / 复制 / 编辑 / 删除表单与主题，含自动判分的考试表单、选项计分的测评表单；创建 / 编辑多维表格；查询、新增（单条或批量）、更新、删除、批量修改数据，给数据写评论，或把本地 Excel / CSV 批量导入；建表格 / 看板视图筛选数据，建对外查询页供访客自助查询；上传本地图片或附件；在服务端统计数据（条数、分组、按天 / 周 / 月的趋势、整表字段分布画像、各表单收数统计），跨表单搜关键字；查询账户套餐额度、团队成员与收款商户。仅在用户操作其金数据平台数据时使用——触发信号：提到 金数据 / Jinshuju / jinshuju.net、给出 form_token，或要操作一张已托管在金数据上的表单、表格或数据。不要用于：用代码开发表单 / 问卷系统、把本地文件当普通文档分析（与导入到金数据表单无关时）、图片 / 票据 OCR、物流或监控等与平台无关的自动化，以及与金数据平台无关的通用数据处理。"
version: 2.0.0
author: Jinshuju
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [Forms, Data Collection, Survey, Productivity, CRM, 金数据]
    category: productivity
    related_skills: []
---

# 金数据（Jinshuju）

金数据（jinshuju.net）是中国领先的在线表单与数据收集平台。通过金数据 MCP，你可以用自然语言完成表单搭建与数据管理的全流程，**替代登录后台手动操作**。

## When to Use

本 skill **仅处理金数据线上表单平台（jinshuju.net）** 的表单搭建与数据管理，且需满足以下任一**平台信号**才触发：

- 用户明确提到"金数据"、"Jinshuju"、"jinshuju.net"
- 用户给出了 `form_token`，或要操作一张**已在金数据上**的表单 / 表格 / 数据（创建、复制、编辑、移动、删除表单或表格，修改主题，增删改查或批量修改 entries，导出数据）
- 用户上传了 Excel / CSV 并要把它**导入到金数据的某张表单 / 表格**
- 用户要给某张表单建**视图**（筛选 / 看板）或建**对外查询页**（让访客自助查数据）
- 用户要查询本账户的套餐额度、团队成员、收款商户

## When NOT to Use

以下场景**不要**用本 skill，直接退出、交给通用能力处理：

- 用代码 / 程序开发表单、问卷、评估系统（如在 Python / 前端项目里"做一个报名表 / 问卷"）
- 纯本地处理文件、Excel / CSV、文档分析（**若目标是把这份表格导入到金数据某表单 / 表格，则属于本 skill**）
- 图片、账单、票据的 OCR / 识别
- 物流、监控等与金数据平台无关的业务自动化
- 仅出现"表 / 表单 / 问卷"字眼，但并非操作金数据线上平台

判断不属于金数据平台操作时，**不要调用任何 MCP 工具**，按通用能力回答即可。

## 参数以 MCP 为准

金数据 MCP 的工具由开放 API v1 的 openapi.yaml 自动生成，随 API 同步更新。**每个工具的参数、取值、返回结构以 MCP 自带的工具描述为准**，本 skill 只讲"什么场景用哪个工具、按什么顺序、哪里容易踩坑"，不重复参数细节。

- 参数描述里写着 `Shape: schema "X"` 的，调 `get_schema("X")` 读结构，**不要猜**
- 建表单 / 加字段：先 `get_schema("FieldInput")`，它的 `x-variants` 把字段类型映射到各自的 schema（`TextField → TextFieldInput`、`RadioButton → RadioButtonInput`），再对要用的类型调 `get_schema` 看属性
- 考试 / 测评题型分别看 `ExamFieldInput` / `EvaluationFieldInput`；表单设置看 `FormSettingWriteInput`；主题看 `ThemeInput`；视图看 `FormViewInput`；对外查询页看 `OpensearchQueryInput`
- 报错会带 HTTP 状态和服务端的 `error_description` / `errors`，通常直接列出可用的字段 / operator / 取值——照着改参数再试

工具清单与分类见 [`references/tools.md`](references/tools.md)。

## Quick Reference

| 场景 | MCP 工具 |
|------|----------|
| 找表单（拿 form_token） | `list_forms`（`q` 按名称模糊搜） |
| 看表单结构（字段 api_code） | `get_form` |
| 建表单 | `get_schema` → `create_form` |
| 建考试 / 测评 | `create_exam_form` / `create_evaluation_form` |
| 改表单字段 / 设置 / 布局 | `edit_form`（考试 / 测评用 `edit_exam_form` / `edit_evaluation_form`） |
| 改字段显示规则 | `get_field_rules` → `edit_field_rules` |
| 删字段 / 选项前查有没有数据 | `check_field_data` |
| 改字段类型前预览数据损失 | `preview_field_type_change` |
| 改主题 / 头图（含 AI 生成头图） | `edit_theme` |
| 复制 / 移动 / 删除表单 | `copy_form` / `move_form` / `delete_form` |
| 看表单协作者 | `list_form_cooperators` |
| 表格（多维表） | `list_tables` / `get_table` / `create_table` / `edit_table` / `move_table` |
| 文件夹 | `list_folders` / `create_folder` |
| 列数据（筛选 / 裁列 / 排序 / 关键字） | `list_entries` |
| 单条数据 | `get_entry` / `create_entry` / `update_entry` / `delete_entry` |
| 批量新建 / 批量更新（≤200 条/次） | `create_entries` / `patch_entries` |
| 只要条数（可一次数多张表单） | `count_entries` |
| 服务端统计（求和 / 均值 / 分位 / 分组 / 趋势） | `aggregate_entries` |
| 整表数据画像 | `get_form_data_summary` |
| 各表单在某时间段收了多少数据 | `list_form_entry_stats` |
| 跨表单搜关键字（≤10 张） | `search_entries_in_forms` |
| 我填过的表单 / 我提交的数据 | `list_my_submitted_forms` / `list_my_submitted_entries` / `search_my_submitted_entries` |
| 数据评论 | `list_entry_comments` / `create_entry_comment` / `update_entry_comment` / `delete_entry_comment` |
| 导入 Excel / CSV | `prepare_import_file_upload`（或 `upload_import_file`）→ `import_entries_from_file` |
| 上传附件 / 表单图片 | `prepare_entry_attachment_upload` / `prepare_form_image_upload`（无 shell 时用 `upload_entry_attachment` / `upload_form_image`） |
| 视图 | `list_form_views` / `get_form_view` / `create_form_view` / `edit_form_view` / `delete_form_view` / `list_form_view_entries` |
| 对外查询页 | `get_opensearch_field_suggestions` / `list_opensearch_queries` / `get_opensearch_query` / `create_opensearch_query` / `edit_opensearch_query` |
| 账户 | `get_current_user` / `get_current_billing_account` / `list_account_users` / `get_merchant` |
| 读参数结构 | `get_schema` |

## Procedure

### 原则

> ⚠️ **绝不绕过 MCP**：金数据 MCP 工具不可用（未连接 / 授权失败 / 调用持续报错）时**立即停止**，**禁止**改用浏览器自动化（Playwright 等）、直接调 REST API、curl 或模拟后台操作来替代。正确做法见下方「MCP 不可用时」。（唯一例外：`prepare_*_upload` 明确要求用 `curl -F` 把本地文件传到它给的一次性 `upload_url`。）

1. **先看再动**：操作未知表单前，先 `get_form` 拿字段结构。写数据时 entry 的键**必须是字段 `api_code`**（或 `api_code_alias`），传中文 label 会被丢弃；选项值可以传选项 api_code 或选项文字。

2. **条件下推优先**：`list_entries` 用 `filters` 把条件下推到数据库；不知道值在哪个字段就用 `keyword` 一次搜全表单所有可搜字段（别逐字段发 `like`）。用 `fields` 只取需要的列、用 `sort` 让服务端排序。默认每页 50 条、`limit` 最大 1000；翻页把上一页的 `next` 原样回传。

3. **统计不拉全量**：问"多少 / 多少钱 / 最多的是哪个 / 趋势怎么样"时**不要**翻页拉明细再自己算——只要条数用 `count_entries`；要具体数字、分组、按天 / 周 / 月趋势用 `aggregate_entries`；要整张表单的分布画像用 `get_form_data_summary`。字段支持哪些聚合函数、能不能分组，用 `get_form(include_analytics=true)` 看每个字段的 `analytics`。

4. **先列再改**：批量操作前先 `list_entries` 拉出命中记录展示给用户，**用户确认后**再执行——批量更新用 `patch_entries` 一次提交（≤200/批）；删除逐条循环 `delete_entry`，每 20 条汇报一次进度。

5. **删除要确认**：`delete_entry`、`delete_form`、删字段 / 选项、`delete_form_view`、`delete_entry_comment` 都必须得到用户显式确认。删字段 / 选项前先 `check_field_data`，有数据时把影响告诉用户。

6. **脱敏展示**：输出手机号 / 邮箱 / 身份证默认打码（`138****1234`），除非用户明确要求原文。

7. **不静默吞错**：字段类型不支持、套餐限制、权限不足的报错原文回显并给出替代方案。

### 典型任务流

**① 新建表单**
```
1. get_schema("FieldInput") → 对要用的字段类型再 get_schema("<Type>Input")
2. create_form，传字段列表（+ 需要的 setting）
   考试 / 测评改用 create_exam_form / create_evaluation_form
   要"分页式 / 一页一题"传 layout:"card"；只想分成几页就保持 classic 加 PageBreak
3. 返回表单链接和 form_token
4. 如需特殊样式，追加 edit_theme（ThemeInput 里有 generate_header_image 让 AI 生成头图）
```

**② 条件查询 / 导出**
```
1. get_form → 记下字段 api_code 和选项 api_code
2. list_entries 用 filters 下推条件；不知道在哪个字段就用 keyword；
   只展示几列传 fields，要倒序 / 取前 N 传 sort + limit；
   不想再对照 get_form 翻译表头可传 include_labels:true
3. next 翻页拿全部数据
4. Markdown 表格展示，关键字段脱敏
5. 询问用户是否需要生成 CSV
```

**③ 批量更新**
```
1. get_form → 拿目标字段 api_code + 目标选项 api_code
2. list_entries + filters 拉出命中集，展示前 10 条 + 总数
3. 用户确认后，patch_entries 一次提交（每行 { serial_number, entry }，只改提供字段，每批 ≤200 自行分批）
   注意：patch_entries 不能写附件字段，附件只能逐条 update_entry
4. 读返回的 failed_rows（按 serial_number），向用户汇总成功 / 失败
```

**④ 批量删除**
```
1. list_entries + filters 拉出命中集，记录 serial_number
2. 必须得到用户显式"确认删除"
3. 逐条循环 delete_entry，每 20 条汇报进度
```

**⑤ 批量写入数据（对话里给的 / 粘贴的表格）**
```
1. get_form → 拿目标字段 api_code
2. 每行整理成 { api_code: value } 对象
3. create_entries 一次提交（每批 ≤200，超过自行分批）
4. 读返回的 errors（按下标），向用户汇总成功 / 失败
   注意：不幂等，失败后不要整批重发，只补 errors 里的行
```

**⑥ 从本地 Excel / CSV 文件导入**
```
1. 读本地文件看表头；get_form / get_table 拿目标字段 api_code
2. prepare_import_file_upload → 用 curl -F file=@<path> <upload_url> 上传，拿 attachment_id
   （没有 shell 时用 upload_import_file 传 Base64；对话里粘贴的表格文本走 ⑤，别转成文件导入）
3. import_entries_from_file(attachment_id, columns=[{field_api_code, column_label | sheet_column_index}])
   表单每个必填字段都要有一列；需要去重传 unique_field_code
4. 返回 201 = 后台任务已开始：告诉用户"导入已开始，进度看数据页"，然后停手——
   别重复调用、别自己再逐行写数据；报错 = 一行都没导入，按错误改映射后重试一次
```

**⑦ 多维表格（Tables）**
```
- 表格是独立资源：list_tables / get_table / create_table / edit_table / move_table，
  别用 list_forms / get_form / edit_form 操作表格（数据读写仍用 list_entries 等，传表格 token）
- 列类型只有 15 种（见 create_table 描述），选项类只有单选 / 多选
- 建空表（暂时没数据要进）传 with_default_entries:true 补 3 行空行；紧接着要写数据就别开
- 表格只能放进 kind="table" 的文件夹（list_folders 看 kind，或 create_folder(kind:"table")）
```

**⑧ 视图筛选（Views）**
```
1. get_form → 拿字段 api_code
2. create_form_view(view={...})，结构见 get_schema("FormViewInput")：
   view_type 为 grid / kanban / stats（form 仅表格可用，是对外填写页）
   filter 与 list_entries 同一套 {field, operator, value}，但视图里不能用 serial_number / creator_id
3. 按视图取数用 list_form_view_entries（自动套用视图的筛选 / 排序 / 列）
4. edit_form_view 只改传入的键；预设视图删不掉，也不能删到一个不剩
```

**⑨ 对外查询页（访客自助查数据）**
```
1. list_opensearch_queries(form_token) 看是否已有，避免重复建
2. get_opensearch_field_suggestions(form_token) 拿可搜 / 可展示字段和推荐字段
3. create_opensearch_query(query={form_token, name, search_field_rules, display_field_rules, ...})
   需要表单管理权限；套餐不含该功能返回 402
4. edit_opensearch_query 改配置，enabled:false 下线、true 重新开启
```

**⑩ 数据统计 / 分析**
```
1. 先 count_entries 探范围（带上要分析的 filters）
2. get_form(include_analytics=true) 看字段的 agg_funcs / groupable
3. aggregate_entries：metrics 1~20 个；dimensions 最多 2 个，日期维度必须带 bucket（day/week/month）= 趋势
   分组按第一个指标降序，limit 默认 20 / 上限 200，看 row_count + truncated 判断是不是全部
4. 整表全貌用 get_form_data_summary
5. 维度值 null 是"该字段没填"的那一组，别丢
6. 只有用户要看具体记录时才 list_entries，并用 fields 只取要展示的列
```

**⑪ 跨表单找一个值 / 看整体收数**
```
- 搜关键字：search_entries_in_forms(keyword, form_tokens?)，一次范围最多 10 张表单；
  返回每张表单的命中数 + 流水号（不含字段值）；带 unavailable 的表单是"没搜成"，
  必须单独重试，不能当"没命中"汇报；没出现在结果里的才是"没命中"
- 一次数多张表单：count_entries(form_token=[...≤10])，此时 filters 只能用 created_at / updated_at / creator_id
- "这周哪些表单收数最多"：list_form_entry_stats(from, to, by?)
```

**⑫ 上传文件**
```
有 shell 且能访问 jinshuju.net（Claude Code / Cursor / Codex 等）：
  prepare_entry_attachment_upload / prepare_form_image_upload / prepare_import_file_upload
  → curl -F file=@<path> <upload_url>（30 分钟内有效、一次性）→ 拿 attachment_id 写进对应位置
没有 shell 或 curl 失败：小文件用 upload_entry_attachment / upload_form_image / upload_import_file 传 Base64
  （表单图片也可直接给公网图片 URL）
```

## Pitfalls

- **entry 键写成中文 label** → 被丢弃，全丢光时报 `Entry attributes cannot be empty` 并列出被丢的键；键必须是 `api_code`
- **简单字段包成对象**（`{"value": "张三"}`）→ 直接传字符串；各类型的写法见 `create_entry` 的 `entry` 描述里的表格
- **`like` 带 SQL 通配符**（`"张%"`）→ 按字面匹配 `%`，查不到；直接传 `"张"`
- **operator 与字段类型不匹配** → 400，错误信息列出可用 operator，照着改
- **批量新建循环调 `create_entry`** → 用 `create_entries`（≤200 条/批，部分成功，按下标返回 `errors`，不幂等）
- **批量更新循环调 `update_entry`** → 用 `patch_entries`（≤200 行/批）；但它**不能写附件字段**，附件逐条 `update_entry`
- **`update_entry` 改附件字段只传新文件** → 附件按整组替换，要保留旧文件就把读到的 URL / attachment id 一起传回
- **`ESignatureField` / `FormulaField` 写入 entry** → 服务端忽略
- **测试号段**（`13800138000`）→ 号段校验拒；用真实在用号段
- **改选项文案用 remove + add** → 会换 api_code，历史数据引用失效；改名用 `fields.update_choices.update`
- **删字段 / 选项不先查数据** → 有数据的会被永久清除；先 `check_field_data`（一次最多 100 个目标），有数据时告知用户、确认后再删
- **直接改字段类型** → 可能清掉数据；先 `preview_field_type_change`，会清数据的改动要带 `confirm_data_loss: true`；考试题和部门 / 年级字段不能原地改类型，只能删了重建
- **字段显示规则的 comparator 跟触发字段类型不匹配** → 400 并列出可用 comparator；规则按 `get_field_rules` 返回的 0-based `index` 定位
- **用 PageBreak 拼一页一题** → 整表分页式传 `layout:"card"`（card 不能放 PageBreak / MultipleBlanksField / WidgetContact / WidgetVideo）
- **用 create_form 建考试 / 测评** → 用 `create_exam_form` / `create_evaluation_form`；测评计分写在 answers + `answer_setting_mode=relative`，不要用普通选项的 `calculable` / `operand_value`
- **考试开限时又把题目设必填** → `show_timeout=true` 与题目 `required` 互斥；默认不开限时
- **编辑考试 / 测评时只传改动的 answers / indicators / comments** → 这些是整体替换；先 `get_form` 读出现状（考试表单带 `include_exam_setting=true`），回传完整列表和原有 `api_code`
- **给选项设 `quota:0` 想表示不限量** → `0` 是名额已满；不限量就省略 `quota`
- **`fill_frequency.condition=by_fields` 不给 `limited_field_api_codes`** → 保存被拒
- **三类关闭规则一起写** → `manually_close_rule` / `by_time_range_close_rule` / `by_entries_close_rule` 互斥，写一类会清掉其他
- **换背景 / 容器颜色不传 `dominant_color`** → 表单深浅色模式不跟着变，文字可能看不清
- **`import_entries_from_file` 后重复调用 / 自己再逐行写** → 它是后台任务，调一次即可
- **把粘贴的表格转成文件再导入** → 直接 `create_entries`
- **拿表单工具操作表格**（`get_form` / `edit_form` / `move_form`）→ 用 `get_table` / `edit_table` / `move_table`
- **`move_form` / `move_table` 移出文件夹不传 `folder_token`** → 必须显式传 `folder_token: null`；重试时带上 `original_folder_token`
- **要统计却翻页拉全量明细自己算** → 用 `count_entries` / `aggregate_entries` / `get_form_data_summary`
- **多值字段（多选 / 级联 / 矩阵 / 地址 / 表格）当 `dimensions`** → 被拒；这类字段的分布用 `get_form_data_summary`
- **日期维度不传 `bucket`** → 出不来趋势；按 `day` / `week` / `month` 分桶
- **把分组结果当全量** → 看 `row_count` 和 `truncated`
- **聚合类工具按 `creator_id` / `serial_number` 过滤** → 被拒；按提交者取数用 `list_entries`
- **把 `search_entries_in_forms` 里带 `unavailable` 的表单报成"没命中"** → 那是没搜成，单独重试
- **超过 99999 条的表单用 `keyword`** → 没开分析引擎时直接 400；改用 `filters` 精确过滤
- **账户级 token 调 `list_my_submitted_*` / `search_my_submitted_entries`** → 400（账户 token 没有"当前用户"）
- **评论里 @ 非协作者** → 整条评论被拒；`@[<user_id>]` 只能 @ 表单协作者（`list_form_cooperators` 查）
- **套餐 / 额度不足当系统故障重试** → 把原文告诉用户并给替代方案（升套餐，或上传本地图代替 AI 生成头图）
- **限流（HTTP 429）把原始 JSON 抛给用户** → 告知"接口请求频繁，稍后重试"，按 `Retry-After` 等待，合并可批量的请求

## Verification

操作完成后确认：
- **创建 / 编辑表单**：返回中包含有效 `form_token` 和表单链接
- **create_entry**：返回包含 `serial_number`；有 `ignored_fields` 时告诉用户哪些值没存（被显示规则隐藏等）
- **create_entries**：`errors` 为空（有部分失败时按下标核对原因）
- **patch_entries**：`failed_rows` 为空（有部分失败时按 serial_number 核对 reason）
- **delete_entry**：返回被删条目的 serial_number
- **delete_form**：表单进了回收站，可在产品里恢复——告诉用户这一点
- **create_table / edit_table**：`get_table` 能读到刚建 / 改的字段
- **create_form_view / edit_form_view**：`list_form_view_entries` 能按其筛选取数
- **import_entries_from_file**：调用成功即任务已入队；让用户去数据页看进度
- **create_opensearch_query**：返回对外访问地址，发给用户
- **aggregate_entries**：分组时核对 `row_count` 与 `truncated` 再下结论
- **批量操作**：向用户汇报"共 N 条，成功 X 条，失败 Y 条"

## MCP 配置

金数据 MCP 端点：`https://jinshuju.net/mcp`（远程 HTTP）。

**方式 A · OAuth（推荐）**：客户端里添加连接器、填上面的地址，按提示登录金数据授权即可。
```json
{ "mcpServers": { "jinshuju": { "url": "https://jinshuju.net/mcp" } } }
```
Claude Code：`claude mcp add jinshuju -s user --transport http https://jinshuju.net/mcp`，然后在 Claude Code 里运行 `/mcp` 登录。

**方式 B · 访问令牌（不支持 OAuth 的客户端 / 脚本）**：在请求头里带 `Authorization: Bearer <访问令牌>`。
```json
{
  "mcpServers": {
    "jinshuju": {
      "url": "https://jinshuju.net/mcp",
      "headers": { "Authorization": "Bearer YOUR_ACCESS_TOKEN" }
    }
  }
}
```
个人访问令牌在「个人资料 → API」（https://next.jinshuju.net/profile/api）创建，只能看到自己创建或被共享的表单；账户访问令牌在「系统设置 → 账户 API」（https://next.jinshuju.net/system/api_licence）创建，能看到整个账户的表单。

**方式 C · 本地 stdio（只支持本地 MCP 的客户端）**：
```json
{
  "mcpServers": {
    "jinshuju": {
      "command": "npx",
      "args": ["-y", "@jinshuju/mcp"],
      "env": { "JINSHUJU_ACCESS_TOKEN": "YOUR_ACCESS_TOKEN" }
    }
  }
}
```

常见配置错误：漏 `/mcp` 后缀、用 `http://`、`Authorization` 缺 `Bearer ` 前缀、还在用旧的 `Basic`（API Key / Secret）凭证——旧凭证已不再支持，换成访问令牌或 OAuth。

### MCP 不可用时

工具未连接 / 授权失败 / 持续报错时，按顺序降级，**不要**用任何非标方式替代：

1. 告知用户"金数据 MCP 未就绪"，不要假装已完成操作。
2. 对照上面的「常见配置错误」引导排查（端点、`Bearer ` 前缀、OAuth 授权等）。
3. 仍不行，就给出在金数据后台（jinshuju.net）手动操作的步骤指引。

> 超大表单（数十个字段）即使 MCP 正常，也建议先 `create_form` 建核心字段，再用 `edit_form` 分批补充，降低超长请求被截断 / 超时的风险。
