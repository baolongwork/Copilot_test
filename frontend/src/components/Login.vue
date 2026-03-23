<template>
  <div style="display:flex;justify-content:center;align-items:center;min-height:80vh;">
    <div style="background:#fff;padding:2rem;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.15);width:320px;">
      <h2 style="margin-top:0;margin-bottom:1.5rem;text-align:center;color:#2c3e50;">Login</h2>
      <form @submit.prevent="submit">
        <div style="margin-bottom:1rem;">
          <label style="display:block;margin-bottom:0.3rem;font-size:0.9rem;color:#555;">Email</label>
          <input
            v-model="form.email"
            type="email"
            placeholder="you@example.com"
            required
            style="width:100%;padding:0.5rem;box-sizing:border-box;border:1px solid #ccc;border-radius:4px;"
          />
        </div>
        <div style="margin-bottom:1.5rem;">
          <label style="display:block;margin-bottom:0.3rem;font-size:0.9rem;color:#555;">Password</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="Password"
            required
            style="width:100%;padding:0.5rem;box-sizing:border-box;border:1px solid #ccc;border-radius:4px;"
          />
        </div>
        <button
          type="submit"
          :disabled="loading"
          style="width:100%;padding:0.6rem;background:#3498db;color:white;border:none;border-radius:4px;cursor:pointer;font-size:1rem;"
        >
          {{ loading ? 'Signing in…' : 'Sign In' }}
        </button>
      </form>
      <p v-if="error" style="color:red;margin-top:1rem;text-align:center;font-size:0.9rem;">{{ error }}</p>
      <div style="margin-top:1rem;text-align:center;">
        <a
          href="#"
          @click.prevent="emit('forgot-password')"
          style="color:#3498db;font-size:0.9rem;text-decoration:none;"
        >
          Forgot your password?
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const BASE = 'http://localhost:8080/api'

const emit = defineEmits(['login', 'forgot-password'])

const form = ref({ email: '', password: '' })
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const res = await axios.post(`${BASE}/login`, form.value)
    emit('login', { token: res.data.token, user: res.data.user })
  } catch (e) {
    error.value = e.response?.data?.error || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
