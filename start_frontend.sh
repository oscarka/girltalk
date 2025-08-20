#!/bin/bash
echo "启动前端开发服务器..."

cd frontend

# 检查node_modules是否存在
if [ ! -d "node_modules" ]; then
    echo "安装Node.js依赖..."
    npm install
else
    echo "Node.js依赖已安装，跳过安装步骤"
fi

echo "启动Vite开发服务器..."
npm run dev
