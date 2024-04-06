/**
 * 环境配置问题
 * 三个环境: 开发, 测试, 线上
 */

// const env = import.meta.env.MODE || 'prod'
const env = 'development'

const EnvConfig = {
    development: {
      baseApi: 'http://127.0.0.1:5000/api',  // Flask后端
      mockApi: '',  // mock后端
    },
    test: {
      baseApi: '',
      mockApi: '',
    },
    pro: {
      baseApi: '',
      mockApi: '',
    },
  }
  
  export default {
    ...EnvConfig[env]   // 解构语法
  }