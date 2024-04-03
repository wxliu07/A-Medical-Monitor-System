import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'myhome',
    redirect: '/home',
    component: () => import('../views/MainPage.vue'), 
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
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
