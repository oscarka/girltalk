import axios from 'axios'

// 定义 API 响应类型
interface APIResponse<T = any> {
  success: boolean
  data: T
  message?: string
}

// 声明 Vite 环境变量类型
declare global {
  interface ImportMeta {
    readonly env: {
      readonly VITE_API_BASE_URL?: string
    }
  }
}

// 创建axios实例
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL.endsWith('/api/v1') ? API_BASE_URL : `${API_BASE_URL}/api/v1`,
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
  staticScan: async (text: string): Promise<APIResponse<any>> => {
    return api.post('/static-scan', { text })
  },

  // 动态风险分析
  dynamicAnalysis: async (responseText: string): Promise<APIResponse<any>> => {
    return api.post('/dynamic-analysis', { response_text: responseText })
  },

  // 完整风控分析
  fullAnalysis: async (inputText: string, userResponse?: string): Promise<APIResponse<any>> => {
    return api.post('/full-analysis', {
      input_text: inputText,
      user_response: userResponse
    })
  },

  // 健康检查
  healthCheck: async (): Promise<APIResponse<any>> => {
    return api.get('/health')
  }
}

// 配置管理API
export const configAPI = {
  // 获取风险规则
  getRiskRules: async (): Promise<APIResponse<any>> => {
    return api.get('/risk-rules')
  },

  // 更新风险规则
  updateRiskRules: async (rules: any): Promise<APIResponse<any>> => {
    return api.post('/risk-rules', rules)
  },

  // 获取权重配置
  getWeightConfig: async (): Promise<APIResponse<any>> => {
    return api.get('/weight-config')
  },

  // 更新权重配置
  updateWeightConfig: async (config: any): Promise<APIResponse<any>> => {
    return api.post('/weight-config', config)
  },

  // 获取知识库
  getKnowledgeBase: async (): Promise<APIResponse<any>> => {
    return api.get('/knowledge-base')
  },

  // 上传知识库文件
  uploadKnowledge: async (file: File): Promise<APIResponse<any>> => {
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
