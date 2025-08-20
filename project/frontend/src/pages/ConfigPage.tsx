import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Button, 
  Card, 
  Tabs, 
  Space,
  Toast,
  Loading,
  List
} from 'antd-mobile'
import { 
  LeftOutline, 
  EditSOutline,
  UploadOutline,
  DownlandOutline
} from 'antd-mobile-icons'
import { configAPI } from '../services/api'
import './ConfigPage.css'

const ConfigPage: React.FC = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [riskRules, setRiskRules] = useState('')
  const [weightConfig, setWeightConfig] = useState('')
  const [knowledgeBase, setKnowledgeBase] = useState<any>({})

  useEffect(() => {
    loadConfigs()
  }, [])

  const loadConfigs = async () => {
    setLoading(true)
    try {
      // 加载风险规则
      const rulesResponse = await configAPI.getRiskRules()
      if (rulesResponse.success) {
        setRiskRules(JSON.stringify(rulesResponse.data.rules, null, 2))
      }

      // 加载权重配置
      const weightResponse = await configAPI.getWeightConfig()
      if (weightResponse.success) {
        setWeightConfig(JSON.stringify(weightResponse.data.config, null, 2))
      }

      // 加载知识库
      const knowledgeResponse = await configAPI.getKnowledgeBase()
      if (knowledgeResponse.success) {
        setKnowledgeBase(knowledgeResponse.data.knowledge_files)
      }
    } catch (error) {
      Toast.show('加载配置失败')
      console.error('Load configs error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSaveRiskRules = async () => {
    try {
      const rules = JSON.parse(riskRules)
      const response = await configAPI.updateRiskRules(rules)
      if (response.success) {
        Toast.show('风险规则保存成功')
      }
    } catch (error) {
      Toast.show('JSON格式错误，请检查语法')
      console.error('Save risk rules error:', error)
    }
  }

  const handleSaveWeightConfig = async () => {
    try {
      const config = JSON.parse(weightConfig)
      const response = await configAPI.updateWeightConfig(config)
      if (response.success) {
        Toast.show('权重配置保存成功')
      }
    } catch (error) {
      Toast.show('JSON格式错误，请检查语法')
      console.error('Save weight config error:', error)
    }
  }

  const handleFileUpload = async (file: File) => {
    try {
      const response = await configAPI.uploadKnowledge(file)
      if (response.success) {
        Toast.show('知识库文件上传成功')
        loadConfigs() // 重新加载知识库
      }
    } catch (error) {
      Toast.show('文件上传失败')
      console.error('Upload file error:', error)
    }
  }

  const downloadConfig = (type: 'rules' | 'weight') => {
    let content = ''
    let filename = ''
    
    if (type === 'rules') {
      content = riskRules
      filename = 'risk_rules.json'
    } else {
      content = weightConfig
      filename = 'weight_config.yaml'
    }

    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const tabs = [
    {
      key: 'risk-rules',
      title: '风险规则',
      content: (
        <Card className="config-card">
          <div className="config-header">
            <h5 className="config-title">风险规则配置</h5>
            <Space wrap>
              <Button
                size="small"
                onClick={() => downloadConfig('rules')}
                className="download-btn"
              >
                <DownlandOutline />
                下载
              </Button>
              <Button
                color="primary"
                size="small"
                onClick={handleSaveRiskRules}
                className="save-btn"
              >
                <EditSOutline />
                保存
              </Button>
            </Space>
          </div>
          <textarea
            value={riskRules}
            onChange={(e) => setRiskRules(e.target.value)}
            placeholder="请输入JSON格式的风险规则配置"
            rows={15}
            className="config-textarea"
          />
          <div className="config-tips">
            <span className="tip-text">
              提示：请确保JSON格式正确，可以使用在线JSON验证工具检查语法
            </span>
          </div>
        </Card>
      )
    },
    {
      key: 'weight-config',
      title: '权重配置',
      content: (
        <Card className="config-card">
          <div className="config-header">
            <h5 className="config-title">权重配置</h5>
            <Space wrap>
              <Button
                size="small"
                onClick={() => downloadConfig('weight')}
                className="download-btn"
              >
                <DownlandOutline />
                下载
              </Button>
              <Button
                color="primary"
                size="small"
                onClick={handleSaveWeightConfig}
                className="save-btn"
              >
                <EditSOutline />
                保存
              </Button>
            </Space>
          </div>
          <textarea
            value={weightConfig}
            onChange={(e) => setWeightConfig(e.target.value)}
            placeholder="请输入JSON格式的权重配置"
            rows={15}
            className="config-textarea"
          />
          <div className="config-tips">
            <span className="tip-text">
              提示：权重配置影响风控决策，请谨慎调整
            </span>
          </div>
        </Card>
      )
    },
    {
      key: 'knowledge-base',
      title: '知识库',
      content: (
        <Card className="config-card">
          <h5 className="config-title">知识库管理</h5>
          
          <div className="upload-section">
            <span className="section-title">上传知识库文件</span>
            <div className="upload-area">
              <input
                type="file"
                accept=".csv"
                onChange={(e) => {
                  const file = e.target.files?.[0]
                  if (file) handleFileUpload(file)
                }}
                className="file-input"
              />
              <Button
                color="primary"
                fill="outline"
                className="upload-btn"
                onClick={() => document.querySelector('.file-input')?.click()}
              >
                <UploadOutline />
                选择CSV文件
              </Button>
            </div>
            <span className="upload-tip">
              支持CSV格式，文件应包含：政策名称、生效日期、影响行业、关键条款等列
            </span>
          </div>

          <div className="knowledge-list">
            <span className="section-title">现有知识库</span>
            {Object.keys(knowledgeBase).length > 0 ? (
              <List>
                {Object.entries(knowledgeBase).map(([key, value]: [string, any]) => (
                  <List.Item key={key} className="knowledge-item">
                    <div className="knowledge-info">
                      <div className="knowledge-name">{key}</div>
                      <div className="knowledge-details">
                        <span className="detail-text">
                          文件：{value.filename} | 
                          行数：{value.rows} | 
                          列数：{value.columns.length}
                        </span>
                      </div>
                    </div>
                  </List.Item>
                ))}
              </List>
            ) : (
              <div className="empty-state">
                <span className="empty-text">暂无知识库文件</span>
              </div>
            )}
          </div>
        </Card>
      )
    }
  ]

  return (
    <div className="config-page">
      {/* 头部 */}
      <div className="header">
        <Button
          fill="none"
          onClick={() => navigate('/')}
          className="back-btn"
        >
          <LeftOutline />
        </Button>
        <h4 className="page-title">系统配置</h4>
      </div>

      {/* 配置标签页 */}
      <Tabs className="config-tabs">
        {tabs.map(tab => (
          <Tabs.Tab title={tab.title} key={tab.key}>
            {tab.content}
          </Tabs.Tab>
        ))}
      </Tabs>

      {loading && <Loading className="loading-overlay" />}
    </div>
  )
}

export default ConfigPage
