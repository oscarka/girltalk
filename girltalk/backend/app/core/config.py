from typing import Optional
import os

# 尝试导入pydantic_settings，如果失败则使用替代方案
try:
    from pydantic_settings import BaseSettings
    PYDANTIC_SETTINGS_AVAILABLE = True
except ImportError:
    PYDANTIC_SETTINGS_AVAILABLE = False
    print("Warning: pydantic-settings not available, using simple config")

if PYDANTIC_SETTINGS_AVAILABLE:
    class Settings(BaseSettings):
        # 应用配置
        app_name: str = "婚恋风控系统"
        app_version: str = "1.0.0"
        debug: bool = True
        
        # 服务器配置
        host: str = "0.0.0.0"
        port: int = 8000
        
        # DeepSeek API配置
        deepseek_api_key: Optional[str] = None
        deepseek_api_base: str = "https://api.deepseek.com"
        deepseek_model: str = "deepseek-chat"
        deepseek_max_tokens: int = 1000
        
        # 风控配置
        risk_threshold_terminate: int = 75
        risk_threshold_warning: int = 40
        static_weight: float = 0.6
        dynamic_weight: float = 0.4
        
        # 文件路径配置
        config_dir: str = "config"
        knowledge_dir: str = "knowledge"
        
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
else:
    # 简单的配置类替代方案
    class Settings:
        def __init__(self):
            self.app_name = "婚恋风控系统"
            self.app_version = "1.0.0"
            self.debug = True
            self.host = "0.0.0.0"
            self.port = 8000
            self.deepseek_api_key = None
            self.deepseek_api_base = "https://api.deepseek.com"
            self.deepseek_model = "deepseek-chat"
            self.deepseek_max_tokens = 1000
            self.risk_threshold_terminate = 75
            self.risk_threshold_warning = 40
            self.static_weight = 0.6
            self.dynamic_weight = 0.4
            self.config_dir = "config"
            self.knowledge_dir = "knowledge"
            
            # 从环境变量加载配置
            self._load_from_env()
        
        def _load_from_env(self):
            """从环境变量加载配置"""
            if os.path.exists(".env"):
                try:
                    with open(".env", "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#") and "=" in line:
                                key, value = line.split("=", 1)
                                key = key.strip()
                                value = value.strip()
                                
                                if hasattr(self, key.lower()):
                                    if value.lower() in ("true", "false"):
                                        setattr(self, key.lower(), value.lower() == "true")
                                    elif value.isdigit():
                                        setattr(self, key.lower(), int(value))
                                    elif "." in value and value.replace(".", "").isdigit():
                                        setattr(self, key.lower(), float(value))
                                    else:
                                        setattr(self, key.lower(), value)
                except Exception as e:
                    print(f"Warning: Failed to load .env file: {e}")

# 创建全局设置实例
settings = Settings()

# 从环境变量加载配置
if os.path.exists(".env"):
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ 成功加载.env文件")
        
        # 重新加载配置
        if PYDANTIC_SETTINGS_AVAILABLE:
            settings = Settings()
            print("✅ 使用pydantic-settings重新加载配置")
        else:
            print("⚠️  pydantic-settings不可用，使用简单配置")
    except Exception as e:
        print(f"❌ 加载.env文件失败: {e}")
else:
    print("⚠️  .env文件不存在，使用默认配置")

# 打印关键配置信息
print(f"🔧 应用配置:")
print(f"   - 应用名称: {settings.app_name}")
print(f"   - 服务器地址: {settings.host}:{settings.port}")
print(f"   - DeepSeek API密钥: {settings.deepseek_api_key[:10] if settings.deepseek_api_key else '未配置'}...")
print(f"   - DeepSeek API地址: {settings.deepseek_api_base}")
print(f"   - DeepSeek 模型: {settings.deepseek_model}")
print(f"   - 调试模式: {settings.debug}")
