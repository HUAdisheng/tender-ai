# Tender Agent 认证功能技术设计

## 1. 设计范围

本文档基于以下文档，补充 `Tender Agent` 在当前阶段的认证功能技术设计：

- [`docs/prd/tender-agent-prd.md`](../../prd/tender-agent-prd.md)
- [`docs/tech/tender-agent-global-tech-design.md`](../tender-agent-global-tech-design.md)
- [`resources/sql/schema.sql`](../../../resources/sql/schema.sql)

当前阶段只聚焦以下能力：

- 用户注册
- 用户登录
- 认证模块在分层单体中的落点
- 注册与登录接口定义

本文档不覆盖：

- 用户资料能力
- 密码重置
- 第三方登录
- 多成员协作、组织、角色权限

## 2. 目标与约束

### 2.1 设计目标

- 先完成可落地的注册、登录闭环。
- 接口字段与 `t_users` 表结构保持一致，避免文档与落地实现脱节。
- 将认证职责从用户能力中独立出来，优先实现 `auth_service`。

### 2.2 核心约束

- 当前阶段 `user` 就是系统登录主体，也是公司主体。
- 当前只实现认证接口，不扩展资料、配置等用户相关能力。
- 注册与登录字段以 `t_users` 为准，核心输入字段使用 `username`、`password`。
- 路由层保持薄，数据库访问统一通过 `repositories/`。

## 3. 数据表对齐

当前认证实现直接对齐 [`resources/sql/schema.sql`](../../../resources/sql/schema.sql:5) 中的 `t_users` 表。

关键字段如下：

- `id`
- `username`
- `password`
- `status`
- `last_login_at`
- `is_deleted`
- `created_at`
- `updated_at`

当前设计约束：

- `username` 全局唯一。
- `password` 在数据库中保存哈希结果，不保存明文。
- `status` 仅允许 `active`、`disabled`。
- `is_deleted = true` 的数据不参与正常登录流程。

## 4. 模块拆分建议

### 4.1 服务拆分

当前阶段将“用户能力”和“认证能力”拆开：

- `auth_service`：负责注册、登录、密码校验、token 签发、登录时间更新。
- `user_service`：保留给后续用户资料类能力，当前阶段不实现。

这样拆分的原因：

- 当前实际要落地的是认证，不是完整用户中心。
- 可以避免把认证逻辑和后续用户资料逻辑混在一个 service 中。
- 后续补用户资料接口时，不需要重写认证职责边界。

### 4.2 目录建议

```text
app/
├── api/
│   └── v1/
│       ├── auth.py
│       └── users.py
├── core/
│   └── security.py
├── models/
│   └── user.py
├── schemas/
│   └── auth.py
├── repositories/
│   └── user_repository.py
└── services/
    ├── auth_service.py
    └── user_service.py
```

说明：

- 当前阶段实际实现 `api/v1/auth.py`、`schemas/auth.py`、`services/auth_service.py`。
- `users.py`、`user_service.py` 仅作为后续预留职责说明，不要求本阶段实现。

### 4.3 各层职责

`api/v1/auth.py`

- 暴露注册、登录接口
- 只负责请求解析、响应转换和依赖注入

`core/security.py`

- 负责密码哈希
- 负责密码校验
- 负责 token 签发

`models/user.py`

- 映射 `t_users` 持久化结构

`schemas/auth.py`

- 定义注册、登录请求响应模型

`repositories/user_repository.py`

- 负责按 `username` 查询用户
- 负责创建用户
- 负责更新 `last_login_at`

`services/auth_service.py`

- 编排注册流程
- 编排登录流程
- 统一处理用户名唯一性校验、状态校验和密码校验

## 5. 认证设计

### 5.1 注册

注册流程建议如下：

1. 校验 `username`、`password`
2. 检查 `username` 是否已存在
3. 对 `password` 进行哈希
4. 创建 `t_users` 记录
5. 返回注册结果

### 5.2 登录

登录流程建议如下：

1. 按 `username` 查询用户
2. 校验用户是否存在、是否已删除、状态是否为 `active`
3. 校验密码
4. 签发 `access_token`
5. 更新 `last_login_at`
6. 返回登录结果

### 5.3 安全建议

- 密码必须使用强哈希算法，如 `argon2` 或 `bcrypt`
- 不允许明文存储密码
- 登录失败统一返回通用认证失败信息
- 已禁用用户不允许登录

## 6. API 设计建议

### 6.1 接口列表

- `POST /api/auth/register`
- `POST /api/auth/login`

### 6.2 统一响应结构

所有接口统一返回 `application/json`：

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

错误响应示例：

```json
{
  "code": 4001001,
  "message": "username or password is invalid",
  "data": null
}
```

### 6.3 注册接口

接口：`POST /api/auth/register`

请求体示例：

```json
{
  "username": "acme_admin",
  "password": "StrongPassword@123"
}
```

成功响应示例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "id": "8a3f8fd0-0e8b-4f34-9b22-4f580c7b6736",
    "username": "acme_admin",
    "status": "active"
  }
}
```

### 6.4 登录接口

接口：`POST /api/auth/login`

请求体示例：

```json
{
  "username": "acme_admin",
  "password": "StrongPassword@123"
}
```

成功响应示例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "access_token": "jwt-access-token",
    "token_type": "Bearer",
    "expires_in": 7200,
    "user": {
      "id": "8a3f8fd0-0e8b-4f34-9b22-4f580c7b6736",
      "username": "acme_admin",
      "status": "active"
    }
  }
}
```

## 7. Repository 建议

建议 `user_repository.py` 提供以下方法：

- `get_by_username`
- `exists_by_username`
- `create_user`
- `update_last_login_at`

约束建议：

- 默认过滤 `is_deleted = true`
- 注册时只写入当前阶段必要字段
- 不在 repository 中处理密码哈希和 token 逻辑

## 8. 异常与日志建议

### 8.1 异常建议

- 用户不存在、密码错误统一返回通用认证失败信息
- 用户名重复时返回明确的业务错误
- 已禁用用户登录时返回标准化禁用提示

### 8.2 日志建议

- 记录注册成功、登录成功、登录失败等关键事件
- 日志中不输出明文密码和完整 token

## 9. 测试建议

建议补充以下测试：

- `tests/unit/`：用户名唯一性、密码哈希、密码校验、状态校验
- `tests/integration/`：注册接口、登录接口

关键验证点：

- 重复 `username` 无法注册
- 错误密码无法登录
- `disabled` 用户无法登录
- `is_deleted = true` 用户无法登录

## 10. 实施顺序建议

1. 先补 `models/user.py`
2. 再补 `schemas/auth.py`
3. 实现 `repositories/user_repository.py`
4. 实现 `core/security.py`
5. 实现 `services/auth_service.py`
6. 最后暴露 `api/v1/auth.py` 并补测试

## 11. 结论

当前阶段用户功能文档应收缩为认证功能文档，只描述注册和登录两项能力。实现上将 `auth_service` 与 `user_service` 分开，其中本阶段只落地 `auth_service`；接口字段直接对齐 `t_users` 表，统一使用 `username`、`password`，避免过早引入额外用户资料和配置能力。
