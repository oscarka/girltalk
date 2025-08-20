# 第一阶段：构建阶段
FROM node:18-slim as builder

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=development

# 复制 package 文件
COPY package.json package-lock.json* ./

# 安装所有依赖（包括 devDependencies）
RUN npm ci --only=production=false

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 第二阶段：运行时镜像
FROM node:18-slim as runtime

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=production
ENV PORT=3000
ENV RAILWAY_ENVIRONMENT=production

# 安装 serve 用于生产环境
RUN npm install -g serve --no-optional --no-audit --no-fund

# 复制构建产物
COPY --from=builder /app/dist ./dist

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app

# 创建必要的目录并设置权限
RUN mkdir -p logs && \
    chown -R app:app /app

# 暴露端口
EXPOSE $PORT

# 切换到非root用户
USER app

# 启动应用
CMD ["serve", "-s", "dist", "-l", "$PORT"]
