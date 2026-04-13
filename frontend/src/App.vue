<template>
  <div v-if="isLoggedIn">
    <nav class="app-nav">
      <button
        class="nav-btn"
        :class="{ active: currentView === 'users' }"
        @click="currentView = 'users'"
      >Users</button>
      <button
        class="nav-btn"
        :class="{ active: currentView === 'products' }"
        @click="currentView = 'products'"
      >Products</button>
      <span class="nav-username">{{ currentUser?.name }}</span>
      <button class="nav-btn logout-btn" @click="handleLogout">Logout</button>
    </nav>
    <div class="app-content">
      <Users v-if="currentView === 'users'" />
      <Products v-if="currentView === 'products'" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Users from './components/Users.vue'
import Products from './components/Products.vue'

const BASE = 'http://localhost:8080/api'

const currentView = ref('users')
const isLoggedIn = ref(!!localStorage.getItem('session_token'))

function loadStoredUser() {
  try {
    return JSON.parse(localStorage.getItem('session_user') || 'null')
  } catch {
    return null
  }
}
const currentUser = ref(loadStoredUser())

onMounted(() => {
  if (!isLoggedIn.value) {
    window.location.href = '/login.html'
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
  window.location.href = '/login.html'
}
</script>

<style scoped>
.app-nav {
  background: #2c3e50;
  padding: 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-btn {
  background: transparent;
  color: white;
  border: 1px solid #3498db;
  padding: 0.5rem 1rem;
  cursor: pointer;
  border-radius: 4px;
}

.nav-btn.active {
  background: #3498db;
}

.nav-username {
  margin-left: auto;
  color: #ecf0f1;
  font-size: 0.9rem;
}

.logout-btn {
  border-color: #e74c3c;
  color: #e74c3c;
}

.app-content {
  padding: 1rem;
}
</style>

