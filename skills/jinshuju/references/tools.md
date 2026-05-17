# 金数据 MCP 工具完整参考

本文档列出当前对外开放的 **18 个 MCP 工具**，每个工具包含一句话用途、输入参数、输出字段、所需 OAuth scope 和常见错误。

> 工具的实际暴露名可能带客户端前缀（如 `mcp__jinshuju__list_forms`），按客户端实际名字调用即可，本文统一用裸名。

## 索引

| 类别 | 工具 |
| ---- | ---- |
| **Forms** | [`list_forms`](#list_forms) · [`list_folders`](#list_folders) · [`get_form`](#get_form) · [`create_form`](#create_form) · [`copy_form`](#copy_form) · [`move_form`](#move_form) · [`edit_form`](#edit_form) · [`edit_theme`](#edit_theme) |
| **Entries** | [`list_entries`](#list_entries) · [`get_entry`](#get_entry) · [`create_entry`](#create_entry) · [`update_entry`](#update_entry) · [`delete_entry`](#delete_entry) |
| **Account** | [`get_current_user`](#get_current_user) · [`get_current_billing_account`](#get_current_billing_account) · [`list_account_users`](#list_account_users) |
| **Billing** | [`list_invoices`](#list_invoices) · [`list_payment_histories`](#list_payment_histories) |

## OAuth Scope 速查

| Scope | 涵盖工具 |
| ----- | -------- |
| `forms` | list_forms / list_folders / get_form / create_form / copy_form / move_form / edit_form |
| `form_setting` | edit_theme |
| `read_entries` | list_entries / get_entry |
| `write_entries` | create_entry / update_entry / delete_entry |
| `user` | get_current_user |
| `billing_account` | get_current_billing_account / list_account_users |
| `public` | list_invoices / list_payment_histories |

> Basic Auth / JWT 模式下不受 scope 限制；OAuth 模式下被授权的 scope 决定可调用工具集合，未授权 scope 调用会报 `Insufficient scope: <name> required`。

---

# Forms

## list_forms

**用途**：列出当前凭证名下能访问的表单（自己创建的 + 被分享协作的）。

**Scope**：`forms`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `name` | string | 否 | 表单名关键字（**正则匹配，大小写不敏感**），如 `"survey"` 能匹配 `Survey A` |
| `next` | string | 否 | 翻页游标（上一次响应里的 `next` 字段） |
| `limit` | integer | 否 | 默认 50；越界自动截断 |

**输出**

```json
{
  "total": 3,
  "count": 3,
  "data": [
    {
      "name": "2026 春季发布会报名表",
      "description": "活动报名收集",
      "token": "abCdEf",
      "scene": "registration",
      "created_at": "2026-04-20T10:00:00+08:00",
      "entries_count": 128
    }
  ],
  "next": null
}
```

**常见错误**

- `Insufficient scope: forms required` — OAuth 未授权 `forms` scope

---

## list_folders

**用途**：列出当前用户能管理的文件夹，**只为给 create_form / copy_form / move_form 拿 folder_token 用**。

**Scope**：`forms`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `limit` | integer | 否 | 默认 50，最大 100，越界自动截断 |

**输出**

```json
{
  "total": 4,
  "returned": 4,
  "data": [
    { "token": "FLD_a1b2", "name": "市场活动" },
    { "token": "FLD_c3d4", "name": "客户登记" }
  ]
}
```

> 别人的文件夹不会出现在结果里。返回字段没有 `id`，**只用 token**。

**常见错误**

- `Insufficient scope: forms required`

---

## get_form

**用途**：拿表单完整结构（字段 / 主题 / setting）。**调任何 entry 类工具前必先 get_form** 拿 `api_code`。

**Scope**：`forms`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `token` | string | ✅ | 表单 token **或** form id（数字 ID 也接受） |

**输出**

```json
{
  "name": "2026 春季发布会报名表",
  "token": "abCdEf",
  "description": "活动报名",
  "fields": [
    {
      "api_code": "field_1",
      "label": "姓名",
      "type": "NameField",
      "required": true,
      "private": false
    },
    {
      "api_code": "field_2",
      "label": "参会城市",
      "type": "DropDown",
      "required": true,
      "private": false,
      "choices": [
        { "value": "北京", "api_code": "city_bj" },
        { "value": "上海", "api_code": "city_sh" }
      ]
    },
    {
      "api_code": "field_3",
      "label": "评分",
      "type": "RatingField",
      "rating_max": 5
    },
    {
      "api_code": "field_4",
      "label": "费用明细",
      "type": "TableField",
      "init_row_length": 3,
      "dimensions": [
        { "api_code": "col_1", "label": "项目", "type": "TextField" },
        { "api_code": "col_2", "label": "金额", "type": "NumberField" }
      ]
    }
  ],
  "theme": {
    "primary_color": "#3B82F6",
    "header": { "type": "image", "has_header_image": true }
  },
  "setting": {
    "entry_submit_mode": "show_message",
    "success_message": "感谢报名！",
    "success_message_style": "text",
    "open_entry_action": "view",
    "show_serial_number_on_success": true,
    "manually_close_rule": null,
    "by_time_range_close_rule": { "start_time": "2026-05-01T09:00+08:00", "end_time": "2026-05-31T18:00+08:00" },
    "by_entries_close_rule": { "limit": 500 },
    "fill_frequency": { "fill_type": "repeatable", "condition": "by_ip", "cycle_period": "every_day", "limited_time": 3 },
    "password_required": false,
    "allowed_audience": "public",
    "notification_rules": [
      { "id": "...", "approach": "WXWORK", "url": "https://qyapi.weixin.qq.com/...", "content": "新报名：$(field_1)", "trigger_scope": "all_new", "enabled": true, "from_next": true }
    ]
  }
}
```

> 字段特有属性（如 `goods_items` / `reservation_items` / `associated_form_token` / `predefined_value` / `placeholder` / `range_min/max` / `precision` / `media_type` / `max_size` 等）按字段类型出现在对应 field 节点上。

**常见错误**

- `Form cannot be found` — token 错 / 表单不属于当前账号 / 没被分享
- `Insufficient scope: forms required`

---

## create_form

**用途**：从零创建一张表单。一次性指定 name + 字段列表 + 可选 setting + 可选 folder。

**Scope**：`forms`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `name` | string | ✅ | 表单名 |
| `fields` | array  | ✅ | 字段列表，每项见下表 |
| `description` | string | 否 | 表单说明 |
| `setting` | object | 否 | 初次创建的关键 setting（仅 `success_message` / `open_entry_action` / `open_entry_message` / `notification_rules`）。完整 setting 用 `edit_form` 配 |
| `folder_token` | string | 否 | 表单要放进的文件夹 token |

**fields[] 通用属性**

| 字段 | 类型 | 说明 |
| ---- | ---- | ---- |
| `type` | string | 字段类型，必须是 [39 种白名单](#字段类型白名单) 之一 |
| `label` | string | 字段标签 |
| `required` | bool | 是否必填，与 `private` 互斥 |
| `private` | bool | 是否隐藏，设 true 时 `required` 自动置 false |
| `notes` | string | 字段提示文案（SectionBreak 时是描述正文） |
| `choices` | array | 选项字段用：`[{ value, quota?, image_url?, sub_choices? }]` |
| `statements` | array | 矩阵类用：`[{ label }]` |
| `dimensions` | array | TableField / MatrixField 用 |
| `rating_max` | int | RatingField / MatrixScaleField 用，3/5/10 |
| `predefined_value` | string / object | 默认值，类型见对应字段说明 |
| `placeholder` | string | 占位文本 |
| `range_min` / `range_max` | number | NumberField 取值范围 |
| `precision` | int / string | NumberField (0-14) 或 DateTimeField (`year`/`month`/`day`/`hour`/`minute`/`second`) |

> 不同字段类型还有专属属性（`max_size` / `media_type` / `goods_items` / `reservation_items` / `formula_display` / `associated_form_token` 等），全部见 [字段类型清单](#字段类型白名单)。

**setting 子参数**（创建阶段只接受这几个，更多设置走 edit_form）

| 字段 | 类型 | 说明 |
| ---- | ---- | ---- |
| `success_message` | string | 提交成功提示文案 |
| `open_entry_action` | enum | `hide` / `view` / `edit`，默认 `view` |
| `open_entry_message` | string | 已填过表单的提示文案（默认 `你已填写过该表单`） |
| `notification_rules` | array | 通知规则数组，见 [edit_form](#edit_form) 同名参数 |

**输出**

```json
{
  "name": "2026 春季发布会报名表",
  "token": "abCdEf",
  "description": "活动报名",
  "form_url": "https://jinshuju.net/f/abCdEf",
  "fields_count": 7,
  "created_at": "2026-05-17T10:00:00+08:00"
}
```

**调用示例（活动报名表）**

```json
{
  "name": "2026 春季发布会报名表",
  "description": "公司春季发布活动登记",
  "fields": [
    { "type": "NameField", "label": "姓名", "required": true },
    { "type": "MobileField", "label": "手机号", "required": true, "sms_verification": true },
    { "type": "TextField", "label": "公司" },
    { "type": "TextField", "label": "职位" },
    {
      "type": "DropDown", "label": "参会城市", "required": true,
      "choices": [{ "value": "北京" }, { "value": "上海" }, { "value": "深圳" }, { "value": "线上" }]
    },
    {
      "type": "CheckBox", "label": "感兴趣议题",
      "choices": [{ "value": "产品发布" }, { "value": "技术架构" }, { "value": "客户案例" }]
    },
    { "type": "TextArea", "label": "备注" }
  ],
  "setting": {
    "success_message": "感谢报名！我们将于活动前一周发送参会指引"
  },
  "folder_token": "FLD_a1b2"
}
```

**常见错误**

- `Name cannot be empty`
- `Fields cannot be empty`
- `Invalid field type: <Type>` — 字段类型不在白名单
- `Folder not accessible` — folder_token 不属于当前用户
- `Insufficient scope: forms required`

### 字段类型白名单

**基础（19）**：`TextField` `TextArea` `NumberField` `EmailField` `MobileField` `TelephoneField` `IdCardField` `NameField` `AddressField` `LinkField` `GeoField` `AttachmentField` `DateTimeField` `TimeField` `RatingField` `NpsField` `RadioButton` `CheckBox` `DropDown`

**进阶（14）**：`TableField` `CascadeDropDown` `SortField` `LikertField` `MatrixField` `MatrixScaleField` `ImageRadioButton` `ImageCheckBox` `GoodsField` `FormulaField` `ReservationField` `FormAssociation` `ESignatureField` `AudioField`

**装饰 / 控件（6）**：`SectionBreak`（描述字段）`PageBreak` `WidgetButton` `WidgetContact` `WidgetMap` `WidgetMarquee`

**复杂字段示例片段**

```json
{
  "type": "GoodsField", "label": "选购", "unit": "件",
  "goods_items": [
    { "layout": "without_images", "name": "黑色 T 恤", "price": 99, "inventory": 50 },
    { "layout": "images", "name": "彩色 T 恤", "price": 99, "image_urls": ["https://cdn.example.com/tshirt.jpg"] },
    {
      "layout": "price_only", "name": "爱心捐款",
      "dimensions": [{ "label": "金额", "options": [{ "label": "100" }, { "label": "500" }, { "label": "自定义", "value": "customized" }] }],
      "skus": [
        { "specification": { "金额": "100" }, "price": 100 },
        { "specification": { "金额": "500" }, "price": 500 },
        { "specification": { "金额": "customized" }, "price": 0.01 }
      ]
    }
  ]
}
```

```json
{
  "type": "ReservationField", "label": "预约场次",
  "reservation_items": [{
    "name": "诊室 A",
    "quota_setting": {
      "type": "by_time_range_repeat_daily",
      "available_days_of_week": ["monday", "tuesday", "wednesday", "thursday", "friday"],
      "time_range_mode": "same_by_wday",
      "show_left_quota": true,
      "daily_time_range_quotas": [
        { "quota": 5, "start_time": { "hour": 9, "minute": 0 }, "end_time": { "hour": 12, "minute": 0 } },
        { "quota": 5, "start_time": { "hour": 14, "minute": 0 }, "end_time": { "hour": 17, "minute": 0 } }
      ]
    }
  }]
}
```

```json
{
  "type": "FormulaField", "label": "总价",
  "formula_display": "<gd-field data-api-code=\"field_2\"></gd-field> * <gd-field data-api-code=\"field_3\"></gd-field>",
  "result_display_type": "numeric",
  "precision": 2,
  "icon_type": "cny1",
  "thousands_separator": true
}
```

```json
{
  "type": "FormAssociation", "label": "关联客户", "required": true,
  "associated_form_token": "MASTER_TOKEN",
  "associated_field_api_codes": ["field_1"],
  "display_field_api_codes": ["field_2", "field_3"]
}
```

```json
{
  "type": "SectionBreak", "label": "活动说明",
  "notes": "请仔细阅读以下规则……",
  "show_split_line": true,
  "show_part_description": true
}
```

---

## copy_form

**用途**：基于已有表单创建新表单（继承字段、主题、setting）。

**Scope**：`forms`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `form_token` | string | ✅ | 源表单 token |
| `name` | string | 否 | 新表单名，默认 `"Copy of <原名>"` |
| `folder_token` | string | 否 | 新表单要放进的文件夹 token |

**输出**

```json
{
  "name": "2026 年会报名表",
  "token": "newToken",
  "description": "...",
  "form_url": "https://jinshuju.net/f/newToken",
  "fields_count": 8,
  "created_at": "2026-05-17T10:00:00+08:00"
}
```

**常见错误**

- `Form cannot be found` — 源表单 token 错
- `Folder not accessible` — folder_token 不属于当前用户
- `Failed to copy form: ...`

---

## move_form

**用途**：把表单移到指定文件夹，或移回根目录。

**Scope**：`forms`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `form_token` | string | ✅ | 要移动的表单 token |
| `folder_token` | string | 否 | 目标文件夹 token；**省略或传 `""` = 移出文件夹回到根目录** |

**输出**

```json
{ "form_token": "abCdEf", "folder_token": "FLD_a1b2" }
```

移出文件夹时 `folder_token` 为 `null`：

```json
{ "form_token": "abCdEf", "folder_token": null }
```

**常见错误**

- `Form cannot be found`
- `Folder not accessible` — 文件夹不存在或不属于当前用户

---

## edit_form

**用途**：原子化地更新表单——可一次性改 name / description / setting / fields（字段增删改、选项增删改名）。

**Scope**：`forms`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `form_token` | string | ✅ | |
| `name` | string | 否 | 新表单名 |
| `description` | string | 否 | 新表单说明 |
| `setting` | object | 否 | 见下"setting 全字段表"；**只传要改的 key，其他保持原值** |
| `fields` | object | 否 | `{ add[], remove[], update[], update_choices[] }` 四种操作，原子化执行 |

**必须至少传一个 edit 操作，否则报 `No edit operations specified`。**

### setting 全字段表

| 字段 | 类型 | 说明 |
| ---- | ---- | ---- |
| `entry_submit_mode` | enum | 提交后行为 `show_message` / `redirect` / `reports` / `exam_score`；填了 `success_redirect_url` 时强制改为 `redirect` |
| `success_message` | string | 文本成功页文案 |
| `success_message_rich_text` | string | HTML 富文本成功页（需套餐支持） |
| `success_message_style` | enum | `text` / `rich_text`；只传一个 message 字段时自动设置 |
| `success_redirect_url` | string | 跳转 URL |
| `success_redirect_fields` | string[] | 跳转 URL 上拼接哪些字段的 api_code |
| `open_entry_action` | enum | `hide` / `view` / `edit`（edit 需 submitter_edit_open_entry 套餐能力） |
| `open_entry_message` | string | 已填过表单的提示语 |
| `open_entry_cancel_reservation` | bool | 预约场景：edit 时是否显示"取消预约"按钮 |
| `show_serial_number_on_success` | bool | 成功页是否显示流水号 |
| `show_submit_again` | bool | 成功页是否显示"再次提交" |
| `manually_close_rule` | object | `{ closed: bool }`，写后清除其他 close rules |
| `by_time_range_close_rule` | object | `{ start_time, end_time }` ISO 8601 |
| `by_entries_close_rule` | object | `{ limit: int }` |
| `show_close_count_down` | bool | 显示截止倒计时；只在有时间 close rule 时生效，否则静默被重置成 false |
| `show_form_before_open` | bool | 开放前是否预览表单；同上 |
| `fill_frequency` | object | `{ fill_type, condition, cycle_period, cycles_per_period, limited_time, limited_field_api_codes }` |
| `password_required` | bool | 启用访问密码闸；开启时必须同时给 `access_password` |
| `access_password` | string | 访问密码 |
| `allowed_audience` | enum | `public` / `internal` / `private` / `gd_user_only` / `weixin_followers_only` / `weixin_qiye_followers_only` |
| `notification_rules` | array | 通知规则数组，见下 |

**notification_rules** —— **替换语义**：传该 key 会重建所有 MCP 管理的规则（即 `from_next=true` 的）；传 `[]` 清空 MCP 规则；4.0 桌面的规则（`from_next=false`）不会被动。

```json
[
  {
    "approach": "WXWORK",
    "url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...",
    "content": "新报名：$(field_1) - $(field_2)",
    "trigger_scope": "all_new",
    "mentioned_mobile_list": ["13812345678", "@all"],
    "enabled": true
  },
  {
    "approach": "DING_TALK",
    "url": "https://oapi.dingtalk.com/robot/send?access_token=...",
    "content": "新订单：$(field_3) 元",
    "trigger_scope": "all_new"
  },
  {
    "approach": "WEBHOOK",
    "url": "https://my.server/jinshuju-hook",
    "content": "{\"name\":\"$(field_1)\",\"mobile\":\"$(field_2)\"}",
    "trigger_scope": "all_new"
  }
]
```

`approach` 必须是 `WXWORK` / `DING_TALK` / `WEBHOOK` 之一；`trigger_scope` 取值：`all_new` / `all_update` / `matched_new` / `matched_update` / `all` / `schedule_time`。

### fields 四种操作

#### `fields.add: []`

形态与 `create_form.fields[]` 完全一致，可额外指定 `position`（0-based 插入位置，省略则追加到末尾）。

```json
{
  "fields": {
    "add": [
      { "type": "NumberField", "label": "年龄", "range_min": 18, "range_max": 100, "position": 2 },
      { "type": "AttachmentField", "label": "简历", "max_size": 8, "max_file_quantity": 2 }
    ]
  }
}
```

#### `fields.remove: ["api_code", ...]`

只传 api_code 列表；**不接受 label**。

```json
{ "fields": { "remove": ["field_5", "field_7"] } }
```

#### `fields.update: []`

每项必须有 `api_code`，可修改 label / required / private / notes / 类型专属属性。**改 TableField / MatrixField 的 dimensions / statements 时必须带 dimension/statement 的 api_code**，否则旧数据引用会失效。

```json
{
  "fields": {
    "update": [
      { "api_code": "field_1", "label": "全名", "required": true },
      { "api_code": "field_3", "notes": "请填整数" },
      { "api_code": "field_8", "media_type": { "type": "custom", "value": ["pdf", "docx"] }, "max_size": 10 }
    ]
  }
}
```

#### `fields.update_choices: []`

选项字段的增删改名。**改文案永远用 `update`（保留 api_code）**，不要用 `remove` + `add`，否则历史数据引用失效。

```json
{
  "fields": {
    "update_choices": [
      {
        "field_api_code": "field_status",
        "add": [{ "value": "已签约", "quota": 100 }],
        "remove": [{ "api_code": "status_obsolete" }],
        "update": [{ "api_code": "status_contacted", "value": "已联系过" }]
      }
    ]
  }
}
```

### 输出

```json
{
  "name": "2026 春季发布会报名表",
  "token": "abCdEf",
  "fields_count": 9,
  "form_url": "https://jinshuju.net/f/abCdEf",
  "updated_at": "2026-05-17T11:30:00+08:00"
}
```

**常见错误**

- `Form cannot be found`
- `No edit operations specified` — 一个操作都没传
- `Invalid field type: <Type>`
- `Failed to update form: <validation messages>`
- `Insufficient scope: forms required`

---

## edit_theme

**用途**：编辑表单视觉主题——颜色、背景、**头图**（外链 / Base64 / **AI 生成**）、字体、容器样式、提交按钮。

**Scope**：`form_setting`（⚠️ 独立 scope，不是 `forms`）

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `form_token` | string | ✅ | |
| `primary_color` | string | 否 | 主色 hex，如 `"#FF5733"` |
| `secondary_color` | string | 否 | 副色 hex |
| `wallpaper` | object | 否 | `{ background_color, background_image_attachment_id }`（id 传 `""` 移除） |
| `header` | object | 否 | 见下 |
| `typography` | object | 否 | `{ form_header, field_label, choice_style }`，每项 `{ font_size, font_weight, color, text_align }` |
| `form_container` | object | 否 | `{ background_color }` |
| `submit_button` | object | 否 | `{ background_color, color, font_size }` |
| `generate_header_image` | object | 否 | `{ prompt?: string }`，让 AI 生成头图；省略 prompt 时按表单名+描述自动推断 |

**header 对象**

| 字段 | 类型 | 说明 |
| ---- | ---- | ---- |
| `type` | enum | `none` / `text` / `image` |
| `text` | string | 头图区文字（type=text 时） |
| `text_style` | object | `{ font_size, font_weight, color, text_align }` |
| `background_color` | string | 头部背景色 |
| `header_image_url` | string | **首选**：外链图片 URL，服务端下载创建附件 |
| `header_image_base64` | string | Base64 图片数据（⚠️ LLM 易截断，能不用就不用） |

**至少传一个改动操作，否则报 `No theme edit operations specified`。**

**输出**

```json
{
  "form_token": "abCdEf",
  "primary_color": "#3B82F6",
  "secondary_color": "#93C5FD",
  "wallpaper": { "background_color": "#FFFBEB" },
  "header": {
    "type": "image",
    "has_header_image": true,
    "background_color": "#FEF3C7"
  },
  "typography": {
    "form_header": { "font-size": "24px", "font-weight": "bold", "color": "#1F2937", "text-align": "center" },
    "field_label": { "font-size": "14px", "color": "#374151" },
    "choice_style": { "color": "#4B5563" }
  },
  "form_container": { "background_color": "#FFFFFF" },
  "submit_button": { "background_color": "#3B82F6", "color": "#FFFFFF", "font_size": "16px" }
}
```

**调用示例**

```json
{
  "form_token": "abCdEf",
  "primary_color": "#1E40AF",
  "generate_header_image": { "prompt": "蓝紫色科技感主题，适合发布会报名表的横幅头图" }
}
```

**常见错误**

- `Insufficient scope: form_setting required` — OAuth 授权时**没勾上 form_setting**（用户最常见的坑：以为 `forms` scope 就够，结果调 edit_theme 被拒）
- `Form cannot be found`
- `No theme edit operations specified`
- `Failed to update theme: <validation messages>`

---

# Entries

## list_entries

**用途**：分页列出表单的数据条目，支持复杂字段过滤（filters）。

**Scope**：`read_entries`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `form_token` | string | ✅ | 表单 token 或 form id |
| `next` | integer | 否 | 翻页游标（上次响应里的 `next`，即 `serial_number`） |
| `created_at` | string | 否 | ISO 8601 字符串，"创建时间 >= 此刻"的简单单边过滤（等价于 `filters=[{field:"created_at", operator:"gte", value:...}]`） |
| `filters` | array / string | 否 | 字段值条件数组，AND 组合；也可传 JSON 字符串 |

### filters 完整说明

每个元素 `{ field, operator, value }`：

| 类别 | operator | value 形式 | 示例 |
| ---- | -------- | ---------- | ---- |
| 等值 | `eq` / `ne` | 标量 | `{"field":"field_1","operator":"eq","value":"张三"}` |
| 比较 | `gt` / `gte` / `lt` / `lte` | 标量 | `{"field":"field_3","operator":"gte","value":6}` |
| 区间 | `between` / `not_between` | `[min, max]` 闭区间 | `{"field":"field_3","operator":"between","value":[80,100]}` |
| 集合 | `any_in` / `none_in` | 数组 | `{"field":"field_2","operator":"any_in","value":["city_bj","city_sh"]}` |
| 文本子串 | `like` / `not_like` | 子串字符串（不区分大小写，**不接受 SQL 通配符**） | `{"field":"field_2","operator":"like","value":"张"}` |
| 是否为空 | `null` / `not_null` | 省略 | `{"field":"field_4","operator":"not_null"}` |

**关键约束**：

1. **选项字段的 value 传 `choices[].api_code`**（如 `city_sh`），不是 label（`"上海"`）
2. `created_at` 是合法字段，可与 `gte` / `between` 等数值 operator 组合
3. **filters 中含 `created_at` 时，结果按 `created_at` 升序**；否则按 `serial_number` 升序
4. **不支持任意字段排序**——倒序 / 取前 N 在本地处理
5. operator 跟字段类型不匹配会被服务端拒，并列出该字段允许的 operator——直接照着改

operator × 字段类型兼容矩阵：

| 字段类型 | 可用 operator |
| -------- | ------------- |
| 文本类（Text / TextArea / Name / Email / Mobile / Telephone / IdCard / Link） | `eq` `ne` `any_in` `none_in` `null` `not_null` `like` `not_like` |
| `NumberField` | `eq` `ne` `null` `not_null` `gte` `gt` `lte` `lt` `between` `not_between` |
| `DateTimeField` / `created_at` | `eq` `ne` `null` `not_null` `like` `gte` `gt` `lte` `lt` `between` `not_between` |
| `RatingField` / `NpsField` | `eq` `ne` `null` `not_null` `gte` `gt` `lte` `lt` |
| `RadioButton` / `CheckBox` / `DropDown` | `eq` `ne` `any_in` `none_in` `null` `not_null` `like` `not_like` |
| `FormAssociation` | `eq` `ne` `any_in` `none_in` `null` `not_null` |
| `AttachmentField` / `GeoField` / `TableField` | `null` `not_null` `like` |
| `ESignatureField` | `null` `not_null` |

### 输出

```json
{
  "total": 128,
  "count": 50,
  "data": [
    {
      "serial_number": 1,
      "token": "ENTRY_TOKEN_1",
      "creator_name": "张三",
      "created_at": "2026-04-20T10:00:00+08:00",
      "field_1": "张三",
      "field_2": "13812345678",
      "field_3": "city_sh",
      "field_4": ["topic_product", "topic_tech"]
    }
  ],
  "next": 51
}
```

> **单次最多 50 条**。需要更多用 `next` 翻页（值是 `serial_number`）。

**调用示例**

```json
{
  "form_token": "abCdEf",
  "filters": [
    { "field": "field_3", "operator": "eq", "value": "city_sh" },
    { "field": "field_2", "operator": "like", "value": "138" },
    { "field": "created_at", "operator": "gte", "value": "2026-05-01 00:00:00" }
  ]
}
```

**常见错误**

- `Insufficient scope: read_entries required`
- `Form cannot be found`
- 400 错配：`Operator 'gte' not supported for field 'field_1' (NameField). Allowed operators: eq, ne, any_in, none_in, null, not_null, like, not_like.`

---

## get_entry

**用途**：拿单条 entry 的完整字段值。

**Scope**：`read_entries`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `form_token` | string | ✅ | 表单 token 或 form id |
| `serial_number` | integer | ✅ | 条目流水号（表单内自增） |

**输出**

```json
{
  "serial_number": 12,
  "token": "ENTRY_TOKEN_12",
  "creator_name": "张三",
  "created_at": "2026-05-15T14:30:00+08:00",
  "field_1": "张三",
  "field_2": "13812345678",
  "field_3": "city_sh",
  "field_4": ["topic_product"]
}
```

**常见错误**

- `Form cannot be found`
- `Entry cannot be found` — serial_number 不存在
- `Insufficient scope: read_entries required`

---

## create_entry

**用途**：给指定表单新增一条数据。

**Scope**：`write_entries`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `form_token` | string | ✅ | |
| `entry` | object | ✅ | `{ api_code: value }` 形式的字段值；未知 key 静默过滤 |

**字段值规范（重点）**

- **key 必须是 `api_code`**（如 `field_1`、`field_mobile`），不是中文 label
- **选项字段的 value 传选项 `api_code`**（如 `code_male` / `city_sh`），不是 label
- 简单字段（`TextField` / `NumberField` / `MobileField` / `NameField` / `IdCardField` / `EmailField`）传**纯字符串或数字**，不要包对象
- `TableField`：对象数组，每行是 `{ dimension_api_code: value }`
- `AddressField`：`{ province, city, district, street }`
- `MultipleChoice`：api_code 数组
- 写入会被忽略：`ESignatureField` / `FormulaField`（在 `NOT_SUPPORT_UPDATE_FIELDS` 黑名单内）
- 写入受限：`AttachmentField` 需要 attachment_id，MCP 无文件上传通道
- `MobileField` 号段正则仍然跑——保留测试号段如 `13800138000` 会被 400 拒；MCP 路径下跳过短信验证码

**输出**

```json
{
  "serial_number": 129,
  "token": "ENTRY_TOKEN_129",
  "creator_name": "<API 调用方名称>",
  "created_at": "2026-05-17T12:00:00+08:00",
  "field_1": "张三",
  "field_2": "13812345678",
  "field_3": "city_sh"
}
```

**调用示例**

```json
{
  "form_token": "abCdEf",
  "entry": {
    "field_1": "张三",
    "field_2": "13812345678",
    "field_3": "city_sh",
    "field_4": ["topic_product", "topic_tech"]
  }
}
```

**常见错误**

- `Form cannot be found`
- `Entry attributes cannot be empty` — `entry` 是 `{}` 或全是未知 key
- `Form has reached entries limit` — 表单达条目上限
- 字段 validation 错误（required 缺失 / Email 格式 / Choice 无效值 / Mobile 号段 等）— 错误信息含 `<字段>` + 具体原因
- `Insufficient scope: write_entries required`

---

## update_entry

**用途**：更新单条 entry。**只支持单条**，批量要逐条循环调用。

**Scope**：`write_entries`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `form_token` | string | ✅ | |
| `serial_number` | integer | ✅ | 目标 entry 的流水号 |
| `entry` | object | ✅ | `{ api_code: value }`，未知 key 静默过滤 |
| `is_put` | bool | 否 | 默认 `false`（PATCH，只改提供的字段）；`true` = PUT 全替换 |

⚠️ **`is_put=true` 危险**：PUT 会把未提供的字段**全部清空**。做"只改某字段"的部分更新永远保持默认 `false`。只有用户明确说"整条覆盖"且已列全所有字段值时才允许 PUT。

**输出**

```json
{
  "serial_number": 12,
  "token": "ENTRY_TOKEN_12",
  "field_1": "李四",
  "field_2": "13812345678",
  "field_3": "city_bj"
}
```

**调用示例（PATCH 改单字段）**

```json
{
  "form_token": "abCdEf",
  "serial_number": 12,
  "entry": { "field_status": "status_contacted" },
  "is_put": false
}
```

**常见错误**

- `Form cannot be found`
- `Entry cannot be found`
- `Entry attributes cannot be empty`
- 字段 validation 错误
- `Insufficient scope: write_entries required`

---

## delete_entry

**用途**：删除单条 entry。**只支持单条**，批量逐条循环；删除前必须二次确认。

**Scope**：`write_entries`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `form_token` | string | ✅ | |
| `serial_number` | integer | ✅ | |

**输出**

```json
{ "serial_number": 12 }
```

**常见错误**

- `Form cannot be found`
- `Entry cannot be found`
- `Failed to delete the entry, try later` — 底层 delete 失败
- `Insufficient scope: write_entries required`

---

# Account

## get_current_user

**用途**：拿当前凭证对应的用户信息。回答"我是谁 / 我属于哪个企业 / 我啥角色"时优先调。

**Scope**：`user`

**输入**：无参数

**输出**

```json
{
  "id": "abc123",
  "name": "张三",
  "email": "zhangsan@example.com",
  "mobile": "13812345678",
  "role": "owner",
  "billing_account_id": "ba_xxx",
  "created_at": "2024-01-15T10:00:00Z"
}
```

`role` 取值：`owner` / `admin` / `worker` / `outworker`。

**常见错误**

- `User cannot be found`
- `Insufficient scope: user required`

---

## get_current_billing_account

**用途**：拿当前用户所属企业账户的套餐 / 用量 / 试用信息。回答"我什么套餐 / 还剩多少额度 / 什么时候到期"时优先调。

**Scope**：`billing_account`

**输入**：无参数

**输出**

```json
{
  "id": "ba_xxx",
  "name": "示例公司",
  "subdomain": "demo",
  "users_count": 12,
  "plan": {
    "code": "professional",
    "name": "专业版",
    "end_date": "2026-12-31",
    "expired": false,
    "org_plan": false
  },
  "feature_trial": {
    "in_use": false,
    "expired": false,
    "end_date": null
  },
  "usage": {
    "sms": { "total_quota": 1000, "total_balance": 800, "month_balance": 200, "consumed_quota": 200 },
    "active_mail": { "total_quota": 500, "total_balance": 450, "month_balance": 50, "consumed_quota": 50 },
    "entry_quota": { "total_quota": 50000, "total_balance": 45000, "month_balance": 2000, "consumed_quota": 5000 },
    "storage_quota": { "total_quota": 10240, "total_balance": 8000, "month_balance": 1000, "consumed_quota": 2240 }
  }
}
```

**常见错误**

- `User cannot be found`
- `Billing account cannot be found`
- `Insufficient scope: billing_account required`

---

## list_account_users

**用途**：列出当前企业账户的所有成员。主要用于"把表单协作给某团队成员"前先找到对方 id。

**Scope**：`billing_account`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `limit` | integer | 否 | 默认 50，最大 100 |

**输出**

```json
{
  "count": 12,
  "data": [
    { "id": "u_xxx", "name": "张三", "email": "zhangsan@example.com", "mobile": "13812345678", "role": "owner", "status": "active" },
    { "id": "u_yyy", "name": "李四", "email": "lisi@example.com",     "mobile": "13898765432", "role": "worker", "status": "active" }
  ]
}
```

> ⚠️ **MCP 暂未提供 add_cooperator / share_form 类协作工具**。拿到成员 id 后实际分享操作要去后台 web 端完成。

**常见错误**

- `User cannot be found`
- `Billing account cannot be found`
- `Insufficient scope: billing_account required`

---

# Billing

## list_invoices

**用途**：列出当前账号的电子发票和未开票金额。

**Scope**：`public`

**输入**：无参数

**输出**

```json
{
  "invoices": {
    "count": 3,
    "records": [
      {
        "created_at": "2026-03-15T10:00:00+08:00",
        "amount": 1000.0,
        "organization": "示例公司",
        "dedicated_invoice": true
      }
    ]
  },
  "uninvoiced_amount": {
    "total": 500.0,
    "transaction_count": 2
  }
}
```

**常见错误**

- `Billing account not found`
- `Insufficient scope: public required`

---

## list_payment_histories

**用途**：列出充值/扣费历史。支持日期范围、交易类型筛选、可选附带当前余额。

**Scope**：`public`

**输入**

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `start_date` | string | 否 | `YYYY-MM-DD` |
| `end_date` | string | 否 | `YYYY-MM-DD` |
| `verb` | string | 否 | 交易类型过滤（如 `sms_charge` / `ai_points_charge`） |
| `limit` | integer | 否 | 默认 50，最大 1000 |
| `include_balance` | bool | 否 | 默认 false；true 时附带 `current_balance` |

**输出**

```json
{
  "payment_history": {
    "total_records": 23,
    "returned_records": 23,
    "records": [
      {
        "id": "ph_xxx",
        "created_at": "2026-05-10T14:00:00+08:00",
        "verb": "sms_charge",
        "description": "短信扣费",
        "amount": -10.0,
        "balance": 990.0
      }
    ]
  },
  "statistics": {
    "total_consumption": 230.0,
    "total_recharge": 1000.0,
    "verb_distribution": {
      "sms_charge": { "count": 20, "amount": -200.0 },
      "ai_points_charge": { "count": 3, "amount": -30.0 }
    }
  },
  "current_balance": {
    "amount": 770.0,
    "entry_quota": 45000
  }
}
```

`current_balance` 仅在请求时传了 `include_balance: true` 才出现。

**常见错误**

- `Billing account not found`
- `Insufficient scope: public required`

---

# 通用规则

## 鉴权方式

金数据 MCP 支持三种鉴权（同一端点 `https://jinshuju.net/mcp`）：

1. **HTTP Basic** —— `Authorization: Basic <base64(api_key:api_secret)>`。Scope 不受限（等价于全开）
2. **JWT** —— `Authorization: Bearer <jwt_token>`。Scope 不受限
3. **OAuth 2.0** —— `Authorization: Bearer <access_token>`。**Scope 按授权范围生效**，未授权 scope 调用会被拒

OAuth metadata 端点：
- `https://jinshuju.net/.well-known/oauth-protected-resource`
- `https://jinshuju.net/.well-known/oauth-authorization-server`

## 错误返回结构

工具失败时抛 `StandardError`，消息会回流给 AI 客户端，常见前缀：

- `Insufficient scope: <scope> required` — OAuth scope 不够
- `Form cannot be found` — 表单不存在 / 无权访问
- `Entry cannot be found` — 条目不存在
- `Folder not accessible` — 文件夹不存在 / 无权管理
- `No edit operations specified` — edit_form / edit_theme 一个操作都没传
- `Invalid field type: <X>` — 不在白名单
- `Entry attributes cannot be empty` — entry 是 `{}` 或全是未知 key
- `Form has reached entries limit` — 表单达条目上限
- `Failed to <action>: <validation messages>` — 底层 service save 失败，含详细 errors
