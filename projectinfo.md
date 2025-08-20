我来仔细分析这个婚恋风控系统项目，并制定详细的工程化计划。

Read file: info.md
基于对项目文档的分析，我来制定详细的工程化计划。这是一个**婚恋风控系统**，核心功能是通过AI对话来识别和评估潜在风险。

## 🎯 项目理解

**核心意图**：构建一个智能风控系统，通过静态文本分析和动态AI对话来识别婚恋关系中的潜在风险，如职业造假、资产隐瞒、家庭负担等。

**核心流程**：
1. 静态风险扫描（关键词匹配）
2. 动态话术生成（AI生成验证问题）
3. 响应分析（AI分析回答风险）
4. 决策引擎（综合评分决策）

## ��️ 详细工程化计划

### 一、技术架构设计

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端 (React)  │    │   后端 (FastAPI) │    │   AI API服务    │
│                 │    │                 │    │                 │
│ - 用户输入界面  │◄──►│ - 风控引擎      │◄──►│ - OpenAI GPT    │
│ - 结果展示      │    │ - 规则管理      │    │ - 话术生成      │
│ - 配置管理      │    │ - 知识库管理    │    │ - 响应分析      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 二、目录结构规划

```
girltalk/
├── frontend/                 # React前端
│   ├── src/
│   │   ├── components/      # 组件
│   │   ├── pages/          # 页面
│   │   ├── services/       # API调用
│   │   └── utils/          # 工具函数
│   ├── public/
│   └── package.json
├── backend/                 # FastAPI后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── config/             # 配置文件
│   ├── knowledge/          # 知识库
│   └── requirements.txt
├── docs/                   # 文档
└── README.md
```

### 三、核心功能模块

#### 1. 前端模块
- **用户输入界面**：文本输入、文件上传
- **风控结果展示**：风险评分、触发规则、证据链
- **配置管理界面**：规则库编辑、权重调整
- **知识库管理**：CSV文件上传、编辑

#### 2. 后端模块
- **风控引擎**：静态扫描、动态生成、响应分析
- **规则管理**：CRUD操作、版本控制
- **知识库管理**：CSV解析、数据验证
- **决策引擎**：权重计算、阈值判断

#### 3. AI集成模块
- **话术生成**：基于规则和知识库生成验证问题
- **响应分析**：分析用户回答的风险特征
- **智能优化**：基于历史数据优化规则

### 四、需要AI API的关键场景

#### 1. 话术生成（必需）
```python
# 调用OpenAI API生成验证话术
def generate_verification_tactic(rule_name, knowledge_item):
    prompt = f"""
    基于以下信息生成一个自然的验证问题：
    规则：{rule_name}
    知识：{knowledge_item}
    要求：问题要自然，不能太直接，要能验证对方是否真的了解这个领域
    """
    # 调用OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

#### 2. 响应风险分析（必需）
```python
# 分析用户回答的风险特征
def analyze_response_risk(response_text):
    prompt = f"""
    分析以下回答的风险特征，返回JSON格式：
    回答：{response_text}
    
    分析维度：
    1. 模糊回避（0-100分）
    2. 情绪攻击（0-100分）
    3. 话题转移（0-100分）
    4. 精准回答（0-100分）
    5. 风险标签列表
    6. 总体风险评分
    """
    # 调用OpenAI API
    # 返回结构化分析结果
```

#### 3. 智能规则优化（可选）
```python
# 基于历史数据优化规则权重
def optimize_rule_weights(historical_data):
    prompt = f"""
    基于以下历史数据，优化风险规则的权重配置：
    {historical_data}
    
    分析哪些规则误判率高，哪些规则漏判率高，
    给出优化建议和新的权重配置。
    """
    # 调用OpenAI API
```

### 五、开发阶段规划

#### 阶段1：基础架构（1-2周）
- 搭建前后端项目结构
- 实现基础API接口
- 配置数据库和文件存储

#### 阶段2：核心引擎（2-3周）
- 实现静态风险扫描
- 集成AI API进行话术生成
- 实现响应分析器

#### 阶段3：前端界面（2-3周）
- 用户输入界面
- 结果展示组件
- 配置管理界面

#### 阶段4：集成测试（1-2周）
- 端到端测试
- 性能优化
- 部署配置

### 六、技术选型建议

#### 前端
- **框架**：React + TypeScript
- **UI库**：Ant Design / Material-UI
- **状态管理**：Redux Toolkit
- **构建工具**：Vite

#### 后端
- **框架**：FastAPI + Python 3.9+
- **数据库**：SQLite（开发）/ PostgreSQL（生产）
- **文件存储**：本地文件系统
- **API文档**：自动生成Swagger

#### AI集成
- **主要API**：OpenAI GPT-3.5/4
- **备用方案**：Claude / 文心一言
- **本地模型**：可考虑使用开源模型

### 七、关键配置项

#### 环境变量
```bash
# .env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-3.5-turbo
RISK_THRESHOLD_TERMINATE=75
RISK_THRESHOLD_WARNING=40
STATIC_WEIGHT=0.6
DYNAMIC_WEIGHT=0.4
```

#### 规则配置
- 风险规则库（JSON）
- 权重配置（YAML）
- 知识库文件（CSV）

### 八、部署方案

#### 开发环境
- 前端：`npm run dev` (localhost:3000)
- 后端：`uvicorn main:app --reload` (localhost:8000)

#### 生产环境
- 前端：Nginx静态文件服务
- 后端：Gunicorn + Nginx反向代理
- 数据库：PostgreSQL
- 文件存储：对象存储服务

## �� 下一步行动

1. **确认技术选型**：是否同意使用React+FastAPI+OpenAI的组合？
2. **准备AI API密钥**：需要OpenAI或其他AI服务的API密钥
3. **开始项目搭建**：我可以立即开始创建项目结构和核心代码
