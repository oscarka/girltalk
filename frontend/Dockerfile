# 使用 Node.js 18 Alpine 镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=production
ENV PORT=3000

# 安装系统依赖
RUN apk add --no-cache dumb-init

# 复制 package 文件（确保包含 package-lock.json）
COPY package.json package-lock.json* ./

# 安装依赖（使用 npm install 而不是 npm ci，更兼容）
RUN npm install --only=production

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 安装 serve 用于生产环境
RUN npm install -g serve

# 暴露端口
EXPOSE $PORT

# 使用 dumb-init 启动应用
ENTRYPOINT ["dumb-init", "--"]
CMD ["serve", "-s", "dist", "-l", "$PORT"]
