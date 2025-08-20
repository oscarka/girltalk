import json
import yaml
import random
import traceback
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from datetime import datetime
from app.services.deepseek_service import DeepSeekService
from app.core.config import settings
import time # Added for performance monitoring

# 尝试导入pandas，如果失败则使用替代方案
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not available, using alternative timestamp")

class RiskEngine:
    def __init__(self):
        self.config_dir = Path(settings.config_dir)
        self.knowledge_dir = Path(settings.knowledge_dir)
        self.deepseek_service = DeepSeekService()
        
        # 加载配置
        self.risk_rules = self._load_risk_rules()
        self.weight_config = self._load_weight_config()
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_risk_rules(self) -> Dict:
        """加载风险规则"""
        rules_file = self.config_dir / "risk_rules.json"
        if rules_file.exists():
            with open(rules_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_weight_config(self) -> Dict:
        """加载权重配置"""
        config_file = self.config_dir / "weight_config.yaml"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_knowledge_base(self) -> Dict[str, List[Dict]]:
        """加载知识库"""
        knowledge = {}
        if self.knowledge_dir.exists():
            for csv_file in self.knowledge_dir.glob("*.csv"):
                try:
                    if PANDAS_AVAILABLE:
                        df = pd.read_csv(csv_file, encoding='utf-8')
                        knowledge[csv_file.stem] = df.to_dict('records')
                    else:
                        # 简单的CSV解析替代方案
                        knowledge[csv_file.stem] = self._simple_csv_parse(csv_file)
                except Exception as e:
                    print(f"加载知识库文件失败 {csv_file}: {e}")
        return knowledge
    
    def _simple_csv_parse(self, csv_file: Path) -> List[Dict]:
        """简单的CSV解析替代方案"""
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) < 2:
                    return []
                
                headers = lines[0].strip().split(',')
                data = []
                
                for line in lines[1:]:
                    values = line.strip().split(',')
                    if len(values) == len(headers):
                        row = {}
                        for i, header in enumerate(headers):
                            row[header] = values[i]
                        data.append(row)
                
                return data
        except Exception as e:
            print(f"简单CSV解析失败: {e}")
            return []
    
    async def static_risk_scan(self, text: str) -> Dict:
        """增强的静态风险扫描 - 结合AI分析"""
        print(f"🔍 开始静态风险扫描，文本长度: {len(text)}")
        print(f"📝 扫描文本: {text[:100]}...")
        
        risk_score = 0
        triggered_rules = []
        
        # 1. 传统关键词匹配
        print("🔍 步骤1: 传统关键词匹配")
        for rule_name, rule_config in self.risk_rules.items():
            if any(keyword in text for keyword in rule_config["触发词"]):
                risk_score += rule_config["风险值"]
                triggered_rules.append({
                    "rule_name": rule_name,
                    "risk_value": rule_config["风险值"],
                    "keywords": [k for k in rule_config["触发词"] if k in text],
                    "detection_method": "keyword_match"
                })
                print(f"✅ 触发关键词规则: {rule_name}, 风险值: {rule_config['风险值']}")
        
        print(f"📊 关键词匹配结果: 触发{len(triggered_rules)}条规则, 当前风险分: {risk_score}")
        
        # 2. AI智能风险分析
        print("🤖 步骤2: AI智能风险分析")
        ai_analysis = await self._ai_risk_analysis(text)
        if ai_analysis:
            ai_risk_score = ai_analysis.get("risk_score", 0)
            ai_rules = ai_analysis.get("ai_rules", [])
            risk_score += ai_risk_score
            triggered_rules.extend(ai_rules)
            print(f"✅ AI分析完成: 风险分+{ai_risk_score}, 新增{len(ai_rules)}条AI规则")
            print(f"📋 AI分析结果: {ai_analysis}")
        else:
            print("❌ AI分析失败或返回空结果")
        
        # 3. 风险模式识别
        print("🔍 步骤3: 风险模式识别")
        pattern_rules = await self._detect_risk_patterns(text)
        pattern_risk_score = pattern_rules.get("risk_score", 0)
        pattern_rules_list = pattern_rules.get("pattern_rules", [])
        risk_score += pattern_risk_score
        triggered_rules.extend(pattern_rules_list)
        print(f"✅ 模式识别完成: 风险分+{pattern_risk_score}, 新增{len(pattern_rules_list)}条模式规则")
        
        final_score = min(risk_score, 100)
        print(f"🎯 扫描完成: 总风险分 {risk_score} -> 最终分 {final_score}")
        print(f"📊 总计触发 {len(triggered_rules)} 条规则")
        
        result = {
            "score": final_score,
            "rules": triggered_rules,
            "total_rules": len(triggered_rules),
            "ai_analysis": ai_analysis,
            "pattern_analysis": pattern_rules
        }
        
        print(f"📤 返回结果: {result}")
        return result
    
    async def _ai_risk_analysis(self, text: str) -> Dict:
        """AI智能风险分析 - 判断是否匹配配置文件中的风险规则"""
        print(f"🤖 开始AI风险分析，文本: {text[:50]}...")
        
        try:
            # 构建风险规则信息，让AI判断是否匹配
            risk_rules_info = []
            for rule_name, rule_config in self.risk_rules.items():
                risk_rules_info.append({
                    "rule_name": rule_name,
                    "keywords": rule_config["触发词"],
                    "risk_value": rule_config["风险值"],
                    "description": f"检测{rule_name}相关的风险"
                })
            
            prompt = f"""
            你是一个专业的风险分析专家，请分析以下个人信息是否匹配已知的风险规则。

            已知风险规则（必须仔细分析）：
            {risk_rules_info}
            
            分析要求（必须严格执行）：
            1. 仔细阅读个人信息，理解其含义和潜在风险
            2. 必须判断是否匹配上述风险规则（即使没有完全相同的关键词，也要看语义是否相关）
            3. 如果匹配到已知规则，必须使用配置文件中的风险值，并在matched_rule字段中标注
            4. 如果不匹配任何已知规则，必须提出新的风险点（风险值设为5-15）
            5. 必须返回至少1条风险规则，不能返回空的ai_rules数组
            
            分析示例：
            - "小国企负责人力工作" → 可能匹配"职业模糊"规则（语义相关，缺乏具体信息）
            - "澳大利亚迪肯本硕" → 可能匹配"收入模糊"相关（海外学历需要经济基础验证）
            - "原生家庭和睦" → 可能匹配"家庭负担"相关（需要验证家庭经济状况）
            
            请返回JSON格式（必须包含ai_rules数组）：
            {{
                "risk_score": 总风险评分(累加所有匹配规则的风险值),
                "risk_reasons": ["风险原因1", "风险原因2"],
                "ai_rules": [
                    {{
                        "rule_name": "规则名称",
                        "risk_value": 风险值(使用配置文件中的值或AI评估值),
                        "detection_method": "ai_analysis",
                        "description": "AI分析描述",
                        "matched_rule": "匹配的配置文件规则名称(如果匹配到)"
                    }}
                ],
                "verification_suggestions": ["建议验证的问题1", "建议验证的问题2"]
            }}
            
            个人信息：{text}
            
            重要提醒：必须分析出风险点，不能返回空的ai_rules数组！
            """
            
            print(f"📤 发送AI请求，prompt长度: {len(prompt)}")
            print(f"🔑 使用DeepSeek服务进行AI分析")
            print(f"🌐 API地址: {self.deepseek_service.api_base}")
            
            result = await self.deepseek_service.generate_verification_tactic(
                "AI风险分析", {"prompt": prompt}
            )
            
            print(f"📥 AI返回结果: {result}")
            
            # 尝试解析AI返回的JSON
            try:
                import json
                # 清理AI返回的内容，去掉markdown代码块标记
                cleaned_result = result.strip()
                if cleaned_result.startswith('```json'):
                    cleaned_result = cleaned_result[7:]  # 去掉 ```json
                if cleaned_result.endswith('```'):
                    cleaned_result = cleaned_result[:-3]  # 去掉 ```
                cleaned_result = cleaned_result.strip()
                
                print(f"🧹 清理后的内容: {cleaned_result}")
                
                ai_result = json.loads(cleaned_result)
                print(f"✅ AI结果JSON解析成功: {ai_result}")
                
                # 验证AI返回的风险值是否与配置文件一致
                for rule in ai_result.get("ai_rules", []):
                    rule_name = rule.get("rule_name", "")
                    ai_risk_value = rule.get("risk_value", 0)
                    matched_rule = rule.get("matched_rule", "")
                    
                    if matched_rule and matched_rule in self.risk_rules:
                        config_risk_value = self.risk_rules[matched_rule]["风险值"]
                        if ai_risk_value != config_risk_value:
                            print(f"⚠️ 风险值不一致: AI返回{ai_risk_value}, 配置文件{config_risk_value}, 使用配置文件值")
                            rule["risk_value"] = config_risk_value
                
                return ai_result
            except json.JSONDecodeError as e:
                print(f"❌ AI返回结果JSON解析失败: {e}")
                print(f"📝 原始返回内容: {result}")
                print(f"🧹 清理后内容: {cleaned_result if 'cleaned_result' in locals() else '未清理'}")
                # 如果AI返回的不是JSON，使用默认分析
                return {
                    "risk_score": 0,
                    "risk_reasons": ["AI分析完成，但返回格式异常"],
                    "ai_rules": [],
                    "verification_suggestions": ["请进一步验证信息真实性"]
                }
                
        except Exception as e:
            print(f"❌ AI风险分析异常: {e}")
            import traceback
            print(f"📋 异常堆栈: {traceback.format_exc()}")
            return {
                "risk_score": 0,
                "risk_reasons": [f"AI分析失败: {str(e)}"],
                "ai_rules": [],
                "verification_suggestions": ["请手动验证信息"]
            }
    
    async def _detect_risk_patterns(self, text: str) -> Dict:
        """风险模式识别"""
        patterns = []
        risk_score = 0
        
        # 1. 数字模式检测
        import re
        numbers = re.findall(r'\d+', text)
        if len(numbers) > 10:  # 数字过多可能可疑
            patterns.append({
                "rule_name": "数字异常模式",
                "risk_value": 10,
                "detection_method": "pattern_analysis",
                "description": "文本中数字过多，可能存在虚假信息"
            })
            risk_score += 10
        
        # 2. 重复信息检测
        words = text.split()
        word_freq = {}
        for word in words:
            if len(word) > 2:  # 只统计长度>2的词
                word_freq[word] = word_freq.get(word, 0) + 1
        
        repeated_words = [word for word, freq in word_freq.items() if freq > 3]
        if repeated_words:
            patterns.append({
                "rule_name": "重复信息模式",
                "risk_value": 5,
                "detection_method": "pattern_analysis",
                "description": f"存在重复词汇: {', '.join(repeated_words[:3])}"
            })
            risk_score += 5
        
        # 3. 矛盾信息检测
        contradictions = []
        if "未婚" in text and "离异" in text:
            contradictions.append("婚姻状态矛盾")
        if "独生子" in text and "兄弟" in text:
            contradictions.append("家庭结构矛盾")
        
        if contradictions:
            patterns.append({
                "rule_name": "信息矛盾模式",
                "risk_value": 15,
                "detection_method": "pattern_analysis",
                "description": f"信息存在矛盾: {', '.join(contradictions)}"
            })
            risk_score += 15
        
        return {
            "risk_score": risk_score,
            "pattern_rules": patterns
        }
    
    async def generate_verification_tactics(self, triggered_rules: List[Dict], ai_analysis: Dict = None) -> List[Dict]:
        """生成验证话术（扁平化错误处理版本）"""
        print(f"🤖 开始生成验证话术")
        print(f"📋 触发规则数量: {len(triggered_rules)}")
        
        start_time = time.time()
        tactics = []
        
        # 1. 基于AI分析生成话术
        if ai_analysis and ai_analysis.get("verification_suggestions"):
            suggestions = ai_analysis["verification_suggestions"]
            print(f"📝 找到{len(suggestions)}条AI建议")
            for suggestion in suggestions:
                tactics.append({
                    "rule_name": "AI智能建议",
                    "tactic": suggestion,
                    "knowledge": "AI分析生成",
                    "priority": "high"
                })
            print(f"✅ 添加了{len(suggestions)}条AI建议话术")
        
        # 2. 批量生成所有规则的话术
        print(f"🚀 开始批量生成所有规则话术")
        
        # 构建统一的批量prompt - 只保留必要字段
        all_rules_info = []
        for rule in triggered_rules:
            rule_info = {
                "rule_name": rule.get("rule_name", ""),
                "keywords": rule.get("keywords", [])
            }
            all_rules_info.append(rule_info)
        
        print(f"📊 准备批量处理{len(all_rules_info)}条规则")
        
        # 构建简化的批量prompt
        prompt = f"""
为以下风险规则生成验证问题，要求自然委婉：
规则：{json.dumps(all_rules_info, ensure_ascii=False, indent=2)}
返回JSON：{{"tactics": [{{"rule_name": "规则名", "tactic": "验证问题", "priority": "high"}}]}}
"""
        
        print(f"📤 开始调用DeepSeek API，批量处理{len(all_rules_info)}条规则")
        
        # 调用AI API
        try:
            result = await self.deepseek_service.generate_verification_tactic(
                "批量话术生成", {"prompt": prompt}
            )
            print(f"✅ 批量AI话术生成成功: {result}")
        except Exception as e:
            print(f"❌ AI API调用失败: {e}")
            print(f"📋 异常堆栈: {traceback.format_exc()}")
            # 快速失败，使用默认话术
            default_tactics = self._generate_default_tactics(triggered_rules)
            tactics.extend(default_tactics)
            print(f"✅ 使用默认话术，共{len(default_tactics)}条")
            return tactics
        
        # 解析AI结果
        parsed_result = self._parse_ai_result(result)
        if not parsed_result:
            print(f"❌ AI结果解析失败，使用默认话术")
            default_tactics = self._generate_default_tactics(triggered_rules)
            tactics.extend(default_tactics)
            return tactics
        
        # 验证话术
        ai_tactics = parsed_result.get("tactics", [])
        if not self._validate_tactics(ai_tactics, len(triggered_rules)):
            print(f"❌ 话术验证失败，使用默认话术")
            default_tactics = self._generate_default_tactics(triggered_rules)
            tactics.extend(default_tactics)
            return tactics
        
        # 转换话术格式
        standard_tactics = self._convert_tactics_to_standard(ai_tactics, triggered_rules)
        tactics.extend(standard_tactics)
        
        # 3. 如果没有检测到规则，生成通用验证话术
        if not tactics:
            print(f"⚠️ 没有生成任何话术，使用通用话术")
            tactics.append({
                "rule_name": "通用验证",
                "tactic": "请详细描述一下您的工作内容和日常安排，这样我们可以更好地了解彼此。",
                "knowledge": "通用验证话术",
                "priority": "medium"
            })
        
        total_time = time.time() - start_time
        print(f"⏱️ 话术生成总耗时: {total_time:.2f}秒")
        print(f"🎉 话术生成完成，总共{len(tactics)}条")
        
        return tactics
    
    def _parse_ai_result(self, result: str) -> Optional[Dict]:
        """解析AI结果，失败立即返回None"""
        try:
            # 清理markdown代码块标记
            cleaned_result = result.strip()
            if cleaned_result.startswith('```json'):
                cleaned_result = cleaned_result[7:]
            if cleaned_result.endswith('```'):
                cleaned_result = cleaned_result[:-3]
            cleaned_result = cleaned_result.strip()
            
            # 解析JSON
            parsed_result = json.loads(cleaned_result)
            print(f"✅ AI结果解析成功: {parsed_result}")
            return parsed_result
            
        except Exception as e:
            print(f"❌ AI结果解析失败: {e}")
            print(f"📋 原始结果: {result}")
            return None
    
    def _validate_tactics(self, ai_tactics: List[Dict], expected_count: int) -> bool:
        """验证AI返回的话术数量是否正确"""
        if not ai_tactics:
            print(f"❌ AI返回话术为空")
            return False
        
        if len(ai_tactics) != expected_count:
            print(f"⚠️ AI返回话术数量不匹配: 期望{expected_count}条，实际{len(ai_tactics)}条")
            return False
        
        # 验证每条话术的必要字段
        for i, tactic in enumerate(ai_tactics):
            if not tactic.get("rule_name") or not tactic.get("tactic"):
                print(f"❌ 第{i+1}条话术字段缺失: {tactic}")
                return False
        
        print(f"✅ 话术验证通过: {len(ai_tactics)}条")
        return True
    
    def _convert_tactics_to_standard(self, ai_tactics: List[Dict], triggered_rules: List[Dict]) -> List[Dict]:
        """将AI话术转换为标准格式"""
        standard_tactics = []
        
        for tactic in ai_tactics:
            rule_name = tactic.get("rule_name", "")
            tactic_text = tactic.get("tactic", "")
            priority = tactic.get("priority", "medium")
            
            # 找到对应的规则信息
            rule_info = next((r for r in triggered_rules if r.get("rule_name") == rule_name), {})
            
            standard_tactics.append({
                "rule_name": rule_name,
                "tactic": tactic_text,
                "knowledge": rule_info.get("description", "AI生成话术"),
                "priority": priority
            })
        
        print(f"✅ 话术转换完成: {len(standard_tactics)}条")
        return standard_tactics
    
    async def _generate_batch_ai_tactics(self, ai_rules: List[Dict]) -> List[Dict]:
        """批量生成AI检测规则的话术（优化性能）"""
        start_time = time.time()
        print(f"🤖 开始批量生成AI话术，规则数量: {len(ai_rules)}")
        
        try:
            # 构建批量prompt - 一次性发送所有规则
            prompt_start = time.time()
            
            # 构建完整的规则信息
            rules_info = []
            for rule in ai_rules:
                rules_info.append({
                    "rule_name": rule.get("rule_name", ""),
                    "description": rule.get("description", ""),
                    "risk_value": rule.get("risk_value", 0),
                    "matched_rule": rule.get("matched_rule", "")
                })
            
            # 优化提示词，让AI一次性处理所有规则
            prompt = f"""
你是一个专业的风险验证专家，请为以下风险规则生成自然的验证问题。

规则信息：
{json.dumps(rules_info, ensure_ascii=False, indent=2)}

要求：
1. 每个问题要自然，像朋友聊天一样，不能太直接
2. 要能验证对方是否真的了解这个领域
3. 语言要委婉，避免直接质疑
4. 针对具体的风险点进行验证
5. 必须一次性生成所有规则的话术，不能遗漏

请返回JSON格式，包含每个规则的话术：
{{
    "tactics": [
        {{
            "rule_name": "规则名称",
            "tactic": "验证问题",
            "description": "话术说明"
        }}
    ]
}}

重要提醒：必须为每个规则生成话术，返回的tactics数组长度必须等于输入规则数量！
"""
            
            prompt_time = time.time() - prompt_start
            print(f"⏱️ Prompt构建耗时: {prompt_time:.2f}秒")
            print(f"📋 批量发送规则数量: {len(rules_info)}")
            
            # 一次性调用AI API，发送所有规则
            api_start = time.time()
            print(f"🌐 开始调用DeepSeek API，批量处理{len(ai_rules)}条规则")
            
            result = await self.deepseek_service.generate_verification_tactic(
                "批量话术生成", {"prompt": prompt}
            )
            
            api_time = time.time() - api_start
            print(f"⏱️ AI API调用耗时: {api_time:.2f}秒")
            print(f"✅ 批量AI话术生成成功: {result}")
            
            # 解析返回结果
            parse_start = time.time()
            try:
                # 清理markdown代码块标记
                cleaned_result = result.strip()
                if cleaned_result.startswith('```json'):
                    cleaned_result = cleaned_result[7:]
                if cleaned_result.endswith('```'):
                    cleaned_result = cleaned_result[:-3]
                cleaned_result = cleaned_result.strip()
                
                parsed_result = json.loads(cleaned_result)
                tactics = parsed_result.get("tactics", [])
                
                # 验证返回的话术数量是否正确
                if len(tactics) != len(ai_rules):
                    print(f"⚠️ AI返回话术数量不匹配: 期望{len(ai_rules)}条，实际{len(tactics)}条")
                    print(f"📋 AI返回结果: {tactics}")
                    # 如果数量不匹配，使用默认话术
                    return self._generate_default_tactics(ai_rules)
                
                # 转换为标准格式
                result_tactics = []
                for i, tactic in enumerate(tactics):
                    rule_name = tactic.get("rule_name", "")
                    tactic_text = tactic.get("tactic", "")
                    
                    # 如果没有话术内容，使用默认话术
                    if not tactic_text:
                        print(f"⚠️ 规则'{rule_name}'的话术为空，使用默认话术")
                        default_tactic = self._generate_default_tactic_for_rule(ai_rules[i])
                        result_tactics.append(default_tactic)
                    else:
                        result_tactics.append({
                            "rule_name": rule_name,
                            "tactic": tactic_text,
                            "knowledge": tactic.get("description", "AI分析生成"),
                            "priority": "high"
                        })
                
                parse_time = time.time() - parse_start
                print(f"⏱️ 结果解析耗时: {parse_time:.2f}秒")
                
                total_time = time.time() - start_time
                print(f"⏱️ 批量话术生成总耗时: {total_time:.2f}秒")
                print(f"✅ 成功生成{len(result_tactics)}条话术")
                
                return result_tactics
                
            except json.JSONDecodeError as e:
                print(f"❌ 批量话术JSON解析失败: {e}")
                print(f"📋 原始返回内容: {result}")
                return self._generate_default_tactics(ai_rules)
                
        except Exception as e:
            print(f"❌ 批量AI话术生成失败: {e}")
            import traceback
            print(f"📋 异常堆栈: {traceback.format_exc()}")
            total_time = time.time() - start_time
            print(f"⏱️ 批量话术生成失败，总耗时: {total_time:.2f}秒")
            return self._generate_default_tactics(ai_rules)
    
    def _generate_default_tactic_for_rule(self, rule: Dict) -> Dict:
        """为单个规则生成默认话术"""
        rule_name = rule.get("rule_name", "")
        if "职业" in rule_name:
            tactic = "能否详细介绍一下您的工作内容和公司情况？"
        elif "收入" in rule_name or "学历" in rule_name:
            tactic = "能否具体说明一下您的收入来源和学历背景？"
        elif "家庭" in rule_name:
            tactic = "能否详细介绍一下您的家庭情况？"
        elif "资产" in rule_name:
            tactic = "能否具体说明一下您的资产状况？"
        else:
            tactic = f"请详细说明一下关于{rule_name}的具体情况，这样我们可以更好地了解。"
        
        return {
            "rule_name": rule_name,
            "tactic": tactic,
            "knowledge": "默认话术",
            "priority": "medium"
        }
    
    def _generate_default_tactics(self, ai_rules: List[Dict]) -> List[Dict]:
        """生成默认话术（备用方案）"""
        tactics = []
        for rule in ai_rules:
            tactic = self._generate_default_tactic_for_rule(rule)
            tactics.append(tactic)
        return tactics
    
    async def _generate_ai_tactic(self, rule_name: str, rule_info: Dict) -> str:
        """生成AI检测规则的话术"""
        try:
            prompt = f"""
            基于以下AI检测结果，生成一个自然的验证问题：
            
            检测规则：{rule_name}
            风险描述：{rule_info.get('description', '')}
            风险值：{rule_info.get('risk_value', 0)}
            
            要求：
            1. 问题要自然，不能太直接
            2. 要能验证对方是否真的了解这个领域
            3. 语言要像朋友聊天一样自然
            4. 针对具体的风险点进行验证
            
            请生成一个验证问题：
            """
            
            print(f"🤖 开始生成AI话术，规则: {rule_name}")
            result = await self.deepseek_service.generate_verification_tactic(
                rule_name, {"prompt": prompt}
            )
            print(f"✅ AI话术生成成功: {result}")
            return result
        except Exception as e:
            print(f"❌ AI话术生成失败: {e}")
            # 返回更具体的默认话术
            if "职业" in rule_name:
                return "能否详细介绍一下您的工作内容和公司情况？"
            elif "收入" in rule_name or "学历" in rule_name:
                return "能否具体说明一下您的收入来源和学历背景？"
            elif "家庭" in rule_name:
                return "能否详细介绍一下您的家庭情况？"
            else:
                return f"请详细说明一下关于{rule_name}的具体情况，这样我们可以更好地了解。"
    
    async def _generate_pattern_tactic(self, rule_name: str, rule_info: Dict) -> str:
        """生成模式检测规则的话术"""
        description = rule_info.get('description', '')
        
        if "数字异常" in rule_name:
            return "您提到的这些数字信息很详细，能否具体说明一下这些数字的来源和含义？"
        elif "重复信息" in rule_name:
            return "我注意到您提到了一些重复的信息，能否重新整理一下，避免重复？"
        elif "信息矛盾" in rule_name:
            return "您提供的信息中似乎有一些不一致的地方，能否澄清一下？"
        else:
            return f"关于{rule_name}，能否提供更详细的信息来验证？"
    
    async def _generate_standard_tactic(self, rule_name: str, rule_info: Dict) -> str:
        """生成标准规则的话术"""
        # 从知识库选择相关条目
        knowledge_item = self._select_knowledge_item(rule_name)
        
        # 生成话术
        tactic = await self.deepseek_service.generate_verification_tactic(
            rule_name, knowledge_item
        )
        return tactic
    
    def _select_knowledge_item(self, rule_name: str) -> Dict[str, str]:
        """选择知识库条目"""
        # 根据规则名称匹配知识库
        if "职业" in rule_name or "金融" in rule_name:
            knowledge_key = "finance_policies"
        elif "医疗" in rule_name or "医保" in rule_name:
            knowledge_key = "medical_policies"
        else:
            knowledge_key = "finance_policies"  # 默认使用金融政策
        
        if knowledge_key in self.knowledge_base and self.knowledge_base[knowledge_key]:
            return random.choice(self.knowledge_base[knowledge_key])
        
        # 返回默认知识
        return {
            "政策名称": "相关政策",
            "影响行业": "相关行业",
            "关键条款": "重要条款"
        }
    
    async def analyze_response(self, response_text: str) -> Dict:
        """分析用户回答"""
        return await self.deepseek_service.analyze_response_risk(response_text)
    
    def make_decision(self, static_score: int, dynamic_score: int) -> Dict:
        """决策引擎"""
        # 获取权重配置
        static_weight = self.weight_config.get("decision_engine", {}).get("static_weight", 0.6)
        dynamic_weight = self.weight_config.get("decision_engine", {}).get("dynamic_weight", 0.4)
        
        # 计算总分
        total_score = static_score * static_weight + dynamic_score * dynamic_weight
        
        # 获取阈值配置
        terminate_threshold = self.weight_config.get("risk_levels", {}).get("terminate", 75)
        warning_threshold = self.weight_config.get("risk_levels", {}).get("warning", 40)
        
        # 决策
        if total_score >= terminate_threshold:
            decision = "TERMINATE"
            risk_level = "高风险"
        elif total_score >= warning_threshold:
            decision = "WARNING"
            risk_level = "中风险"
        else:
            decision = "PASS"
            risk_level = "低风险"
        
        return {
            "decision": decision,
            "risk_level": risk_level,
            "total_score": round(total_score, 2),
            "static_score": static_score,
            "dynamic_score": dynamic_score,
            "static_weight": static_weight,
            "dynamic_weight": dynamic_weight,
            "terminate_threshold": terminate_threshold,
            "warning_threshold": warning_threshold
        }
    
    async def full_risk_analysis(
        self, 
        input_text: str, 
        user_response: str = None
    ) -> Dict:
        """完整风控分析流程"""
        print(f"🚀 开始完整风控分析流程")
        print(f"📝 输入文本: {input_text[:50]}...")
        print(f"💬 用户回答: {user_response if user_response else '无'}")
        
        # 1. 静态风险扫描
        print(f"🔍 步骤1: 开始静态风险扫描")
        static_result = await self.static_risk_scan(input_text)
        print(f"✅ 静态扫描完成: {static_result}")
        
        # 2. 生成验证话术
        print(f"🤖 步骤2: 开始生成验证话术")
        print(f"📋 触发规则数量: {len(static_result.get('rules', []))}")
        print(f"📋 AI分析结果: {static_result.get('ai_analysis', {})}")
        
        try:
            tactics = await self.generate_verification_tactics(static_result["rules"], static_result["ai_analysis"])
            print(f"✅ 话术生成完成: {tactics}")
        except Exception as e:
            print(f"❌ 话术生成失败: {e}")
            import traceback
            print(f"📋 异常堆栈: {traceback.format_exc()}")
            tactics = []
        
        # 3. 动态分析（如果有用户回答）
        dynamic_result = None
        if user_response:
            print(f"💬 步骤3: 开始动态分析用户回答")
            try:
                dynamic_result = await self.analyze_response(user_response)
                print(f"✅ 动态分析完成: {dynamic_result}")
            except Exception as e:
                print(f"❌ 动态分析失败: {e}")
                dynamic_result = None
        
        # 4. 决策
        print(f"🎯 步骤4: 开始决策分析")
        try:
            decision_result = self.make_decision(
                static_result["score"],
                dynamic_result["overall_risk_score"] if dynamic_result else 0
            )
            print(f"✅ 决策分析完成: {decision_result}")
        except Exception as e:
            print(f"❌ 决策分析失败: {e}")
            decision_result = {"decision": "ERROR", "risk_level": "分析失败", "total_score": 0}
        
        # 5. 构建证据链
        print(f"🔗 步骤5: 构建证据链")
        evidence_chain = []
        try:
            for rule in static_result.get("rules", []):
                keywords = rule.get('keywords', [])
                if keywords:
                    evidence_chain.append(f"静态：{rule['rule_name']}（{', '.join(keywords)}）")
                else:
                    evidence_chain.append(f"静态：{rule['rule_name']}")
            
            if dynamic_result and dynamic_result.get("risk_tags"):
                for tag in dynamic_result["risk_tags"]:
                    if tag:
                        evidence_chain.append(f"动态：{tag}")
            
            print(f"✅ 证据链构建完成: {evidence_chain}")
        except Exception as e:
            print(f"❌ 证据链构建失败: {e}")
            evidence_chain = ["证据链构建失败"]
        
        # 6. 生成时间戳
        print(f"⏰ 步骤6: 生成时间戳")
        try:
            if PANDAS_AVAILABLE:
                timestamp = pd.Timestamp.now().isoformat()
            else:
                timestamp = datetime.now().isoformat()
            print(f"✅ 时间戳生成: {timestamp}")
        except Exception as e:
            print(f"❌ 时间戳生成失败: {e}")
            timestamp = "时间戳生成失败"
        
        # 7. 构建最终结果
        print(f"📦 步骤7: 构建最终结果")
        final_result = {
            "version": "1.0",
            "input_text": input_text,
            "static_scan": static_result,
            "verification_tactics": tactics,
            "dynamic_session": dynamic_result,
            "decision": decision_result,
            "evidence_chain": evidence_chain,
            "timestamp": timestamp
        }
        
        print(f"🎉 完整风控分析流程完成")
        print(f"📤 返回结果: {final_result}")
        return final_result
    
    def _generate_default_tactics(self, rules: List[Dict]) -> List[Dict]:
        """生成默认话术（备用方案）"""
        tactics = []
        for rule in rules:
            rule_name = rule.get("rule_name", "")
            if "职业" in rule_name:
                tactic = "能否详细介绍一下您的工作内容和公司情况？"
            elif "收入" in rule_name or "学历" in rule_name:
                tactic = "能否具体说明一下您的收入来源和学历背景？"
            elif "家庭" in rule_name:
                tactic = "能否详细介绍一下您的家庭情况？"
            elif "资产" in rule_name:
                tactic = "能否具体说明一下您的资产状况？"
            else:
                tactic = f"请详细说明一下关于{rule_name}的具体情况，这样我们可以更好地了解。"
            
            tactics.append({
                "rule_name": rule_name,
                "tactic": tactic,
                "knowledge": "默认话术",
                "priority": "medium"
            })
        return tactics
