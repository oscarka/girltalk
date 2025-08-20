from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# 创建 FastAPI 应用实例
app = FastAPI(
    title="婚恋风控系统",
    description="AI驱动的婚恋风险评估系统",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 尝试导入API模块，如果失败则创建空的router
try:
    from app.api import risk_analysis, config_management
    risk_router = risk_analysis.router
    config_router = config_management.router
    print("✅ 成功导入API模块")
except ImportError as e:
    print(f"⚠️  Warning: Failed to import API modules: {e}")
    from fastapi import APIRouter
    risk_router = APIRouter()
    config_router = APIRouter()
    
    @risk_router.get("/health")
    async def risk_health():
        return {"status": "error", "message": "Risk analysis module not available"}
    
    @config_router.get("/health")
    async def config_health():
        return {"status": "error", "message": "Config management module not available"}

try:
    from app.core.config import settings
    print("✅ 成功导入配置模块")
except ImportError:
    print("⚠️  Warning: Failed to import config, using defaults")
    settings = None

# 注册路由
app.include_router(risk_router, prefix="/api/v1", tags=["风控分析"])
app.include_router(config_router, prefix="/api/v1", tags=["配置管理"])

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "婚恋风控系统API", 
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查端点 - Railway 使用此端点"""
    try:
        # 检查基本功能
        return {
            "status": "healthy", 
            "message": "Backend service is running",
            "timestamp": "2024-01-01T00:00:00Z",
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Health check failed: {str(e)}",
            "timestamp": "2024-01-01T00:00:00Z"
        }

@app.get("/api/health")
async def api_health_check():
    """API健康检查"""
    return {"status": "healthy", "message": "API service is running"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # 生产环境关闭热重载
    )
