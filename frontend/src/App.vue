<template>
  <div>
    <nav style="background:#2c3e50;padding:1rem;display:flex;gap:1rem;">
      <button @click="currentView='users'" :style="navBtnStyle('users')">Users</button>
      <button @click="currentView='products'" :style="navBtnStyle('products')">Products</button>
    </nav>
    <div style="padding:1rem;">
      <Users v-if="currentView==='users'" />
      <Products v-if="currentView==='products'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Users from './components/Users.vue'
import Products from './components/Products.vue'

const currentView = ref('users')

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
