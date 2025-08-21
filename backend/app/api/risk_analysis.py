from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from app.services.risk_engine import RiskEngine

router = APIRouter()

# 请求模型
class RiskAnalysisRequest(BaseModel):
    input_text: str
    user_response: Optional[str] = None

class StaticScanRequest(BaseModel):
    text: str

class DynamicAnalysisRequest(BaseModel):
    response_text: str

class GenerateTacticsRequest(BaseModel):
    rules: List[Dict]
    ai_analysis: Dict

# 响应模型
class RiskAnalysisResponse(BaseModel):
    success: bool
    data: dict
    message: str

# 依赖注入
def get_risk_engine():
    try:
        return RiskEngine()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"风控引擎初始化失败: {str(e)}")

@router.post("/static-scan", response_model=RiskAnalysisResponse)
async def static_risk_scan(
    request: StaticScanRequest,
    risk_engine: RiskEngine = Depends(get_risk_engine)
):
    """静态风险扫描"""
    try:
        result = await risk_engine.static_risk_scan(request.text)
        return RiskAnalysisResponse(
            success=True,
            data=result,
            message="静态风险扫描完成"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"静态扫描失败: {str(e)}")

@router.post("/dynamic-analysis", response_model=RiskAnalysisResponse)
async def dynamic_risk_analysis(
    request: DynamicAnalysisRequest,
    risk_engine: RiskEngine = Depends(get_risk_engine)
):
    """动态风险分析"""
    try:
        result = await risk_engine.analyze_response(request.response_text)
        return RiskAnalysisResponse(
            success=True,
            data=result,
            message="动态风险分析完成"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"动态分析失败: {str(e)}")

@router.post("/generate-tactics", response_model=RiskAnalysisResponse)
async def generate_verification_tactics(
    request: GenerateTacticsRequest,
    risk_engine: RiskEngine = Depends(get_risk_engine)
):
    """基于已有的AI提示生成验证话术"""
    try:
        # 直接基于传入的规则和AI分析结果生成话术
        verification_tactics = await risk_engine.generate_verification_tactics(
            request.rules, 
            request.ai_analysis
        )
        
        # 返回话术相关的结果
        tactics_result = {
            "verification_tactics": verification_tactics,
            "rules": request.rules,
            "ai_analysis": request.ai_analysis
        }
        
        return RiskAnalysisResponse(
            success=True,
            data=tactics_result,
            message="话术生成完成"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"话术生成失败: {str(e)}")

@router.post("/full-analysis", response_model=RiskAnalysisResponse)
async def full_risk_analysis(
    request: RiskAnalysisRequest,
    risk_engine: RiskEngine = Depends(get_risk_engine)
):
    """完整风控分析"""
    try:
        result = await risk_engine.full_risk_analysis(
            request.input_text,
            request.user_response
        )
        return RiskAnalysisResponse(
            success=True,
            data=result,
            message="完整风控分析完成"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"完整分析失败: {str(e)}")

@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "risk_analysis"}
