# 使用Python 3.11官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# 注意：PORT环境变量由Railway自动设置，这里不需要固定值

# 安装系统依赖（只安装必要的）
RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE $PORT

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
