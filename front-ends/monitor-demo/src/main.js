import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import './assets/less/index.less'
import api from './api/api'

const app = createApp(App)  // 全局唯一

// 注册图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)   
}

// store.commit("addMenu", router)          
app.config.globalProperties.$api = api     


app.use(ElementPlus)
app.use(router)
app.use(store)


// // 动态添加路由的函数
// function addRoutesFromMenu(menu) {
//     menu.forEach(item => {
//       let route = {
//         path: item.path,
//         name: item.name,
//         component: () => import(/* webpackChunkName: "[request]" */ `@/views/${item.url}`)
//       };
//       router.addRoute(route);
  
//       // 如果有子菜单，递归添加
//       if (item.children && item.children.length) {
//         addRoutesFromMenu(item.children);
//       }
//     });
//   }
  
//   // 从 localStorage 加载菜单并添加路由
//   const storedMenu = JSON.parse(localStorage.getItem('menu') || '[]');
//   if (storedMenu.length > 0) {
//     addRoutesFromMenu(storedMenu);
//   }

app.mount('#app')

