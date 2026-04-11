# Deploy

这个目录提供 `Tender AI` 的一键运行包。

## 前置条件

- 已安装 `Docker`
- 已安装 `Docker Compose`

## 启动

```bash
cd deploy
bash up.sh
```

首次启动时会自动：

- 复制 `deploy/.env.example` 为 `deploy/.env`
- 构建应用镜像
- 启动 `app`、`postgres`、`redis`
- 初始化 `t_users` 表

启动完成后可访问：

- 健康检查：`http://127.0.0.1:8000/v1/health`
- 注册接口：`POST http://127.0.0.1:8000/api/auth/register`
- 登录接口：`POST http://127.0.0.1:8000/api/auth/login`

## 停止

```bash
cd deploy
bash down.sh
```

## 环境变量

默认环境变量位于 `deploy/.env`。

常用项：

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `REDIS_URL`
- `AUTH_SECRET_KEY`

## 说明

- 数据库初始化 SQL 来自 `resources/sql/schema.sql`
- `postgres` 与 `redis` 数据通过 Docker volume 持久化
- 如果宿主机已占用 `8000`、`5432`、`6379` 端口，需要先调整 `deploy/docker-compose.yml`
