# 使用更稳定的基础镜像，避免网络问题
FROM node:18-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=production
ENV PORT=3000

# 设置 npm 配置，提高网络稳定性
ENV NPM_CONFIG_REGISTRY=https://registry.npmjs.org/
ENV NPM_CONFIG_FETCH_RETRIES=15
ENV NPM_CONFIG_FETCH_RETRY_FACTOR=2
ENV NPM_CONFIG_FETCH_RETRY_MINTIMEOUT=30000
ENV NPM_CONFIG_FETCH_RETRY_MAXTIMEOUT=180000

# 添加调试信息
RUN echo "=== 开始构建前端应用 ===" && \
    echo "Node.js 版本: $(node --version)" && \
    echo "npm 版本: $(npm --version)" && \
    echo "当前工作目录: $(pwd)" && \
    echo "目录内容: $(ls -la)"

# 复制 package 文件（确保包含 package-lock.json）
COPY package.json package-lock.json* ./

# 显示复制的文件
RUN echo "=== 复制的文件 ===" && \
    echo "package.json 存在: $(test -f package.json && echo 'YES' || echo 'NO')" && \
    echo "package-lock.json 存在: $(test -f package-lock.json && echo 'YES' || echo 'NO')" && \
    echo "当前目录文件: $(ls -la)"

# 安装依赖（使用 npm install，添加重试机制）
RUN echo "=== 开始安装依赖 ===" && \
    npm install --only=production --no-optional --no-audit --no-fund --prefer-offline --verbose && \
    echo "=== 依赖安装完成 ==="

# 复制源代码
COPY . .

# 显示源代码文件
RUN echo "=== 源代码文件 ===" && \
    echo "src 目录存在: $(test -d src && echo 'YES' || echo 'NO')" && \
    echo "src 目录内容: $(ls -la src/ | head -10)"

# 构建应用
RUN echo "=== 开始构建应用 ===" && \
    npm run build && \
    echo "=== 构建完成 ==="

# 安装 serve 用于生产环境
RUN echo "=== 安装 serve ===" && \
    npm install -g serve --no-optional --no-audit --no-fund --prefer-offline && \
    echo "=== serve 安装完成 ==="

# 显示构建结果
RUN echo "=== 构建结果 ===" && \
    echo "dist 目录存在: $(test -d dist && echo 'YES' || echo 'NO')" && \
    echo "dist 目录内容: $(ls -la dist/)"

# 暴露端口
EXPOSE $PORT

# 启动应用
CMD ["serve", "-s", "dist", "-l", "$PORT"]
