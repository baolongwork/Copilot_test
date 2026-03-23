<template>
  <div>
    <Login v-if="!isLoggedIn && authView === 'login'" @login="handleLogin" @forgot-password="authView = 'forgot-password'" />
    <ForgotPassword v-else-if="!isLoggedIn && authView === 'forgot-password'" @back-to-login="authView = 'login'" />
    <template v-else-if="isLoggedIn">
      <nav style="background:#2c3e50;padding:1rem;display:flex;gap:1rem;align-items:center;">
        <button @click="currentView='users'" :style="navBtnStyle('users')">Users</button>
        <button @click="currentView='products'" :style="navBtnStyle('products')">Products</button>
        <span style="margin-left:auto;color:#ecf0f1;font-size:0.9rem;">{{ currentUser?.name }}</span>
        <button @click="handleLogout" style="background:transparent;color:#e74c3c;border:1px solid #e74c3c;padding:0.5rem 1rem;cursor:pointer;border-radius:4px;">Logout</button>
      </nav>
      <div style="padding:1rem;">
        <Users v-if="currentView==='users'" />
        <Products v-if="currentView==='products'" />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Users from './components/Users.vue'
import Products from './components/Products.vue'
import Login from './components/Login.vue'
import ForgotPassword from './components/ForgotPassword.vue'

const BASE = 'http://localhost:8080/api'

const currentView = ref('users')
const authView = ref('login')
const isLoggedIn = ref(!!localStorage.getItem('session_token'))
const currentUser = ref((() => {
  try { return JSON.parse(localStorage.getItem('session_user') || 'null') } catch { return null }
})())

function handleLogin({ token, user }) {
  localStorage.setItem('session_token', token)
  localStorage.setItem('session_user', JSON.stringify(user))
  isLoggedIn.value = true
  currentUser.value = user
}

async function handleLogout() {
  const token = localStorage.getItem('session_token')
  if (token) {
    try {
      await axios.post(`${BASE}/logout`, null, { headers: { Authorization: token } })
    } catch (_) {
      // ignore errors on logout
    }
  }
  localStorage.removeItem('session_token')
  localStorage.removeItem('session_user')
  isLoggedIn.value = false
  currentUser.value = null
  authView.value = 'login'
}

function navBtnStyle(view) {
  return {
    background: currentView.value === view ? '#3498db' : 'transparent',
    color: 'white',
    border: '1px solid #3498db',
    padding: '0.5rem 1rem',
    cursor: 'pointer',
    borderRadius: '4px',
  }
}
</script>

