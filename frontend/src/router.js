import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue'
import ForgotPassword from './components/ForgotPassword.vue'
import Main from './components/Main.vue'

const routes = [
  { path: '/login', component: Login, meta: { public: true } },
  { path: '/forgot-password', component: ForgotPassword, meta: { public: true } },
  { path: '/', component: Main },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const token = localStorage.getItem('session_token')
  if (!to.meta.public && !token) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
  if (to.meta.public && token) {
    return { path: '/' }
  }
})

export default router
