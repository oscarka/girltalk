import httpx
import json
from typing import Dict, List, Optional
from app.core.config import settings

class DeepSeekService:
    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.api_base = settings.deepseek_api_base
        self.model = settings.deepseek_model
        self.max_tokens = settings.deepseek_max_tokens
        
        if not self.api_key:
            raise ValueError("DeepSeek API密钥未配置")
    
    async def generate_verification_tactic(
        self, 
        rule_name: str, 
        knowledge_item: Dict[str, str]
    ) -> str:
        """生成验证话术"""
        print(f"🤖 DeepSeek服务: 开始生成话术")
        print(f"📋 规则名称: {rule_name}")
        print(f"📚 知识信息: {knowledge_item}")
        
        # 如果是AI风险分析，使用特殊处理
        if rule_name == "AI风险分析":
            prompt = knowledge_item.get("prompt", "")
            print(f"📤 使用AI风险分析prompt，长度: {len(prompt)}")
        else:
            prompt = f"""
            基于以下信息生成一个自然的验证问题，要求：
            1. 问题要自然，不能太直接
            2. 要能验证对方是否真的了解这个领域
            3. 语言要像朋友聊天一样自然
            
            规则名称：{rule_name}
            知识信息：{json.dumps(knowledge_item, ensure_ascii=False)}
            
            请生成一个验证问题：
            """
            print(f"📤 使用标准prompt，长度: {len(prompt)}")
        
        try:
            print(f"🌐 准备调用DeepSeek API")
            print(f"🔑 API密钥: {self.api_key[:10]}...")
            print(f"🌍 API地址: {self.api_base}")
            print(f"🤖 模型: {self.model}")
            
            async with httpx.AsyncClient() as client:
                request_data = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": self.max_tokens,
                    "temperature": 0.7
                }
                
                print(f"📤 发送请求数据: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
                
                response = await client.post(
                    f"{self.api_base}/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=request_data,
                    timeout=30.0
                )
                
                print(f"📥 收到响应，状态码: {response.status_code}")
                print(f"📋 响应头: {dict(response.headers)}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ API调用成功，响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                    
                    content = result["choices"][0]["message"]["content"].strip()
                    print(f"📝 提取的内容: {content}")
                    return content
                else:
                    print(f"❌ API调用失败: {response.status_code}")
                    print(f"📋 错误响应: {response.text}")
                    return self._fallback_tactic(rule_name, knowledge_item)
                    
        except Exception as e:
            print(f"❌ DeepSeek API调用异常: {e}")
            import traceback
            print(f"📋 异常堆栈: {traceback.format_exc()}")
            return self._fallback_tactic(rule_name, knowledge_item)
    
    async def analyze_response_risk(self, response_text: str, verification_tactics: List[Dict] = None) -> Dict[str, any]:
        """分析用户回答的风险特征"""
        
        # 构建验证问题信息
        tactics_info = ""
        if verification_tactics:
            tactics_info = "\n## 验证问题及目的：\n"
            for i, tactic in enumerate(verification_tactics, 1):
                rule_name = tactic.get('rule_name', '未知规则')
                tactic_text = tactic.get('tactic', '')
                tactics_info += f"{i}. 问题：\"{tactic_text}\"\n"
                tactics_info += f"   目的：验证{rule_name}相关信息的真实性\n\n"
        
        prompt = f"""
        你是一个专业的风险分析专家，需要分析用户对验证问题的回答。

        {tactics_info}
        ## 用户回答：
        {response_text}

        请基于用户对上述验证问题的回答，从以下5个维度进行评分（0-100分）：

        1. fuzzy_evasion（模糊回避程度）：
           - 0分：回答具体、明确、信息充分
           - 25分：使用模糊词汇（大概、可能、不清楚等）
           - 50分：部分回避，信息不完整
           - 75分：大量模糊词汇，明显回避
           - 100分：完全回避，无有效信息

        2. emotional_attack（情绪攻击程度）：
           - 0分：态度友好，配合回答
           - 25分：轻微抵触，语气变化
           - 50分：明显防御，质疑动机
           - 75分：强烈抵触，攻击性语言
           - 100分：完全对抗，拒绝配合

        3. topic_shift（话题转移程度）：
           - 0分：专注当前话题，不转移
           - 25分：轻微转移，但会回到主题
           - 50分：明显转移，回避问题
           - 75分：频繁转移，难以控制
           - 100分：完全转移，拒绝讨论

        4. precise_answer（精准回答程度）：
           - 0分：完全偏离问题，无相关信息
           - 25分：部分相关，但不够精准
           - 50分：基本相关，信息一般
           - 75分：相关且具体，信息较好
           - 100分：完全精准，信息充分

        5. risk_tags（风险标签）：
           根据上述分析，生成2-4个风险标签，如：模糊回避、情绪攻击、话题转移、信息不足等

        6. overall_risk_score（总体风险评分）：
           综合考虑上述4个维度，给出0-100分的总体风险评分

        请严格按照以下JSON格式返回，不要有其他文字：
        {{
            "fuzzy_evasion": 分数,
            "emotional_attack": 分数,
            "topic_shift": 分数,
            "precise_answer": 分数,
            "risk_tags": ["标签1", "标签2"],
            "overall_risk_score": 分数
        }}
        """
        
        try:
            print(f"🌐 准备调用DeepSeek API进行动态分析")
            print(f"🔑 API密钥: {self.api_key[:10]}...")
            print(f"📤 用户回答: {response_text}")
            
            async with httpx.AsyncClient() as client:
                request_data = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": self.max_tokens,
                    "temperature": 0.3
                }
                
                print(f"📤 发送动态分析请求")
                
                response = await client.post(
                    f"{self.api_base}/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=request_data,
                    timeout=30.0
                )
                
                print(f"📥 收到响应，状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ 动态分析API调用成功")
                    content = result["choices"][0]["message"]["content"].strip()
                    print(f"📝 AI返回的原始内容: {content}")
                    
                    # 尝试解析JSON，处理可能被代码块包裹的情况
                    try:
                        # 如果内容被```json```包裹，先提取出来
                        if content.startswith("```json") and content.endswith("```"):
                            content = content[7:-3].strip()  # 移除```json和```
                            print(f"🧹 移除JSON代码块标记后: {content}")
                        elif content.startswith("```") and content.endswith("```"):
                            content = content[3:-3].strip()  # 移除```和```
                            print(f"🧹 移除代码块标记后: {content}")
                        
                        analysis = json.loads(content)
                        print(f"✅ 动态分析JSON解析成功: {analysis}")
                        return analysis
                    except json.JSONDecodeError:
                        print(f"❌ 动态分析JSON解析失败: {content}")
                        return self._fallback_analysis(response_text)
                else:
                    print(f"❌ 动态分析API调用失败: {response.status_code}")
                    print(f"📋 错误响应: {response.text}")
                    return self._fallback_analysis(response_text)
                    
        except Exception as e:
            print(f"DeepSeek API调用异常: {e}")
            return self._fallback_analysis(response_text)
    
    def _fallback_tactic(self, rule_name: str, knowledge_item: Dict[str, str]) -> str:
        """备用话术生成"""
        industry = knowledge_item.get("影响行业", "相关行业")
        policy = knowledge_item.get("政策名称", "新政策")
        clause = knowledge_item.get("关键条款", "重要条款")
        
        return f"听说{industry}最近{policy}变化很大，{clause}，您有了解吗？"
    
    def _fallback_analysis(self, response_text: str) -> Dict[str, any]:
        """备用风险分析"""
        # 扩展的关键词匹配分析
        fuzzy_words = ["大概", "可能", "不清楚", "不太确定", "应该吧", "不知道", "忘了", "记不清", "说不准"]
        attack_words = ["现实", "查户口", "太物质", "问太细", "商业机密", "不想说", "不方便", "隐私"]
        topic_shift_words = ["换个话题", "说点别的", "这个不重要", "先不说这个"]
        
        # 计算各项分数
        fuzzy_score = sum(25 for word in fuzzy_words if word in response_text)
        attack_score = sum(40 for word in attack_words if word in response_text)
        topic_shift_score = sum(30 for word in topic_shift_words if word in response_text)
        
        # 如果回答太短（少于5个字），增加模糊回避分数
        if len(response_text.strip()) < 5:
            fuzzy_score += 20
        
        # 如果回答包含否定词，增加模糊回避分数
        negative_words = ["不", "没", "无", "否", "别", "莫"]
        if any(word in response_text for word in negative_words):
            fuzzy_score += 15
        
        # 计算精准回答分数（反向计算，但确保不为负数）
        total_risk = fuzzy_score + attack_score + topic_shift_score
        precise_score = max(0, 100 - total_risk)
        
        # 计算总体风险分数
        overall_score = min(total_risk, 100)
        
        # 生成风险标签
        risk_tags = []
        if fuzzy_score > 0:
            risk_tags.append("模糊回避")
        if attack_score > 0:
            risk_tags.append("情绪攻击")
        if topic_shift_score > 0:
            risk_tags.append("话题转移")
        if precise_score < 50:
            risk_tags.append("信息不足")
        
        return {
            "fuzzy_evasion": min(fuzzy_score, 100),
            "emotional_attack": min(attack_score, 100),
            "topic_shift": min(topic_shift_score, 100),
            "precise_answer": max(precise_score, 0),
            "risk_tags": [tag for tag in risk_tags if tag],
            "overall_risk_score": overall_score
        }
