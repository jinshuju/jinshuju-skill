---
name: jinshuju
slug: jinshuju
displayName: 金数据（Jinshuju）
description: "通过金数据（Jinshuju，jinshuju.net）MCP 操作用户托管在金数据平台上的在线表单与表格：创建 / 复制 / 编辑表单与主题，含自动判分的考试表单、选项计分的测评表单；创建 / 编辑多维表格；查询、新增（单条或批量）、更新、删除、批量修改数据，或把本地上传的 Excel / CSV 批量导入；建表格 / 看板视图筛选数据，建对外查询页供访客自助查询；用上传凭证上传本地图片或文件；在服务端统计数据（条数、分组、按天 / 周 / 月的趋势、整表字段分布画像），跨表单搜关键字；查询账户套餐额度与团队成员。仅在用户操作其金数据平台数据时使用——触发信号：提到 金数据 / Jinshuju / jinshuju.net、给出 form_token，或要操作一张已托管在金数据上的表单、表格或数据。不要用于：用代码开发表单 / 问卷系统、把本地文件当普通文档分析（与导入到金数据表单无关时）、图片 / 票据 OCR、物流或监控等与平台无关的自动化，以及与金数据平台无关的通用数据处理。"
version: 1.9.0
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
- 用户给出了 `form_token`，或要操作一张**已在金数据上**的表单 / 表格 / 数据（创建、复制、编辑、移动表单或表格，修改主题，增删改查或批量修改 entries，导出数据）
- 用户上传了 Excel / CSV 并要把它**导入到金数据的某张表单 / 表格**
- 用户要给某张表单建**视图**（筛选 / 看板）或建**对外查询页**（让访客自助查数据）
- 用户要查询本账户的套餐额度、团队成员

## When NOT to Use

以下场景**不要**用本 skill，直接退出、交给通用能力处理：

- 用代码 / 程序开发表单、问卷、评估系统（如在 Python / 前端项目里"做一个报名表 / 问卷"）
- 纯本地处理文件、Excel / CSV、文档分析（**若目标是把这份表格导入到金数据某表单 / 表格，则属于本 skill**，用 `import_entries_from_file`）
- 图片、账单、票据的 OCR / 识别
- 物流、监控等与金数据平台无关的业务自动化
- 仅出现"表 / 表单 / 问卷"字眼，但并非操作金数据线上平台

判断不属于金数据平台操作时，**不要调用任何 MCP 工具**，按通用能力回答即可。

## Quick Reference

| 场景 | MCP 工具 |
|------|----------|
| 列出文件夹 | `list_folders` |
| 新建文件夹 | `create_folder` |
| 列出表单 | `list_forms` |
| 查看表单详情（字段结构） | `get_form` |
| 检查字段/选项是否已有数据（删前确认） | `check_field_data` |
| 创建表单 | `create_form` |
| 创建考试表单（答案 + 自动判分） | `create_exam_form` |
| 编辑考试表单 | `edit_exam_form` |
| 创建测评表单（选项计分 / 维度报告） | `create_evaluation_form` |
| 编辑测评表单 | `edit_evaluation_form` |
| 复制表单 | `copy_form` |
| 移动表单到文件夹 | `move_form` |
| 修改表单字段/设置 | `edit_form` |
| 查看字段显示规则 | `get_field_rules` |
| 增删改字段显示规则（外科式） | `edit_field_rules` |
| 修改表单主题 | `edit_theme` |
| 上传本地图片（头图 / 选项配图） | `prepare_form_image_upload` |
| 上传文件写入附件字段 | `prepare_entry_attachment_upload` |
| 列出表格（多维表） | `list_tables` |
| 查看表格详情（字段结构） | `get_table` |
| 创建表格 | `create_table` |
| 编辑表格字段/名称 | `edit_table` |
| 移动表格到文件夹 | `move_table` |
| 列出表单视图 | `list_form_views` |
| 查看视图详情 | `get_form_view` |
| 创建视图（表格 / 看板） | `create_form_view` |
| 编辑视图 | `edit_form_view` |
| 删除视图 | `delete_form_view` |
| 按视图筛选列出数据 | `list_form_view_entries` |
| 列出数据（可裁列 / 排序 / 关键字搜索） | `list_entries` |
| 只要条数，不拉数据 | `count_entries` |
| 服务端统计（求和 / 均值 / 分位 / 分组 / 按天周月趋势） | `aggregate_entries` |
| 整张表单的数据画像（每个字段的分布 / 填答率） | `get_form_data_summary` |
| 在多张表单里搜同一个关键字（≤10 张） | `search_entries_in_forms` |
| 列出我填写 / 提交过的表单 | `list_my_submitted_forms` |
| 列出我在某表单提交的数据 | `list_my_submitted_entries` |
| 查看单条数据 | `get_entry` |
| 新建数据（单条） | `create_entry` |
| 批量新建数据（一次最多 200 条） | `create_entries` |
| 更新数据（单条） | `update_entry` |
| 批量更新数据（一次最多 200 条，PATCH） | `patch_entries` |
| 删除数据（单条） | `delete_entry` |
| 把本地上传的 Excel / CSV 导入表单/表格（后台任务） | `import_entries_from_file` |
| 列出对外查询页 | `list_opensearch_queries` |
| 查看对外查询页配置 | `get_opensearch_query` |
| 创建对外查询页（访客自助查数据） | `create_opensearch_query` |
| 编辑 / 启停对外查询页 | `edit_opensearch_query` |
| 当前用户信息 | `get_current_user` |
| 当前企业账户/套餐 | `get_current_billing_account` |
| 列出团队成员 | `list_account_users` |

## Procedure

### 原则

> ⚠️ **绝不绕过 MCP**：金数据 MCP 工具不可用（未连接 / 授权失败 / 调用持续报错）时**立即停止**，**禁止**改用浏览器自动化（Playwright 等）、直接调 GraphQL / REST API、curl 或模拟后台操作来替代——这类非标方式会产出中文乱码、字段不兼容的错误表单。正确做法见下方「MCP 不可用时」。

1. **先看再动**：操作未知表单前，先 `get_form` 拿字段结构——每个字段的 `api_code`、选项的 `choices[].api_code`、表格的 `dimensions[].api_code`。`create_entry` / `update_entry` 的键**必须是 `api_code`**，传中文 label 会被服务端丢弃。

2. **条件下推优先**：`list_entries` 的 `filters=[{field, operator, value}]` 把条件下推到数据库，比拉全量再本地筛选快几个数量级；不知道值在哪个字段就用 `keyword` 一次搜全表单所有字段（别逐字段发 `like`）。要搜多张表单用 `search_entries_in_forms`（≤10 张/次）。读明细时用 `fields` 只取需要的列、用 `sort` 让服务端排序，别把几十列全拉回来再本地处理。单次上限 50 条，超过用 `next` 翻页（传了 `sort` 时 `next` 是行偏移量，否则是 serial_number 游标）。

3. **统计不拉全量**：问"多少 / 多少钱 / 最多的是哪个 / 趋势怎么样"时**不要**翻页拉明细再自己算——只要条数用 `count_entries`；要具体数字、分组、按天 / 周 / 月趋势用 `aggregate_entries`；要整张表单的分布画像用 `get_form_data_summary`。响应大小与数据量无关，也不会因为漏翻一页而算错。字段支持哪些 operator / 聚合函数、能不能当分组维度，都在 `get_form` 返回的 `operators` 和 `analytics` 里，照着读别猜。

4. **先列再改**：批量操作前先 `list_entries` 拉出命中记录展示给用户，**用户确认后**再执行——批量更新用 `patch_entries` 一次提交（≤200/批）；删除仍逐条循环 `delete_entry`，每 20 条汇报一次进度。

5. **永不主动开 PUT**：`update_entry` 默认 `is_put=false`（PATCH，只改提供的字段）。`is_put=true` 会把未提供字段全部清空，只有用户明确说"整条替换"且已列全所有字段时才允许，且需二次确认。

6. **脱敏展示**：输出手机号/邮箱/身份证默认打码（`138****1234`），除非用户明确要求原文。

7. **不静默吞错**：字段类型不支持、套餐限制、权限不足的报错原文回显并给出替代方案。

### 典型任务流

**① 新建表单**
```
1. create_form，传字段列表 + setting
   （考试 / 测评场景改用 create_exam_form / create_evaluation_form，
    create_form 的 scene 已不支持 exam / evaluation，也不支持 vote / customer_acquisition，改用 form 场景；
    要"分页式 / 一页一题 / 自动翻页"传 layout:"card"，别拿 PageBreak 拼）
2. 返回表单链接和 form_token
3. 如需特殊样式，追加 edit_theme（可用 generate_header_image 让 AI 生成头图，
   本地已有图片则先 prepare_form_image_upload（type=header）上传）
```

**② 条件查询 / 导出**
```
1. get_form → 记下字段 api_code 和选项 api_code（顺便看每个字段的 operators）
2. list_entries 用 filters 下推条件（选项字段传 api_code 不是 label）；
   不知道值在哪个字段就用 keyword 一次搜全表单；
   只展示几列就传 fields 裁列，要倒序 / 取前 N 就传 sort（别拉回来再本地排）
3. next 翻页拿全部数据（有 sort 时 next 是行偏移量，否则是 serial_number 游标）
4. Markdown 表格展示，表头用 get_form 的 label，关键字段脱敏
5. 询问用户是否需要生成 CSV artifact
```

**③ 批量更新**
```
1. get_form → 拿目标字段 api_code + 目标选项 api_code
2. list_entries + filters 拉出命中集，展示前 10 条 + 总数
3. 用户确认后，用 patch_entries 一次提交（每行 { serial_number, entry }，PATCH 只改提供字段，每批 ≤200 自行分批）
4. 读返回的 updated_count + failed_rows（按 serial_number），向用户汇总成功/失败
```

**④ 批量删除**
```
1. list_entries + filters 拉出命中集，记录 serial_number
2. 必须得到用户显式"确认删除"
3. 逐条循环 delete_entry
4. 每 20 条汇报进度
```

**⑤ 批量导入数据**
```
1. get_form → 拿目标字段 api_code + 选项 api_code
2. 把每行整理成 { api_code: value } 对象（选项传 api_code）
3. create_entries 一次提交（每批 ≤200，超过自行分批循环）
4. 读返回的 created_count + errors（按下标），向用户汇总成功/失败
   注意：不幂等，重复提交会产生重复数据；失败后不要整批重发，按 errors 下标只补失败行
```

**⑥ 从本地上传的表格文件导入**（用户在对话里上传了 Excel / CSV，要写进某张表单 / 表格）
```
1. 先读文件（read_raw_content）看表头，get_form / get_table 拿目标字段 api_code
2. 组好 column_mapping（每列 → field_api_code；表头唯一时用 column_label，
   有重名/空表头才用 sheet_column_index）；需要去重传 unique_field_code
3. import_entries_from_file 调用一次即返回——它是后台任务
4. 告诉用户"导入已开始，进度看数据页"，然后停手：
   别轮询、别重复调用、别自己再逐行写数据
   报错 = 一行都没导入（校验在起任务前完成）：读错误、改参数、只重试一次
   （空表会先清掉占位空行）
```

**⑦ 多维表格（Tables）**
```
- 表格是独立于表单的资源：list_tables / get_table / create_table / edit_table / move_table，
  不要用 list_forms / get_form 那套去操作表格
- 建空表（暂时没有数据要进）传 with_default_entries:true 补几行空行，否则空网格看着像坏了；
  紧接着要导数据 / create_entries 就别开，免得数据落在空行下面
- 表格字段类型是表单的子集，选项类只支持单选(RadioButton)/多选(CheckBox)；
  FormulaField 引用列同表单：本请求内新列用 <gd-field data-cid="...">，已有列用 data-api-code
- 移动表格只能进 kind="table" 的文件夹（先 list_folders 找），表单文件夹放不了表格
```

**⑧ 视图筛选（Views）**
```
1. get_form → 拿字段 api_code
2. create_form_view：view_type 传 grid（表格）/ kanban（看板）/ stats（统计）
   看板要传 kanban_group_by_api_code（按哪个选择字段分列）、kanban_card_title_api_code；
   列的顺序传 kanban_group_order（分组选项 api_code 的顺序，没列出的排在后面，"未设置"列恒最后）、
   要隐藏某几列传 kanban_hidden_groups（未设置列用 "__unset__"；edit_form_view 传 [] 表示全部显示）
   filters 与 list_entries 同一套 {field, operator, value}（AND 组合，OR 分组只能在网页端编辑）
3. 按视图取数用 list_form_view_entries（自动套用视图的筛选/排序/列偏好），next 翻页
4. edit_form_view 只改传入项；delete_form_view 删不掉预设视图和最后一个视图
```

**⑨ 对外查询页（访客自助查数据）**
```
1. 先 list_opensearch_queries 看该表单是否已有，避免重复建
2. create_opensearch_query：search_field_rules 定义访客可用哪些字段查、
   display_field_rules 定义查到后展示哪些字段；allow_to_export_results 默认 false
3. 返回 url（发给访客）+ admin_url（后台管理）；仅表单管理员能建
4. edit_opensearch_query 改配置，enabled:false 下线该查询页、true 重新开启
```

**⑩ 数据统计 / 分析**
```
1. 先 count_entries 探范围（带上要分析的 filters），知道是 300 条还是 30 万条
2. 要具体数字用 aggregate_entries：
   metrics=[{"func":"sum","field":"field_5"}]（1~20 个，函数按字段类型受限）
   dimensions=[{"field":"field_city"}] 按 1~2 个字段分组（只有 analytics.groupable 的字段能分组）
   日期维度必须带 bucket:"day"/"week"/"month" —— 这就是趋势
   分组结果按第一个指标降序，limit 默认 20 / 上限 200，看 row_count + truncated 判断是否只是一段
3. 要整表全貌用 get_form_data_summary：每个字段的 buckets / stats + answered / null_count
4. 展示时把选项维度的 api_code 换成同返回里的 label；维度值 null 是"该字段没填"的那一组，别丢
5. 只有用户要看具体记录时才 list_entries，并用 fields 只取要展示的列
```

**⑪ 跨表单找一个值**
```
1. list_forms 拿候选表单 token（search 一次最多 10 张，多了拆成几次调用）
2. search_entries_in_forms(form_tokens, keyword) —— 返回每张表单的 matched + serial_numbers（不含字段值）
3. 带 unavailable 的表单是"没搜成"（无权限 / 超限 / 服务未响应），必须单独重试，
   绝不能当成"没命中"汇报；响应里完全没出现的 token 才是"搜过了没命中"
4. 要看内容：单条用 get_entry(form_token, serial_number)，
   整批用 list_entries(form_token, keyword) 翻页（matched 大于列出的 serial_numbers 时用它取剩下的）
```

### 关键格式规范

**entry payload 的键是 `api_code`，不是中文 label：**

| 字段类型 | 正确值格式 |
|----------|-----------|
| TextField / TextArea / NameField | 纯字符串 `"张三"` |
| MobileField | 纯字符串 `"13812345678"` |
| NumberField | 数字 `123` 或字符串 `"123"` |
| RadioButton / DropDown | 选项 api_code `"city_sh"`（不是 label "上海"） |
| CheckBox | api_code 数组 `["topic_a", "topic_b"]` |
| DateTimeField | ISO 字符串 `"2026-05-01 14:30"` |
| TableField | 对象数组 `[{"dim_api_code": value, ...}]` |

**list_entries filters operator 速查：**

| operator | 适用字段 | value 形式 |
|----------|----------|-----------|
| `eq` / `ne` | 所有 | 标量 |
| `gt` / `gte` / `lt` / `lte` | 数字、日期 | 标量 |
| `between` / `not_between` | 数字、日期 | `[min, max]`；矩阵 / 表格字段要指明列：`{"<dimension api_code>": [min, max]}` |
| `within_last` | 日期类（含 `created_at`） | `{"unit":"day"/"week"/"month","n":正整数}`，截至此刻往回数 |
| `any_in` / `none_in` | 文本、选项 | 数组 |
| `like` / `not_like` | 文本、选项 | 子串（**不带 % 通配符**） |
| `null` / `not_null` | 所有 | 省略 |

> 特殊字段：`created_at`（创建时间，配 `gte` / `between` / `within_last` 等）；`creator_id`（提交者用户 id，**只支持 `eq`**，value 是 entry 返回的 `creator_id` 字符串）——按提交者查数据用它，但聚合类工具不支持按它过滤。
>
> 字段名写错会被**拒**并列出该表单实际字段，不会静默返回 0 条。排序传 `sort=[{api_code, order}]`（`asc` / `desc`），不必再在对话侧倒序。

## Pitfalls

- **entry 键写成中文 label** → 服务端静默丢弃，报 "Entry attributes cannot be empty"；键必须是 `api_code`
- **选项字段传 label**（如 `"男"` / `"上海"`）→ 400 invalid choice；传 `choices[].api_code`
- **`is_put=true` 做部分更新** → 未提供字段全部清空；部分更新永远保持默认 `is_put=false`
- **`like` 带 SQL 通配符**（`"张%"` / `"%张%"`）→ 按字面匹配 `%`，永远查不到；直接传 `"张"`
- **`operator` 与字段类型不匹配** → 400，错误信息会列出该字段的可用 operator，照着改
- **简单字段包成对象**（`{"value": "张三"}`）→ 直接传字符串
- **TableField 按二维数组传** → 必须是对象数组，键是 dimension 的 `api_code`
- **批量新建数据循环调 `create_entry`** → 改用 `create_entries` 一次提交（≤200 条/批，超过自行分批）；它部分成功、按下标返回 `errors`、不幂等（重复调会生成重复数据）
- **批量更新循环调 `update_entry`** → 改用 `patch_entries`（一次 ≤200 行，每行 `{ serial_number, entry }`，PATCH 只改提供字段，单条聚合操作日志、按 serial_number 返回 `failed_rows`）；`delete_entry` 仍无批量版，逐条循环
- **测试号段**（`13800138000`）→ 号段正则校验 400 拒；用真实在用号段
- **删除整张表单** → MCP 不支持 `delete_form`，引导用户去后台手动操作
- **`ESignatureField` / `FormulaField` 写入 entry** → 服务端忽略，写入无效
- **改选项文案用 remove + add** → 会换 api_code，历史数据引用失效；改名用 `fields.update_choices.update`
- **选择字段设默认选中用 `predefined_value`** → 选择类字段（单选 / 多选 / 下拉 / 级联）不接受 `predefined_value`；默认选中改用 `choices[].selected: true`
- **字段显示规则 comparator 跟触发字段类型不匹配**（如选择字段用 `like`）→ 该 `edit_field_rules` 调用被拒；选择类用 `equal` / `none_in`、评分 / NPS 用 `between`、文本类用 `like` / `not_like`
- **还在用 edit_form 的 `field_rules` 改显示规则** → 该参数已移除、误传被拒；改用 `edit_field_rules` 做外科式 add / update / remove（按 `get_form(include_field_rules=true)` 或 `get_field_rules` 返回的 0-based `index` 定位），只动你传的那条、其余保留
- **给图片选项字段（ImageRadioButton / ImageCheckBox）`update_choices.add` 不带图片** → 被拒（image choice requires image_url / image_base64 / image_upload_token）；每个图片选项必须带图片，`value` 是文字标签必填
- **edit_form 改预约字段只改一项却不回传 `reservation_items[].api_code`** → reservation_items 是整体替换，丢了 api_code 会让历史预约数据失联；改动前先 get_form 读出各项 api_code 原样回传（省略时后端按 name 匹配保留，改名必须回传 api_code）
- **用 PageBreak 拼分页式 / 一页一题表单** → PageBreak 只在经典式内手动分页；整表分页式传 `layout:"card"`（仅 form / survey 场景生效，且不支持矩阵 / 表格 / 商品 / 签名等字段）
- **create_form 传 vote / customer_acquisition** → 已移除且会被拒（新编辑器打不开）；改用 `form` 场景
- **删字段 / 选项不先查数据** → 删有提交数据的字段 / 选项会永久清除数据且不可恢复；`fields.remove` / `update_choices.remove` 前先对每个目标用 `check_field_data` 查，`has_data=true` 时把影响告诉用户、确认后再删（edit_form 本身不拦截）
- **用 create_form 建考试/测评** → scene 枚举已移除 exam / evaluation；用 `create_exam_form` / `create_evaluation_form`
- **给考试设"每人限答 N 次"时自造 `times` 这种键** → `fill_frequency` 只认 `fill_type` / `condition` / `cycle_period` / `cycles_per_period` / `limited_time` / `limited_field_api_codes`；限一次用 `fill_type=once`（匿名考试配 `condition=by_device`），限 N 次用 `fill_type=repeatable` + `cycle_period` + `limited_time=N`；`condition=by_fields` 必须同时给 `limited_field_api_codes`，否则保存被拒。`custom_repeatable` / `by_fields` 是付费能力，账户不支持时限制存得下但不生效
- **套餐 / 额度不足的报错当成系统故障重试** → 这类失败（如 `edit_theme` 生成头图时 AI 点数不足）现在以工具错误返回，不是 500；把原文告诉用户并给替代方案（升套餐，或改用 `prepare_form_image_upload` 传本地图），不要重试
- **考试开限时又把题目设必填** → `show_timeout=true` 与题目字段 `required` 互斥；默认不开限时，仅用户明确要求时开
- **FormulaField 引用同一请求新增的字段** → 新字段还没有 api_code，公式里用 `<gd-field data-cid="...">` 引用其 `cid`，不要猜 api_code
- **编辑考试/测评题目时只传改动的 answers 项** → answers 是整体替换语义，会重建整个答案库；必须传完整列表
- **给选项设 `quota:0` 想表示"不限量"** → `0` 是"名额已满"，该选项会显示但置灰不可选；不限量就**省略 `quota`**，正整数才是名额上限
- **`import_entries_from_file` 后去轮询 / 重复调用 / 自己再逐行写数据** → 它是后台任务，调一次即返回；只需告诉用户"已开始、进度看数据页"然后停手。它报错 = 一行都没导入（校验在起任务前完成），读错误改参数、只重试一次
- **拿 `list_forms` / `get_form` / `edit_form` 去操作表格** → 表格是独立资源，用 `list_tables` / `get_table` / `edit_table`；`get_table` 对非表格资源直接报错
- **`create_table` 建空表不传 `with_default_entries`** → 空网格看着像坏了；暂时没数据进就传 `true` 补空行，紧接着要导数据就别开（免得真实数据落在空行下面）
- **把表格移进表单文件夹** → 表格只能进 `kind="table"` 的文件夹，先 `list_folders` 找；`move_table` 省略 `folder_token` 表示移回根目录
- **删预设视图或最后一个视图** → `delete_form_view` 拒绝；只能删自建且非最后一个的视图
- **`edit_form_view` 传 OR 分组的 filters** → MCP 只支持 AND 组合，OR 分组会被拍平成 AND（OR 需在网页端编辑）
- **让非表单管理员建 / 改对外查询页** → 被拒（只有该表单的管理员能操作 `create_opensearch_query` / `edit_opensearch_query`）
- **要统计却翻页拉全量明细自己算** → 数据量一大就慢、且漏页就算错；用 `count_entries` / `aggregate_entries` / `get_form_data_summary`，统计留在服务端
- **给 `aggregate_entries` / `get_form_data_summary` 传 `keyword`** → 这两个工具没有该参数（永远算整个过滤范围）；也别把带 `keyword` 的条数和不带的统计摆在一起讲，那是两批数据
- **拿多值字段（多选 / 级联 / 矩阵 / 地址 / 表格）当 `dimensions`** → 被拒（一条会落进多个组）；这类字段的分布用 `get_form_data_summary`
- **日期维度不传 `bucket`** → 每个存储值各成一组，出不来趋势；按 `day` / `week` / `month` 分桶
- **把分组结果当全量** → 分组按第一个指标降序、受 `limit` 截断（默认 20 / 上限 200）；看 `row_count` 和 `truncated`，别把一段说成全部
- **忽略维度值为 `null` 的那一组** → 那是"该字段没填"的条目，常常还是最大的一组，不是脏数据
- **聚合类工具里按 `creator_id` 过滤** → 被拒（它在查询引擎之外生效）；按提交者取数用 `list_entries`
- **为了找一个值先 `get_form` 再逐字段发 `like`** → 一次 `keyword` 就搜完该表单所有可搜字段；多张表单用 `search_entries_in_forms`
- **把 `search_entries_in_forms` 里带 `unavailable` 的表单汇报成"没命中"** → 那是**没搜成**（无权限 / 超 99999 条无 ClickHouse / 服务未响应），必须单独重试
- **超过 99999 条的表单用 `keyword`** → 需要 ClickHouse 支持，不可用时直接报错（不是返回空）；改用 `filters` 精确过滤
- **传了 `sort` 还把 `next` 当 serial_number 用** → 有 `sort` 时 `next` 是行偏移量；两种情况都只需把上一页的 `next` 原样回传
- **`fields` / `sort` / `filters` 里写不存在的 `api_code`** → 一律被拒并列出该表单实际字段；不会静默丢列或回落到默认排序
- **限流报错（HTTP 429 / code 14003）把原始 JSON 抛给用户** → 不友好；改为告知"接口请求频繁，请等 1–2 分钟后重试"，并放慢节奏、合并可批量的请求降低调用频次；不要立刻疯狂重试

## Verification

操作完成后确认：
- **创建/编辑表单**：返回中包含有效 `form_token`，可访问 `https://jinshuju.net/f/{form_token}`
- **create_entry**：返回包含 `serial_number`（整数）
- **create_entries**：返回 `created_count` 与提交条数一致，`errors` 为空（有部分失败时按下标核对原因）
- **update_entry**：返回的字段值与提交值一致
- **patch_entries**：返回 `updated_count` 与提交行数一致，`failed_rows` 为空（有部分失败时按 serial_number 核对 reason）
- **delete_entry**：后续 `get_entry` 返回 404 或条目不再出现在 `list_entries`
- **create_table / edit_table**：返回含 `token`，`get_table` 能读到刚建/改的字段
- **create_form_view / edit_form_view**：返回含视图 `token`，`list_form_view_entries` 能按其筛选取数
- **import_entries_from_file**：调用成功即代表任务已入队；不在本轮核对行数，让用户去数据页看进度
- **create_opensearch_query**：返回含 `url`（对外）与 `admin_url`（后台），访问 `url` 可打开查询页
- **aggregate_entries**：`columns` 与你传的 metrics / dimensions 顺序一一对应，分组时核对 `row_count` 与 `truncated` 再下结论
- **get_form_data_summary**：`overview.total_entries` 与同 filters 下的 `count_entries` 一致
- **批量操作**：向用户汇报"共 N 条，成功 X 条，失败 Y 条"

## MCP 配置

金数据 MCP 端点：`https://jinshuju.net/mcp`

**方式 A · HTTP Basic（API Key/Secret）**
```bash
echo -n "YOUR_API_KEY:YOUR_API_SECRET" | base64
```
```json
{
  "mcpServers": {
    "jinshuju": {
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
    "jinshuju": { "url": "https://jinshuju.net/mcp" }
  }
}
```

常见配置错误：漏 `/mcp` 后缀、用 `http://`、`Authorization` 缺 `Basic ` 前缀、用 `command/args`（stdio 写法，金数据是远程 HTTP MCP 不支持）。

### MCP 不可用时

工具未连接 / 授权失败 / 持续报错时，按顺序降级，**不要**用任何非标方式替代：

1. 告知用户"金数据 MCP 未就绪"，不要假装已完成操作。
2. 对照上面的「常见配置错误」引导排查（端点、`Basic ` 前缀、OAuth 授权等）。
3. 仍不行，就给出在金数据后台（jinshuju.net）手动操作的步骤指引。

> 超大表单（数十个字段）即使 MCP 正常，也建议先 `create_form` 建核心字段，再用 `edit_form` 分批补充，降低超长请求被截断 / 超时的风险。
