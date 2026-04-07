<template>
  <div v-if="isLoggedIn">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Users from './components/Users.vue'
import Products from './components/Products.vue'

const LOGIN_URL = 'http://localhost:3000'
const BASE = 'http://localhost:8080/api'

const currentView = ref('users')
const isLoggedIn = ref(!!localStorage.getItem('session_token'))
const currentUser = ref((() => {
  try { return JSON.parse(localStorage.getItem('session_user') || 'null') } catch { return null }
})())

onMounted(() => {
  if (!isLoggedIn.value) {
    window.location.href = `${LOGIN_URL}?redirect=${encodeURIComponent(window.location.href)}`
  }
})

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
  window.location.href = `${LOGIN_URL}?redirect=${encodeURIComponent(window.location.href)}`
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

