import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    // '/'是根路径
    path: '/',
    name: 'myhome',
    component: () => import('../views/MainPage.vue'), 
    redirect: '/login',
    children: [
      {
        path: '/home',
        name: 'home',
        component: () => import('../views/home/HomePage.vue')
      },
      {
        path: '/monitor',
        name: 'monitorPage',
        component: () => import('../views/monitor/Monitor.vue')
      },
      {
        path: '/data',
        name: 'hrPage',
        component: () => import('../views/data/HRPage.vue')
      },
      {
        path: '/data',
        name: 'rrPage',
        component: () => import('../views/data/RRPage.vue')
      },
      {
        path: '/data',
        name: 'spo2Page',
        component: () => import('../views/data/SpO2Page.vue')
      },
      {
        path: '/user',
        name: 'user',
        component: () => import('../views/user/UserPage.vue')
      },
      {
        path: '/user',
        name: 'usersInfo',
        component: () => import('../views/user/AdminUsersPage.vue')
      },
      {
        path: '/userControlPage',
        name: 'userControlPage',
        component: () => import('../views/admin/UsersControlPage.vue')
      },
      {
        path: '/userInfolPage',
        name: 'userInfolPage',
        component: () => import('../views/admin/UserInfoPage.vue')
      },
      {
        path: '/usersVideoPage',
        name: 'usersVideoPage',
        component: () => import('../views/admin/UsersVideoPage.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginPage.vue')
  },
  {
    path: '/:catchAll(.*)',
    name: '404',
    component: () => import('../views/404Page.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
