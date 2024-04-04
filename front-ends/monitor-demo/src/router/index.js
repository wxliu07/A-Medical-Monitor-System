import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    // '/'是根路径
    path: '/',
    name: 'myhome',
    component: () => import('../views/MainPage.vue'), 
    redirect: '/home',
    children: [
      {
        path: '/home',
        name: 'home',
        component: () => import('../views/home/HomePage.vue')
      },
      {
        path: '/user',
        name: 'user',
        component: () => import('../views/user/UserPage.vue')
      },
      {
        path: '/data',
        name: 'datapage1',
        component: () => import('../views/data/DataPage1.vue')
      },
      {
        path: '/data',
        name: 'datapage2',
        component: () => import('../views/data/DataPage2.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginPage.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
