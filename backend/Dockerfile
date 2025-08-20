# 使用更轻量的Python镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖（使用 apt 而不是 apk，更稳定）
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt
COPY requirements.txt .

# 安装Python依赖（分批安装，减少内存使用）
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE $PORT

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
