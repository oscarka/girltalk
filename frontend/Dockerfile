# 使用稳定的 Node.js 镜像
FROM node:18-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=production
ENV PORT=3000

# 复制 package 文件
COPY package.json package-lock.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 安装 serve
RUN npm install -g serve

# 暴露端口
EXPOSE $PORT

# 注意：启动命令由 Railway 的 startCommand 控制
