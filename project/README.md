# 婚恋风控系统

AI驱动的婚恋风险评估系统，通过静态文本分析和动态AI对话来识别潜在风险。

## 🚀 快速开始

### 环境要求
- Node.js 16+
- Python 3.9+
- OpenAI API密钥

### 1. 克隆项目
```bash
git clone <repository-url>
cd girltalk
```

### 2. 配置环境变量
```bash
cd backend
cp env.example .env
# 编辑 .env 文件，添加你的 OpenAI API 密钥
```

### 3. 启动服务

#### 启动前端（新终端）
```bash
./start_frontend.sh
# 或手动执行：
cd frontend
npm install
npm run dev
```

#### 启动后端（新终端）
```bash
./start_backend.sh
# 或手动执行：
cd backend
pip install -r requirements.txt
python -m app.main
```

### 4. 访问系统
- 前端：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

## 📱 移动端H5特性

- 响应式设计，完美适配手机屏幕
- 触摸友好的交互界面
- 离线缓存支持
- PWA特性

## 🔧 系统架构

```
前端 (React + TypeScript) ←→ 后端 (FastAPI) ←→ AI API (OpenAI)
```

## 📊 核心功能

1. **静态风险扫描**：基于关键词的风险识别
2. **动态话术生成**：AI生成验证问题
3. **响应风险分析**：AI分析回答风险
4. **智能决策引擎**：综合评分决策

## 🎯 测试案例

输入：`男，1988，某私募MD，年薪500万+，有房贷，父母农村无医保`

预期结果：高风险，触发多个风险规则

## 📁 项目结构

```
girltalk/
├── frontend/          # React前端
├── backend/           # FastAPI后端
├── config/            # 配置文件
├── knowledge/         # 知识库
└── docs/             # 文档
```

## 🔑 配置说明

### 风险规则配置
- 文件：`backend/config/risk_rules.json`
- 可自定义触发词、风险值、验证话术

### 权重配置
- 文件：`backend/config/weight_config.yaml`
- 可调整静态/动态权重、风险阈值

### 知识库
- 文件：`backend/knowledge/*.csv`
- 支持CSV格式，可动态更新

## 🚨 注意事项

1. **API密钥安全**：请妥善保管OpenAI API密钥
2. **法律合规**：系统仅用于风险评估，请遵守相关法律法规
3. **数据隐私**：敏感信息请勿在测试环境中使用

## 📞 技术支持

如有问题，请查看：
- API文档：http://localhost:8000/docs
- 前端控制台日志
- 后端日志输出

## 🔄 更新日志

### v1.0.0
- 基础风控引擎
- 移动端H5界面
- AI集成支持
- 可配置规则库
