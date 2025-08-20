import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ConfigProvider } from 'antd-mobile'
import zhCN from 'antd-mobile/es/locales/zh-CN'
import HomePage from './pages/HomePage'
import RiskAnalysisPage from './pages/RiskAnalysisPage'
import ConfigPage from './pages/ConfigPage'
import './App.css'

const App: React.FC = () => {
  return (
    <ConfigProvider locale={zhCN}>
      <Router>
        <div className="app">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/analysis" element={<RiskAnalysisPage />} />
            <Route path="/config" element={<ConfigPage />} />
          </Routes>
        </div>
      </Router>
    </ConfigProvider>
  )
}

export default App
