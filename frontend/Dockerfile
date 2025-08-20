# 使用更轻量的 Node.js 镜像（参考后端成功的 python:3.11-slim）
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=production
# 移除固定端口，使用 Railway 提供的 $PORT

# 安装必要的系统依赖（Alpine 需要这些来编译某些 npm 包）
RUN apk add --no-cache python3 make g++

# 复制 package 文件（参考后端的路径配置）
COPY frontend/package.json frontend/package-lock.json ./

# 安装所有依赖（明确指定安装 devDependencies）
RUN npm ci --include=dev

# 复制源代码（参考后端的路径配置）
COPY frontend/ .

# 构建应用
RUN npm run build

# 暴露端口（使用环境变量）
EXPOSE $PORT

# 注意：启动命令由 Railway 的 startCommand 控制（参考后端）
