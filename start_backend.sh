#!/bin/bash
echo "启动后端API服务器..."

# 检查是否在conda环境中
if [[ "$CONDA_DEFAULT_ENV" != "girltalk" ]]; then
    echo "正在激活girltalk conda环境..."
    source ~/miniconda3/etc/profile.d/conda.sh
    conda activate girltalk
fi

cd backend

# 检查依赖是否已安装
if ! python -c "import fastapi" 2>/dev/null; then
    echo "安装Python依赖..."
    pip install -r requirements.txt
else
    echo "Python依赖已安装，跳过安装步骤"
fi

echo "启动FastAPI服务器..."
python -m app.main
