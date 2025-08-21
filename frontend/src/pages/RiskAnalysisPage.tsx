import React, { useState, useEffect, useCallback, useRef } from 'react'
import { flushSync } from 'react-dom'
import { useNavigate } from 'react-router-dom'
import {
  Button,
  Card,
  Space,
  Tag,
  Toast,
  Loading
} from 'antd-mobile'
import {
  LeftOutline,
  PlayOutline,
  SendOutline,
  CheckShieldOutline
} from 'antd-mobile-icons'
import { riskAnalysisAPI } from '../services/api'
import './RiskAnalysisPage.css'

interface RiskResult {
  score: number
  rules: any[]
  total_rules: number
  verification_tactics?: any[]
  decision?: any
  evidence_chain?: string[]
  ai_analysis?: {
    risk_reasons?: string[];
    verification_suggestions?: string[];
  };
  static_scan?: {
    score: number;
  };
}

const RiskAnalysisPage: React.FC = () => {
  const navigate = useNavigate()
  const [inputText, setInputText] = useState('')
  const [userResponse, setUserResponse] = useState('')
  const [riskResult, setRiskResult] = useState<RiskResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [stepLoading, setStepLoading] = useState(false)
  const [step, setStep] = useState<'input' | 'tactics' | 'response' | 'result'>('input')

  // 使用useRef追踪stepLoading状态变化，避免闭包问题
  const stepLoadingRef = useRef(stepLoading)
  stepLoadingRef.current = stepLoading

  // 监听stepLoading状态变化
  useEffect(() => {
    console.log('🔍 useEffect: stepLoading状态变化 ->', stepLoading)
    console.log('🔍 useEffect: 当前时间戳:', Date.now())
    console.log('🔍 useEffect: 调用栈:', new Error().stack?.split('\n').slice(1, 4).join('\n'))

    // 追踪状态变化的原因
    if (stepLoading === false) {
      console.log('🚨 警告: stepLoading被设置为false!')
      console.log('🚨 当前调用栈:', new Error().stack?.split('\n').slice(1, 6).join('\n'))

      // 检查是否有其他状态变化
      console.log('🚨 当前所有状态值:')
      console.log('🚨 - step:', step)
      console.log('🚨 - loading:', loading)
      console.log('🚨 - inputText长度:', inputText.length)
      console.log('🚨 - riskResult存在:', !!riskResult)
    }
  }, [stepLoading, step, loading, inputText, riskResult])

  // 监听step状态变化
  useEffect(() => {
    console.log('🔍 useEffect: step状态变化 ->', step)
  }, [step])

  // 示例文本
  const examples = [
    '男，1988，某私募MD，年薪500万+，有房贷，父母农村无医保',
    '女，1992，某知名企业总监，月薪3万，有车无房，父母退休',
    '男，1990，某银行VP，年薪200万，有房有车，家庭条件一般'
  ]

  const handleExampleClick = (example: string) => {
    setInputText(example)
  }

  const handleStaticScan = useCallback(async () => {
    if (!inputText.trim()) {
      Toast.show('请输入要分析的文本')
      return
    }

    // 立即显示加载动画
    console.log('🔄 立即显示步骤切换加载动画')
    flushSync(() => {
      setStepLoading(true)
    })
    console.log('📊 设置stepLoading为true，立即显示加载动画')

    setLoading(true)
    try {
      console.log('🚀 开始调用静态扫描API')
      const response = await riskAnalysisAPI.staticScan(inputText)
      console.log('📡 API响应:', response)

      if ((response as any).success) {
        console.log('✅ API调用成功，开始设置状态')
        setRiskResult((response as any).data)

        // 显示Toast，然后延迟跳转
        console.log('🍞 显示Toast消息')
        Toast.show('静态扫描完成')

        // 延迟跳转，确保加载动画有足够时间显示
        setTimeout(() => {
          console.log('✅ 步骤切换完成，跳转到话术生成')
          console.log('📊 跳转前stepLoading状态:', stepLoading)
          setStep('tactics')
          // 跳转后再关闭加载动画
          setTimeout(() => {
            console.log('🚨 即将设置stepLoading为false (第1个位置 - handleStaticScan)')
            console.log('🚨 调用栈:', new Error().stack?.split('\n').slice(1, 4).join('\n'))
            setStepLoading(false)
            console.log('📊 跳转后关闭加载动画')
          }, 100)
        }, 1000)
      }
    } catch (error) {
      Toast.show('分析失败，请重试')
      console.error('Static scan error:', error)
    } finally {
      setLoading(false)
    }
  }, [inputText])

  const handleGenerateTactics = async () => {
    if (!riskResult) return

    console.log('🚀 开始生成验证话术')
    console.log('📋 当前风险结果:', riskResult)

    // 检查是否已有话术（注意：static-scan返回的是AI提示，不是最终话术）
    if (riskResult.verification_tactics && riskResult.verification_tactics.length > 0) {
      console.log('✅ 检测到已有话术，直接使用，避免重复调用API')
      console.log('📝 话术数量:', riskResult.verification_tactics.length)

      // 显示Toast，然后延迟跳转
      Toast.show('话术已生成，无需重复调用')

      setTimeout(() => {
        console.log('✅ 步骤切换完成，跳转到用户回答')
        setStep('response')
      }, 1000)
      return
    }

    // 检查是否有AI分析结果和提示
    if (riskResult.ai_analysis && riskResult.ai_analysis.verification_suggestions) {
      console.log('📝 检测到AI分析提示，需要基于提示生成话术')
      console.log('📝 AI提示数量:', riskResult.ai_analysis.verification_suggestions.length)
    } else {
      console.log('⚠️ 未检测到AI分析提示，无法生成话术')
      Toast.show('缺少AI分析结果，无法生成话术')
      return
    }

    // 如果没有话术，需要调用API生成
    console.log('⚠️ 未检测到话术，需要调用API生成')

    // 立即显示加载动画
    console.log('🔄 立即显示步骤切换加载动画')
    flushSync(() => {
      setStepLoading(true)
    })
    console.log('📊 设置stepLoading为true，立即显示加载动画')

    setLoading(true)
    const startTime = Date.now()

    try {
      console.log('📤 准备调用 generateTactics API')
      console.log('📝 输入文本:', inputText)

      console.log('⏰ API调用开始时间:', new Date(startTime).toISOString())

      const response = await riskAnalysisAPI.generateTactics(
        inputText,
        riskResult.rules,
        riskResult.ai_analysis
      )

      const endTime = Date.now()
      const duration = endTime - startTime
      console.log('⏰ API调用完成时间:', new Date(endTime).toISOString())
      console.log('⏱️ API调用耗时:', duration, 'ms')
      console.log('✅ API调用成功:', response)

      if (response && (response as any).success) {
        console.log('🎉 话术生成成功，更新风险结果')
        setRiskResult((response as any).data)
        // 显示Toast，然后延迟跳转
        console.log('🍞 显示Toast消息')
        Toast.show('话术生成完成')

        setTimeout(() => {
          console.log('✅ 步骤切换完成，跳转到用户回答')
          setStep('response')
          // 跳转后再关闭加载动画
          setTimeout(() => {
            console.log('🚨 即将设置stepLoading为false (第2个位置 - handleGenerateTactics)')
            console.log('🚨 调用栈:', new Error().stack?.split('\n').slice(1, 4).join('\n'))
            setStepLoading(false)
            console.log('📊 跳转后关闭加载动画')
          }, 100)
        }, 1000)
        console.log('📋 更新后的风险结果:', (response as any).data)
      } else {
        console.log('❌ API返回失败:', response)
        Toast.show('话术生成失败，请重试')
      }
    } catch (error: any) {
      const errorTime = Date.now()
      const totalDuration = errorTime - startTime
      console.error('❌ 话术生成异常:', error)
      console.error('⏱️ 总耗时:', totalDuration, 'ms')
      console.error('📋 错误详情:', {
        name: error?.name,
        message: error?.message,
        code: error?.code,
        config: error?.config,
        request: error?.request
      })

      if (error?.code === 'ECONNABORTED') {
        Toast.show('话术生成超时，请重试')
      } else {
        Toast.show('话术生成失败，请重试')
      }
    } finally {
      setLoading(false)
      console.log('🏁 话术生成流程结束')
    }
  }

  const handleAnalyzeResponse = async () => {
    if (!userResponse.trim()) {
      Toast.show('请输入用户回答')
      return
    }

    // 立即显示加载动画
    console.log('🔄 立即显示步骤切换加载动画')
    flushSync(() => {
      setStepLoading(true)
    })
    console.log('📊 设置stepLoading为true，立即显示加载动画')

    setLoading(true)
    try {
      const response = await riskAnalysisAPI.fullAnalysis(inputText, userResponse)
      if ((response as any).success) {
        setRiskResult((response as any).data)
        // 显示Toast，然后延迟跳转
        console.log('🍞 显示Toast消息')
        Toast.show('分析完成')

        setTimeout(() => {
          console.log('✅ 步骤切换完成，跳转到分析结果')
          setStep('result')
          // 跳转后再关闭加载动画
          setTimeout(() => {
            console.log('🚨 即将设置stepLoading为false (第3个位置 - handleAnalyzeResponse)')
            console.log('🚨 调用栈:', new Error().stack?.split('\n').slice(1, 4).join('\n'))
            setStepLoading(false)
            console.log('📊 跳转后关闭加载动画')
          }, 100)
        }, 1000)
      }
    } catch (error) {
      Toast.show('分析失败，请重试')
      console.error('Analyze response error:', error)
    } finally {
      setLoading(false)
    }
  }



  const getRiskLevel = (score: number) => {
    if (score >= 75) return '高风险'
    if (score >= 40) return '中风险'
    return '低风险'
  }

  // 临时状态监控器
  console.log('🎭 组件渲染 - 当前状态:', {
    stepLoading,
    step,
    loading,
    hasRiskResult: !!riskResult,
    stepLoadingRef: stepLoadingRef.current
  })

  // 检查状态是否一致
  if (stepLoading !== stepLoadingRef.current) {
    console.log('🚨 状态不一致警告!')
    console.log('🚨 stepLoading:', stepLoading)
    console.log('🚨 stepLoadingRef.current:', stepLoadingRef.current)
  }

  return (
    <div className="risk-analysis-page">
      {/* 头部 */}
      <div className="header">
        <Button
          fill="none"
          onClick={() => navigate('/')}
          className="back-btn"
        >
          <LeftOutline />
        </Button>
        <h4 className="page-title">风控分析</h4>
        <div style={{
          position: 'fixed',
          top: '10px',
          right: '10px',
          background: 'rgba(0,0,0,0.8)',
          color: 'white',
          padding: '8px',
          borderRadius: '4px',
          fontSize: '12px',
          zIndex: 9999
        }}>
          stepLoading: {stepLoading.toString()}<br />
          step: {step}
        </div>
      </div>



      {/* 步骤指示器 */}
      <div className="step-indicator">
        <div className={`step ${step === 'input' ? 'active' : ''}`}>
          <div className="step-number">1</div>
          <div className="step-text">输入信息</div>
        </div>
        <div className={`step ${step === 'tactics' ? 'active' : ''}`}>
          <div className="step-number">2</div>
          <div className="step-text">生成话术</div>
        </div>
        <div className={`step ${step === 'response' ? 'active' : ''}`}>
          <div className="step-number">3</div>
          <div className="step-text">用户回答</div>
        </div>
        <div className={`step ${step === 'result' ? 'active' : ''}`}>
          <div className="step-number">4</div>
          <div className="step-text">分析结果</div>
        </div>
      </div>

      {/* 步骤切换加载动画 - 修复版本 */}
      {stepLoading && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999
        }}>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '40px',
            background: 'white',
            borderRadius: '16px',
            color: 'black',
            boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
            minWidth: '280px',
            textAlign: 'center'
          }}>
            <div style={{
              width: '50px',
              height: '50px',
              border: '4px solid #f3f3f3',
              borderTop: '4px solid #3498db',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
              marginBottom: '20px'
            }}></div>
            <div style={{
              fontSize: '20px',
              fontWeight: '600',
              marginBottom: '10px',
              color: '#333'
            }}>正在切换步骤...</div>
            <div style={{
              fontSize: '14px',
              color: '#666'
            }}>请稍候，系统正在处理...</div>
          </div>
        </div>
      )}

      {/* 步骤1：输入信息 */}
      {step === 'input' && (
        <div className="step-content">
          <Card className="input-card">
            <h5 className="card-title">输入要分析的信息</h5>
            <textarea
              placeholder="请输入对方的个人信息，如：年龄、职业、收入、家庭情况等"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              rows={4}
              className="input-textarea"
            />

            <div className="examples">
              <span className="examples-title">示例：</span>
              <Space wrap>
                {examples.map((example, index) => (
                  <Tag
                    key={index}
                    color="primary"
                    fill="outline"
                    onClick={() => handleExampleClick(example)}
                    className="example-tag"
                  >
                    {example.substring(0, 20)}...
                  </Tag>
                ))}
              </Space>
            </div>

            <Button
              color="primary"
              size="large"
              block
              onClick={handleStaticScan}
              loading={loading}
              className="action-btn"
            >
              <PlayOutline />
              开始静态扫描
            </Button>
          </Card>
        </div>
      )}

      {/* 步骤2：生成话术 */}
      {step === 'tactics' && riskResult && (
        <div className="step-content">
          <Card className="result-card">
            <h5 className="card-title">静态扫描结果</h5>

            <div className="risk-score">
              <div className="score-circle">
                <div className="score-circle-inner">
                  <div className="score-text">
                    {riskResult.score}
                  </div>
                </div>
              </div>
              <div className="score-info">
                <div className="risk-level">{getRiskLevel(riskResult.score)}</div>
                <div className="rules-count">触发 {riskResult.total_rules} 条规则</div>
              </div>
            </div>

            {/* AI分析结果 */}
            {riskResult.ai_analysis && (
              <>
                <div className="divider">AI智能分析</div>
                <div className="ai-analysis">
                  <div className="ai-risk-reasons">
                    <span className="ai-title">风险原因：</span>
                    <div className="ai-tags-container">
                      {riskResult.ai_analysis?.risk_reasons && riskResult.ai_analysis.risk_reasons.length > 0 ? (
                        riskResult.ai_analysis.risk_reasons.map((reason, index) => (
                          <Tag key={index} color="orange" fill="outline" className="ai-tag">
                            {reason}
                          </Tag>
                        ))
                      ) : (
                        <span className="no-ai-reasons">暂无AI分析结果</span>
                      )}
                    </div>
                  </div>
                  <div className="ai-suggestions">
                    <span className="ai-title">验证建议：</span>
                    <div className="suggestions-list">
                      {riskResult.ai_analysis?.verification_suggestions && riskResult.ai_analysis.verification_suggestions.length > 0 ? (
                        riskResult.ai_analysis.verification_suggestions.map((suggestion, index) => (
                          <div key={index} className="suggestion-item">
                            <span className="suggestion-number">{index + 1}</span>
                            <span className="suggestion-text">{suggestion}</span>
                          </div>
                        ))
                      ) : (
                        <span className="no-ai-suggestions">暂无验证建议</span>
                      )}
                    </div>
                  </div>
                </div>
              </>
            )}

            <div className="divider">触发规则</div>

            <div className="rules-container">
              {riskResult.rules && riskResult.rules.length > 0 ? (
                riskResult.rules.map((rule: any, index: number) => (
                  <div key={index} className="rule-item">
                    <div className="rule-header">
                      <Tag
                        color={rule.detection_method === 'ai_analysis' ? 'orange' :
                          rule.detection_method === 'pattern_analysis' ? 'purple' : 'red'}
                        fill="outline"
                        className="rule-method-tag"
                      >
                        {rule.detection_method === 'ai_analysis' ? 'AI检测' :
                          rule.detection_method === 'pattern_analysis' ? '模式识别' : '关键词'}
                      </Tag>
                      <span className="rule-name">{rule.rule_name}</span>
                      <span className="rule-score">+{rule.risk_value}分</span>
                    </div>
                    {rule.description && (
                      <div className="rule-description">{rule.description}</div>
                    )}
                    {rule.keywords && (
                      <div className="rule-keywords">
                        <span className="keywords-label">关键词：</span>
                        <span className="keywords-text">{rule.keywords.join('、')}</span>
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <div className="no-rules">
                  <p>暂无触发规则</p>
                </div>
              )}
            </div>

            <Button
              color="primary"
              size="large"
              block
              onClick={handleGenerateTactics}
              loading={loading}
              className="action-btn"
            >
              <SendOutline />
              生成验证话术
            </Button>
          </Card>
        </div>
      )}

      {/* 步骤3：用户回答 */}
      {step === 'response' && riskResult && (
        <div className="step-content">
          <Card className="tactics-card">
            <h5 className="card-title">验证话术</h5>

            {riskResult.verification_tactics?.filter((tactic: any) =>
              // 只显示AI生成的自然话术，过滤掉直接的验证建议
              tactic.rule_name !== 'AI智能建议'
            ).map((tactic: any, index: number) => (
              <div key={index} className="tactic-item">
                <div className="tactic-header">
                  <span className="tactic-rule">{tactic.rule_name}</span>
                  <span className="tactic-priority">{tactic.priority === 'high' ? '高优先级' : '中优先级'}</span>
                </div>
                <div className="tactic-text">{tactic.tactic}</div>
                {tactic.knowledge && (
                  <div className="tactic-knowledge">
                    <span className="knowledge-label">说明：</span>
                    <span className="knowledge-text">{tactic.knowledge}</span>
                  </div>
                )}
              </div>
            ))}

            <div className="divider">用户回答</div>

            <textarea
              placeholder="请输入用户的回答内容"
              value={userResponse}
              onChange={(e) => setUserResponse(e.target.value)}
              rows={4}
              className="input-textarea"
            />

            <Button
              color="primary"
              size="large"
              block
              onClick={handleAnalyzeResponse}
              loading={loading}
              className="action-btn"
            >
              <CheckShieldOutline />
              分析回答风险
            </Button>
          </Card>
        </div>
      )}

      {/* 步骤4：分析结果 */}
      {step === 'result' && riskResult && (
        <div className="step-content">
          <Card className="final-result-card">
            <h5 className="card-title">最终分析结果</h5>

            <div className="final-risk-score">
              <div className="score-circle large">
                <div className="score-circle-inner large">
                  <div className="score-text large">
                    {riskResult.decision?.total_score || riskResult.score}
                  </div>
                </div>
              </div>
              <div className="score-info">
                <div className="risk-level large">{riskResult.decision?.risk_level || getRiskLevel(riskResult.score)}</div>
                <div className="decision">{riskResult.decision?.decision || '分析完成'}</div>
              </div>
            </div>

            <div className="divider">评分详情</div>

            <div className="score-details">
              <div className="score-item">
                <span>静态评分：</span>
                <span className="score-value">
                  {riskResult.static_scan?.score || riskResult.score || 0}
                </span>
              </div>
              <div className="score-item">
                <span>动态评分：</span>
                <span className="score-value">
                  {riskResult.decision?.dynamic_score || 0}
                </span>
              </div>
              <div className="score-item">
                <span>权重：</span>
                <span className="score-value">
                  静态{riskResult.decision?.static_weight ? (riskResult.decision.static_weight * 100) : 60}% +
                  动态{riskResult.decision?.dynamic_weight ? (riskResult.decision.dynamic_weight * 100) : 40}%
                </span>
              </div>
            </div>

            <div className="divider">证据链</div>

            <div className="evidence-chain">
              {riskResult.evidence_chain && riskResult.evidence_chain.length > 0 ? (
                riskResult.evidence_chain.map((evidence, index) => (
                  <div key={index} className="evidence-item">
                    <div className="evidence-number">{index + 1}</div>
                    <div className="evidence-text">{evidence}</div>
                  </div>
                ))
              ) : (
                <div className="evidence-item">
                  <div className="evidence-number">1</div>
                  <div className="evidence-text">基于静态扫描结果进行风险评估</div>
                </div>
              )}
            </div>

            {/* 显示验证话术 */}
            {riskResult.verification_tactics && riskResult.verification_tactics.length > 0 && (
              <>
                <div className="divider">验证话术</div>
                <div className="verification-tactics">
                  {riskResult.verification_tactics.filter((tactic: any) =>
                    tactic.rule_name !== 'AI智能建议'
                  ).map((tactic: any, index: number) => (
                    <div key={index} className="tactic-item">
                      <div className="tactic-header">
                        <span className="tactic-rule">{tactic.rule_name}</span>
                        <span className="tactic-priority">{tactic.priority === 'high' ? '高优先级' : '中优先级'}</span>
                      </div>
                      <div className="tactic-text">{tactic.tactic}</div>
                      {tactic.knowledge && (
                        <div className="tactic-knowledge">
                          <span className="knowledge-label">说明：</span>
                          <span className="knowledge-text">{tactic.knowledge}</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </>
            )}

            <Button
              color="default"
              size="large"
              block
              onClick={() => {
                console.log('🚨 即将设置stepLoading为true (重新分析按钮)')
                setStepLoading(true)
                setTimeout(() => {
                  setStep('input')
                  setInputText('')
                  setUserResponse('')
                  setRiskResult(null)
                  console.log('🚨 即将设置stepLoading为false (第4个位置 - 重新分析按钮)')
                  console.log('🚨 调用栈:', new Error().stack?.split('\n').slice(1, 4).join('\n'))
                  setStepLoading(false)
                }, 1000)
              }}
              className="action-btn"
            >
              重新分析
            </Button>
          </Card>
        </div>
      )}

      {loading && <Loading className="loading-overlay" />}

      {/* 添加简单的CSS动画 */}
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}

export default RiskAnalysisPage
