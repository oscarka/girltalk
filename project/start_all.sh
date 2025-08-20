#!/bin/bash
echo "🚀 启动婚恋风控系统..."

# 检查conda环境
if [[ "$CONDA_DEFAULT_ENV" != "girltalk" ]]; then
    echo "📦 正在激活girltalk conda环境..."
    source ~/miniconda3/etc/profile.d/conda.sh
    conda activate girltalk
fi

# 启动后端（后台运行）
echo "🔧 启动后端API服务器..."
cd backend
if ! python -c "import fastapi" 2>/dev/null; then
    echo "安装Python依赖..."
    pip install -r requirements.txt
fi
python -m app.main &
BACKEND_PID=$!
cd ..

# 等待后端启动
echo "⏳ 等待后端启动..."
sleep 3

# 检查后端是否启动成功
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 后端启动成功！"
else
    echo "❌ 后端启动失败，请检查日志"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# 启动前端
echo "🎨 启动前端开发服务器..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "安装Node.js依赖..."
    npm install
fi
npm run dev &
FRONTEND_PID=$!
cd ..

echo "🎉 系统启动完成！"
echo "📱 前端: http://localhost:3000"
echo "🔌 后端: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT
wait
