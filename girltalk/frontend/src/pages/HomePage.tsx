import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Button, Card, Space } from 'antd-mobile'
import {
  CheckShieldOutline,
  SetOutline,
  PlayOutline
} from 'antd-mobile-icons'
import './HomePage.css'

const HomePage: React.FC = () => {
  const navigate = useNavigate()

  const features = [
    {
      icon: <CheckShieldOutline />,
      title: '智能风控',
      desc: 'AI驱动的风险评估系统'
    },
    {
      icon: <PlayOutline />,
      title: '动态对话',
      desc: '智能话术生成与验证'
    },
    {
      icon: <SetOutline />,
      title: '灵活配置',
      desc: '可自定义规则与权重'
    }
  ]

  return (
    <div className="home-page">
      <div className="header">
        <h1 className="main-title">
          婚恋风控系统
        </h1>
        <p className="subtitle">
          智能识别潜在风险，保护您的感情安全
        </p>
      </div>

      <div className="features">
        {features.map((feature, index) => (
          <Card key={index} className="feature-card">
            <div className="feature-icon">{feature.icon}</div>
            <h4 className="feature-title">{feature.title}</h4>
            <p className="feature-desc">{feature.desc}</p>
          </Card>
        ))}
      </div>

      <div className="actions">
        <Space direction="vertical" block>
          <Button
            color="primary"
            size="large"
            block
            onClick={() => navigate('/analysis')}
            className="action-btn"
          >
            开始风控分析
          </Button>
          <Button
            color="default"
            size="large"
            block
            onClick={() => navigate('/config')}
            className="action-btn"
          >
            系统配置
          </Button>
        </Space>
      </div>

      <div className="footer">
        <p className="version">版本 1.0.0</p>
      </div>
    </div>
  )
}

export default HomePage
