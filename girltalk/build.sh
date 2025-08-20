#!/bin/bash

# Railway构建脚本
echo "🔍 检测项目类型..."

# 检查是否有Python文件
if [ -f "requirements.txt" ] || [ -f "app/main.py" ]; then
    echo "🐍 检测到Python后端项目"
    echo "🚀 开始构建后端..."
    
    # 安装Python依赖
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
    
    # 启动后端
    exec uvicorn app.main:app --host 0.0.0.0 --port $PORT

# 检查是否有Node.js文件
elif [ -f "package.json" ]; then
    echo "⚛️  检测到React前端项目"
    echo "🚀 开始构建前端..."
    
    # 安装Node.js依赖
    npm ci
    
    # 构建前端
    npm run build
    
    # 启动前端服务
    exec npm run preview -- --port $PORT

else
    echo "❌ 无法识别项目类型"
    echo "📋 当前目录内容："
    ls -la
    
    echo ""
    echo "💡 请确保："
    echo "1. 后端项目包含 requirements.txt 或 app/main.py"
    echo "2. 前端项目包含 package.json"
    echo "3. 或者分别部署到不同的Railway项目"
    
    exit 1
fi
