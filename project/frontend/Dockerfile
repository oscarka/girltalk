# 构建阶段
FROM node:18-alpine AS builder

# 设置工作目录
WORKDIR /app

# 复制package文件
COPY project/frontend/package*.json ./

# 安装依赖
RUN npm ci

# 复制源代码
COPY project/frontend/ .

# 构建应用
RUN npm run build

# 生产阶段
FROM nginx:alpine

# 复制构建产物到nginx目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY project/frontend/nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE $PORT

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]
