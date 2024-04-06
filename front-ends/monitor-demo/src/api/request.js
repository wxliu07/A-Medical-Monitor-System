import axios from 'axios'
import config from '../config'
import { ElMessage } from 'element-plus'
const NETWORK_ERROR = 'network error, please try it again.....'

// 创建一个axios实例对象
const service = axios.create({
    baseURL: config.baseApi
})


// 请求拦截: 可以发起请求之前，做一个拦截，把数据（参数，配置…）做了处理再发送请求
// jwt-token认证的时候可以自定义header
service.interceptors.request.use((req) => {
    return req
})


// 在请求之后做一些事情
service.interceptors.response.use((res) => {
    console.log(res);
    const { code, data, msg } = res.data
    if (code == 200) {
        return data
    } 
    else {
        // 网络请求错误
        ElMessage.error(msg || NETWORK_ERROR)
        return Promise.reject(msg || NETWORK_ERROR)
    }
})


// axios参数调整
function request(options) {
    options.method = options.method || 'get'    // 默认get方式
    if (options.method.toLowerCase() == 'get') {
        options.params = options.data
      }
    
    // 处理不同环境的baseURL, 此处省略

    return service(options) // 初始化axios实例化对象
}

export default request