# Railway 部署指南

## 项目概述

本项目包含前端和后端两个部分，可以分别部署到Railway上。

### 目录结构
```
oscarka/girltalk (GitHub仓库)
└── girltalk/                    ← 项目根目录
    ├── backend/                 ← Python后端代码
    │   ├── app/                 ← FastAPI应用
    │   ├── config/              ← 配置文件
    │   ├── requirements.txt     ← Python依赖
    │   └── railway.json         ← 后端Railway配置
    ├── frontend/                ← React前端代码
    │   ├── src/                 ← 源代码
    │   ├── package.json         ← Node.js依赖
    │   └── railway.json         ← 前端Railway配置
    └── README.md                ← 项目说明
```

## 部署架构

```
┌─────────────────┐    ┌─────────────────┐
│   前端 (React)  │    │   后端 (FastAPI) │
│   Railway #1    │    │   Railway #2     │
│   Port: 3000    │    │   Port: 8000     │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┘
                 API调用
```

## 后端部署 (Backend)

### 1. 在Railway上创建新项目
- 项目名称: `girltalk-backend`
- 选择 "Deploy from GitHub repo"
- 选择仓库: `oscarka/girltalk`
- **子目录设置**: `girltalk/backend` ⭐ **关键设置**

### 2. 环境变量配置
在Railway项目设置中添加以下环境变量：

```bash
# DeepSeek API配置
DEEPSEEK_API_KEY=sk-6f5caabbb32b411cb21426002d64726f
DEEPSEEK_API_BASE=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_MAX_TOKENS=1000

# 应用配置
ENVIRONMENT=production
# 注意：PORT环境变量由Railway自动设置，无需手动配置
```

### 3. 部署配置
- **构建命令**: Railway会自动检测Python项目
- **启动命令**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **健康检查**: `/health` 端点

### 4. 域名设置
部署完成后，Railway会提供一个域名，如：
`https://girltalk-backend-production-xxxx.up.railway.app`

## 前端部署 (Frontend)

### 1. 在Railway上创建新项目
- 项目名称: `girltalk-frontend`
- 选择 "Deploy from GitHub repo"
- 选择仓库: `oscarka/girltalk`
- **子目录设置**: `girltalk/frontend` ⭐ **关键设置**

### 2. 环境变量配置
在Railway项目设置中添加以下环境变量：

```bash
# 后端API地址
VITE_API_BASE_URL=https://girltalk-backend-production-xxxx.up.railway.app

# 应用配置
NODE_ENV=production
# 注意：PORT环境变量由Railway自动设置，无需手动配置
```

### 3. 部署配置
- **构建命令**: `npm run build`
- **启动命令**: `npm run preview`
- **健康检查**: `/` 端点

### 4. 域名设置
部署完成后，Railway会提供一个域名，如：
`https://girltalk-frontend-production-xxxx.up.railway.app`

## 前端API配置更新

部署完成后，需要更新前端的API配置：

```typescript
// girltalk/frontend/src/services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

## 部署步骤

### 第一步：部署后端
1. 在Railway上创建 `girltalk-backend` 项目
2. 连接GitHub仓库: `oscarka/girltalk`
3. **设置子目录**: `girltalk/backend` ⭐ **关键设置**
4. 配置环境变量
5. 部署并获取域名

### 第二步：部署前端
1. 在Railway上创建 `girltalk-frontend` 项目
2. 连接GitHub仓库: `oscarka/girltalk`
3. **设置子目录**: `girltalk/frontend` ⭐ **关键设置**
4. 配置环境变量（包含后端域名）
5. 部署并获取域名

### 第三步：测试
1. 访问前端域名
2. 测试风控分析功能
3. 检查API调用是否正常

## 注意事项

1. **环境变量**: 确保所有敏感信息都通过环境变量配置
2. **端口配置**: **不要手动设置PORT环境变量**，Railway会自动分配并设置$PORT
3. **子目录设置**: ⭐ **必须正确设置子目录**，这是部署成功的关键
4. **CORS设置**: 后端已配置允许所有来源，生产环境可限制为前端域名
5. **健康检查**: 两个服务都有健康检查端点，Railway会自动监控
6. **域名更新**: 如果域名变化，需要更新前端的环境变量

### ⚠️ 重要提醒
- **不要从根目录 `girltalk` 部署**，这会导致Nixpacks构建失败
- **必须分别创建两个Railway项目**，每个项目指向不同的子目录
- **子目录设置是部署成功的关键**，请严格按照说明操作

## 端口配置说明

### 重要提醒
- **不要手动设置PORT环境变量**
- **Railway会自动分配端口并设置$PORT环境变量**
- **应用代码必须使用$PORT而不是固定端口**

### 正确的端口使用方式
```bash
# 后端启动命令
uvicorn app.main:app --host 0.0.0.0 --port $PORT

# 前端启动命令  
npm run preview -- --port $PORT
```

## 故障排除

### 常见问题
1. **构建失败**: 检查依赖是否正确安装
2. **启动失败**: 检查环境变量和端口配置
3. **API调用失败**: 检查前端API地址配置
4. **健康检查失败**: 检查应用是否正常启动

### 日志查看
在Railway项目页面可以查看实时日志，帮助诊断问题。
