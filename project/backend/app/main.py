from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# 尝试导入API模块，如果失败则创建空的router
try:
    from app.api import risk_analysis, config_management
    risk_router = risk_analysis.router
    config_router = config_management.router
except ImportError as e:
    print(f"Warning: Failed to import API modules: {e}")
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
except ImportError:
    print("Warning: Failed to import config, using defaults")
    settings = None

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

# 注册路由
app.include_router(risk_router, prefix="/api/v1", tags=["风控分析"])
app.include_router(config_router, prefix="/api/v1", tags=["配置管理"])

@app.get("/")
async def root():
    return {"message": "婚恋风控系统API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
