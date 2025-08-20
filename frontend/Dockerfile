# 使用更轻量的 Node.js 镜像（参考后端成功的 python:3.11-slim）
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=production
# 设置 Vite 环境变量，确保构建时能正确读取
ENV VITE_API_BASE_URL=https://backend-production-e222.up.railway.app

# 安装必要的系统依赖（Alpine 需要这些来编译某些 npm 包）
RUN apk add --no-cache python3 make g++

# 复制 package 文件（参考后端的路径配置）
COPY frontend/package.json frontend/package-lock.json ./

# 安装所有依赖（明确指定安装 devDependencies）
RUN npm ci --include=dev

# 安装 serve 用于生产环境
RUN npm install -g serve

# 复制源代码（参考后端的路径配置）
COPY frontend/ .

# 构建应用
RUN npm run build

# 暴露端口（使用 Railway 的 PORT 环境变量）
EXPOSE $PORT

# 启动命令（使用 shell 确保环境变量正确读取）
CMD sh -c "serve -s dist -l \${PORT:-3000}"
