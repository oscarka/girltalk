import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 60000, // 增加到60秒，给后端更多处理时间
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url, config.data)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data)
    return response.data
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// 风控分析API
export const riskAnalysisAPI = {
  // 静态风险扫描
  staticScan: async (text: string) => {
    return api.post('/static-scan', { text })
  },

  // 动态风险分析
  dynamicAnalysis: async (responseText: string) => {
    return api.post('/dynamic-analysis', { response_text: responseText })
  },

  // 完整风控分析
  fullAnalysis: async (inputText: string, userResponse?: string) => {
    return api.post('/full-analysis', {
      input_text: inputText,
      user_response: userResponse
    })
  },

  // 健康检查
  healthCheck: async () => {
    return api.get('/health')
  }
}

// 配置管理API
export const configAPI = {
  // 获取风险规则
  getRiskRules: async () => {
    return api.get('/risk-rules')
  },

  // 更新风险规则
  updateRiskRules: async (rules: any) => {
    return api.post('/risk-rules', rules)
  },

  // 获取权重配置
  getWeightConfig: async () => {
    return api.get('/weight-config')
  },

  // 更新权重配置
  updateWeightConfig: async (config: any) => {
    return api.post('/weight-config', config)
  },

  // 获取知识库
  getKnowledgeBase: async () => {
    return api.get('/knowledge-base')
  },

  // 上传知识库文件
  uploadKnowledge: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)

    return api.post('/upload-knowledge', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  }
}

export default api
