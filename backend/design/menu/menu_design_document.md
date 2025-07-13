# 动态菜单系统设计文档

## 1. 数据库设计

### 1.1 新增表结构

菜单项表 (menu_items)

| 字段名     | 类型        | 是否为空 | 默认值   | 说明     |
| ---------- | ----------- | -------- | -------- | -------- |
| id         | Integer     | 否       | -        | 主键     |
| title      | String(50)  | 否       | -        | 菜单标题 |
| icon       | String(30)  | 是       | NULL     | 菜单图标 |
| route      | String(100) | 是       | NULL     | 路由路径 |
| parent_id  | Integer     | 是       | NULL     | 父菜单ID |
| order      | Integer     | 否       | 0        | 排序权重 |
| is_active  | Boolean     | 否       | True     | 是否激活 |
| created_at | DateTime    | 否       | 当前时间 | 创建时间 |

用户菜单关联表 (user_menu_items)

| 字段名         | 类型    | 是否为空 | 默认值 | 说明           |
| -------------- | ------- | -------- | ------ | -------------- |
| id             | Integer | 否       | -      | 主键           |
| user_id        | Integer | 否       | -      | 用户ID(外键)   |
| menu_item_id   | Integer | 否       | -      | 菜单项ID(外键) |
| has_permission | Boolean | 否       | True   | 是否有权限     |

按钮权限表 (button_permissions)

| 字段名       | 类型        | 是否为空 | 默认值 | 说明               |
| ------------ | ----------- | -------- | ------ | ------------------ |
| id           | Integer     | 否       | -      | 主键               |
| button_id    | String(50)  | 否       | -      | 按钮唯一标识       |
| description  | String(100) | 是       | NULL   | 按钮描述           |
| menu_item_id | Integer     | 否       | -      | 关联菜单项ID(外键) |

用户按钮权限表 (user_button_permissions)

| 字段名         | 类型       | 是否为空 | 默认值 | 说明         |
| -------------- | ---------- | -------- | ------ | ------------ |
| id             | Integer    | 否       | -      | 主键         |
| user_id        | Integer    | 否       | -      | 用户ID(外键) |
| button_id      | String(50) | 否       | -      | 按钮ID       |
| has_permission | Boolean    | 否       | False  | 是否有权限   |

用户表更新 (users) - 新增关系

| 关系               | 类型   | 说明                     |
| ------------------ | ------ | ------------------------ |
| menu_items         | 一对多 | 关联UserMenuItem         |
| button_permissions | 一对多 | 关联UserButtonPermission |

### 外键关系说明

1. `menu_items.parent_id` 自引用 `menu_items.id`
2. `user_menu_items.user_id` → `users.id`
3. `user_menu_items.menu_item_id` → `menu_items.id`
4. `button_permissions.menu_item_id` → `menu_items.id`
5. `user_button_permissions.user_id` → `users.id`

### 索引设计

1. `menu_items` 表:

   - 主键: id
   - 普通索引: parent_id, order
2. `user_menu_items` 表:

   - 主键: id
   - 唯一索引: (user_id, menu_item_id)
3. `button_permissions` 表:

   - 主键: id
   - 唯一索引: button_id
   - 普通索引: menu_item_id
4. `user_button_permissions` 表:

   - 主键: id
   - 唯一索引: (user_id, button_id)

## 2. API 设计

### 2.1 路由结构

```
/routers/
├── menu/
│   ├── __init__.py
│   ├── routes.py
│   ├── schemas.py
│   └── services.py
```

### 2.2 API 端点

#### 菜单项管理

| 方法   | 路径                     | 描述               |
| ------ | ------------------------ | ------------------ |
| GET    | `/api/menus`           | 获取所有菜单项     |
| POST   | `/api/menus`           | 创建新菜单项       |
| GET    | `/api/menus/{menu_id}` | 获取单个菜单项详情 |
| PUT    | `/api/menus/{menu_id}` | 更新菜单项         |
| DELETE | `/api/menus/{menu_id}` | 删除菜单项         |

#### 用户菜单权限

| 方法 | 路径                           | 描述             |
| ---- | ------------------------------ | ---------------- |
| GET  | `/api/users/{user_id}/menus` | 获取用户菜单权限 |
| POST | `/api/users/{user_id}/menus` | 设置用户菜单权限 |
| GET  | `/api/users/me/menus`        | 获取当前用户菜单 |

#### 按钮权限

| 方法 | 路径                             | 描述                 |
| ---- | -------------------------------- | -------------------- |
| GET  | `/api/buttons`                 | 获取所有按钮权限定义 |
| POST | `/api/buttons`                 | 创建按钮权限         |
| GET  | `/api/users/{user_id}/buttons` | 获取用户按钮权限     |
| POST | `/api/users/{user_id}/buttons` | 设置用户按钮权限     |


## 3. 前端数据结构示例

```json
{
  "menus": [
    {
      "id": 1,
      "title": "Dashboard",
      "icon": "dashboard",
      "route": "/dashboard",
      "buttons": [
        {
          "button_id": "dashboard_refresh",
          "has_permission": true
        }
      ],
      "children": [
        {
          "id": 2,
          "title": "Analytics",
          "route": "/dashboard/analytics",
          "buttons": []
        }
      ]
    }
  ]
}
```

## 4. 权限控制流程

1. **菜单加载流程**:

   - 用户登录后请求 `/api/users/me/menus`
   - 后端根据用户角色和权限返回可访问的菜单结构
   - 前端根据返回结果渲染侧边栏
2. **按钮权限检查**:

   - 页面加载时检查按钮权限
   - 根据权限决定是否显示或禁用按钮
   - 重要操作在API层面再次验证权限

## 5. 监控与审计

1. **日志记录**:

   - 记录菜单和按钮权限变更
   - 记录用户访问的菜单项
2. **性能优化**:

   - 缓存常用菜单结构
   - 批量查询按钮权限
3. **安全考虑**:

   - 后端始终验证权限
   - 敏感操作需要额外确认
