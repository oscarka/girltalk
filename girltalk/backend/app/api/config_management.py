from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import yaml
from pathlib import Path
from app.core.config import settings

# 尝试导入pandas，如果失败则使用替代方案
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not available, using alternative CSV parsing")

router = APIRouter()

# 响应模型
class ConfigResponse(BaseModel):
    success: bool
    data: dict
    message: str

def _simple_csv_parse(file_path: Path) -> Dict:
    """简单的CSV解析替代方案"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < 2:
                return {"filename": file_path.name, "rows": 0, "columns": [], "preview": []}
            
            headers = lines[0].strip().split(',')
            data = []
            
            for line in lines[1:4]:  # 只取前3行作为预览
                values = line.strip().split(',')
                if len(values) == len(headers):
                    row = {}
                    for i, header in enumerate(headers):
                        row[header] = values[i]
                    data.append(row)
            
            return {
                "filename": file_path.name,
                "rows": len(lines) - 1,
                "columns": headers,
                "preview": data
            }
    except Exception as e:
        print(f"简单CSV解析失败: {e}")
        return {"filename": file_path.name, "rows": 0, "columns": [], "preview": []}

@router.get("/risk-rules", response_model=ConfigResponse)
async def get_risk_rules():
    """获取风险规则配置"""
    try:
        rules_file = Path(settings.config_dir) / "risk_rules.json"
        if rules_file.exists():
            with open(rules_file, 'r', encoding='utf-8') as f:
                rules = json.load(f)
            return ConfigResponse(
                success=True,
                data={"rules": rules},
                message="获取风险规则成功"
            )
        else:
            return ConfigResponse(
                success=False,
                data={},
                message="风险规则文件不存在"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取风险规则失败: {str(e)}")

@router.post("/risk-rules", response_model=ConfigResponse)
async def update_risk_rules(rules: Dict):
    """更新风险规则配置"""
    try:
        rules_file = Path(settings.config_dir) / "risk_rules.json"
        rules_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(rules, f, ensure_ascii=False, indent=2)
        
        return ConfigResponse(
            success=True,
            data={"rules": rules},
            message="更新风险规则成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新风险规则失败: {str(e)}")

@router.get("/weight-config", response_model=ConfigResponse)
async def get_weight_config():
    """获取权重配置"""
    try:
        config_file = Path(settings.config_dir) / "weight_config.yaml"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return ConfigResponse(
                success=True,
                data={"config": config},
                message="获取权重配置成功"
            )
        else:
            return ConfigResponse(
                success=False,
                data={},
                message="权重配置文件不存在"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取权重配置失败: {str(e)}")

@router.post("/weight-config", response_model=ConfigResponse)
async def update_weight_config(config: Dict):
    """更新权重配置"""
    try:
        config_file = Path(settings.config_dir) / "weight_config.yaml"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        return ConfigResponse(
            success=True,
            data={"config": config},
            message="更新权重配置成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新权重配置失败: {str(e)}")

@router.get("/knowledge-base", response_model=ConfigResponse)
async def get_knowledge_base():
    """获取知识库列表"""
    try:
        knowledge_dir = Path(settings.knowledge_dir)
        knowledge_files = {}
        
        if knowledge_dir.exists():
            for csv_file in knowledge_dir.glob("*.csv"):
                try:
                    if PANDAS_AVAILABLE:
                        df = pd.read_csv(csv_file, encoding='utf-8')
                        knowledge_files[csv_file.stem] = {
                            "filename": csv_file.name,
                            "rows": len(df),
                            "columns": list(df.columns),
                            "preview": df.head(3).to_dict('records')
                        }
                    else:
                        # 使用简单CSV解析
                        result = _simple_csv_parse(csv_file)
                        knowledge_files[csv_file.stem] = result
                except Exception as e:
                    print(f"读取知识库文件失败 {csv_file}: {e}")
                    # 尝试简单解析
                    result = _simple_csv_parse(csv_file)
                    knowledge_files[csv_file.stem] = result
        
        return ConfigResponse(
            success=True,
            data={"knowledge_files": knowledge_files},
            message="获取知识库列表成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取知识库列表失败: {str(e)}")

@router.post("/upload-knowledge", response_model=ConfigResponse)
async def upload_knowledge(file: UploadFile = File(...)):
    """上传知识库文件"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="只支持CSV文件")
        
        knowledge_dir = Path(settings.knowledge_dir)
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = knowledge_dir / file.filename
        
        # 保存文件
        content = await file.read()
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # 验证CSV格式
        try:
            if PANDAS_AVAILABLE:
                df = pd.read_csv(file_path, encoding='utf-8')
                result = {
                    "filename": file.filename,
                    "rows": len(df),
                    "columns": list(df.columns)
                }
            else:
                # 使用简单CSV解析
                result = _simple_csv_parse(file_path)
                result["filename"] = file.filename
            
            return ConfigResponse(
                success=True,
                data=result,
                message="上传知识库文件成功"
            )
        except Exception as e:
            # 如果CSV格式错误，删除文件
            file_path.unlink()
            raise HTTPException(status_code=400, detail=f"CSV格式错误: {str(e)}")
            
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"上传文件失败: {str(e)}")

@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "config_management"}
