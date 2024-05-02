import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import './assets/less/index.less'
import api from './api/api'

const app = createApp(App)  // ����VueӦ��ʵ��

// ע��Element Plusͼ�꣺
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)   // ע��ʹ��ͼ��
}

// store.commit("addMenu", router)          // ����addMenu���mutation ����·�ɵ��˵�״̬��
app.config.globalProperties.$api = api      // ��APIģ������ΪVueʵ����ȫ�����ԣ��Ա����κ������ͨ��this.$api����API����

app.use(ElementPlus)
app.use(router)
app.use(store)
app.mount('#app')

