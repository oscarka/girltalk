# 使用更轻量的 Node.js 镜像（参考后端成功的 python:3.11-slim）
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=production
ENV PORT=3000

# 设置 npm 配置，提高网络稳定性（参考后端的 --no-cache-dir）
ENV NPM_CONFIG_REGISTRY=https://registry.npmjs.org/
ENV NPM_CONFIG_FETCH_RETRIES=10
ENV NPM_CONFIG_FETCH_RETRY_FACTOR=2
ENV NPM_CONFIG_FETCH_RETRY_MINTIMEOUT=20000
ENV NPM_CONFIG_FETCH_RETRY_MAXTIMEOUT=120000

# 复制 package 文件
COPY package.json package-lock.json ./

# 安装依赖（参考后端的 pip install --no-cache-dir）
RUN npm ci --only=production --no-optional --no-audit --no-fund --prefer-offline

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 安装 serve（参考后端的简单依赖安装）
RUN npm install -g serve --no-optional --no-audit --no-fund

# 暴露端口
EXPOSE $PORT

# 注意：启动命令由 Railway 的 startCommand 控制（参考后端）
