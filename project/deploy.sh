#!/bin/bash

# Railway部署脚本
echo "🚀 开始部署到Railway..."

# 检查git状态
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  发现未提交的更改，正在提交..."
    git add .
    git commit -m "Update: Railway部署配置"
fi

# 推送到GitHub
echo "📤 推送到GitHub..."
git push origin main

echo "✅ 代码已推送到GitHub"
echo ""
echo "📋 下一步操作："
echo "1. 在Railway上创建 girltalk-backend 项目"
echo "2. 连接GitHub仓库，选择 girltalk/backend 目录"
echo "3. 配置环境变量（包含DeepSeek API密钥）"
echo "4. 部署后端并获取域名"
echo "5. 在Railway上创建 girltalk-frontend 项目"
echo "6. 连接GitHub仓库，选择 girltalk/frontend 目录"
echo "7. 配置环境变量（包含后端域名）"
echo "8. 部署前端"
echo ""
echo "📖 详细部署说明请查看 RAILWAY_DEPLOY.md"
