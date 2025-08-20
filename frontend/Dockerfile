# 使用更轻量的 Node.js 18 镜像
FROM node:18-alpine3.18

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=production
ENV PORT=3000

# 设置 npm 配置，提高网络稳定性
ENV NPM_CONFIG_REGISTRY=https://registry.npmjs.org/
ENV NPM_CONFIG_FETCH_RETRIES=5
ENV NPM_CONFIG_FETCH_RETRY_FACTOR=2
ENV NPM_CONFIG_FETCH_RETRY_MINTIMEOUT=10000
ENV NPM_CONFIG_FETCH_RETRY_MAXTIMEOUT=60000

# 复制 package 文件（确保包含 package-lock.json）
COPY package.json package-lock.json* ./

# 安装依赖（使用 npm install，添加重试机制）
RUN npm install --only=production --no-optional --no-audit --no-fund

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 安装 serve 用于生产环境
RUN npm install -g serve --no-optional --no-audit --no-fund

# 暴露端口
EXPOSE $PORT

# 启动应用
CMD ["serve", "-s", "dist", "-l", "$PORT"]
