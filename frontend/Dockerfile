# 使用更轻量的 Node.js 镜像（参考后端成功的 python:3.11-slim）
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=production
ENV PORT=3000

# 复制 package 文件（参考后端的路径配置）
COPY frontend/package.json frontend/package-lock.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码（参考后端的路径配置）
COPY frontend/ .

# 构建应用
RUN npm run build

# 安装 serve
RUN npm install -g serve

# 暴露端口
EXPOSE $PORT

# 注意：启动命令由 Railway 的 startCommand 控制（参考后端）
