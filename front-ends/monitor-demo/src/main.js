import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import './assets/less/index.less'
import api from './api/api'

const app = createApp(App)  // 创建Vue应用实例

// 注册Element Plus图标：
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)   // 注册使用图标
}

// store.commit("addMenu", router)          // 触发addMenu这个mutation 添加路由到菜单状态中
app.config.globalProperties.$api = api      // 将API模块设置为Vue实例的全局属性，以便在任何组件中通过this.$api访问API函数

app.use(ElementPlus)
app.use(router)
app.use(store)
app.mount('#app')

