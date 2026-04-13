<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h2 class="login-title">Login</h2>
      <form @submit.prevent="submit">
        <div class="form-group">
          <label class="form-label">Email</label>
          <input
            v-model="form.email"
            type="email"
            placeholder="you@example.com"
            required
            class="form-input"
          />
        </div>
        <div class="form-group form-group--last">
          <label class="form-label">Password</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="Password"
            required
            class="form-input"
          />
        </div>
        <button type="submit" :disabled="loading" class="btn-submit">
          {{ loading ? 'Signing in…' : 'Sign In' }}
        </button>
      </form>
      <p v-if="error" class="error-text">{{ error }}</p>
      <div class="forgot-link-wrapper">
        <a href="#" @click.prevent="emit('forgot-password')" class="forgot-link">
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

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.login-card {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  width: 320px;
}

.login-title {
  margin-top: 0;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group--last {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.3rem;
  font-size: 0.9rem;
  color: #555;
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn-submit {
  width: 100%;
  padding: 0.6rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.btn-submit:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.error-text {
  color: red;
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
}

.forgot-link-wrapper {
  margin-top: 1rem;
  text-align: center;
}

.forgot-link {
  color: #3498db;
  font-size: 0.9rem;
  text-decoration: none;
}
</style>
