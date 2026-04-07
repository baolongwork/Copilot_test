<template>
  <div style="display:flex;justify-content:center;align-items:center;min-height:80vh;">
    <div style="background:#fff;padding:2rem;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.15);width:340px;">

      <!-- Step 1: Request reset token -->
      <template v-if="step === 'request'">
        <h2 style="margin-top:0;margin-bottom:0.5rem;text-align:center;color:#2c3e50;">Forgot Password</h2>
        <p style="text-align:center;color:#666;font-size:0.9rem;margin-bottom:1.5rem;">
          Enter your email address and we'll send you a reset token.
        </p>
        <form @submit.prevent="requestReset">
          <div style="margin-bottom:1rem;">
            <label style="display:block;margin-bottom:0.3rem;font-size:0.9rem;color:#555;">Email</label>
            <input
              v-model="email"
              type="email"
              placeholder="you@example.com"
              required
              style="width:100%;padding:0.5rem;box-sizing:border-box;border:1px solid #ccc;border-radius:4px;"
            />
          </div>
          <button
            type="submit"
            :disabled="loading"
            style="width:100%;padding:0.6rem;background:#3498db;color:white;border:none;border-radius:4px;cursor:pointer;font-size:1rem;"
          >
            {{ loading ? 'Sending…' : 'Send Reset Token' }}
          </button>
        </form>
        <p v-if="error" style="color:red;margin-top:1rem;text-align:center;font-size:0.9rem;">{{ error }}</p>
      </template>

      <!-- Step 2: Enter token and new password -->
      <template v-else-if="step === 'reset'">
        <h2 style="margin-top:0;margin-bottom:0.5rem;text-align:center;color:#2c3e50;">Reset Password</h2>
        <p style="text-align:center;color:#27ae60;font-size:0.85rem;margin-bottom:1.5rem;">
          A reset token has been issued. Enter it below along with your new password.
        </p>
        <form @submit.prevent="doReset">
          <div style="margin-bottom:1rem;">
            <label style="display:block;margin-bottom:0.3rem;font-size:0.9rem;color:#555;">Reset Token</label>
            <input
              v-model="resetTokenInput"
              type="text"
              placeholder="Paste your reset token"
              required
              style="width:100%;padding:0.5rem;box-sizing:border-box;border:1px solid #ccc;border-radius:4px;font-family:monospace;"
            />
          </div>
          <div style="margin-bottom:1rem;">
            <label style="display:block;margin-bottom:0.3rem;font-size:0.9rem;color:#555;">New Password</label>
            <input
              v-model="newPassword"
              type="password"
              placeholder="At least 8 characters"
              required
              minlength="8"
              style="width:100%;padding:0.5rem;box-sizing:border-box;border:1px solid #ccc;border-radius:4px;"
            />
          </div>
          <div style="margin-bottom:1.5rem;">
            <label style="display:block;margin-bottom:0.3rem;font-size:0.9rem;color:#555;">Confirm Password</label>
            <input
              v-model="confirmPassword"
              type="password"
              placeholder="Repeat new password"
              required
              style="width:100%;padding:0.5rem;box-sizing:border-box;border:1px solid #ccc;border-radius:4px;"
            />
          </div>
          <button
            type="submit"
            :disabled="loading"
            style="width:100%;padding:0.6rem;background:#27ae60;color:white;border:none;border-radius:4px;cursor:pointer;font-size:1rem;"
          >
            {{ loading ? 'Resetting…' : 'Reset Password' }}
          </button>
        </form>
        <p v-if="error" style="color:red;margin-top:1rem;text-align:center;font-size:0.9rem;">{{ error }}</p>
      </template>

      <!-- Step 3: Success -->
      <template v-else-if="step === 'done'">
        <h2 style="margin-top:0;margin-bottom:0.5rem;text-align:center;color:#27ae60;">Password Reset!</h2>
        <p style="text-align:center;color:#555;font-size:0.9rem;margin-bottom:1.5rem;">
          Your password has been updated successfully. You can now sign in with your new password.
        </p>
        <button
          @click="emit('back-to-login')"
          style="width:100%;padding:0.6rem;background:#3498db;color:white;border:none;border-radius:4px;cursor:pointer;font-size:1rem;"
        >
          Back to Login
        </button>
      </template>

      <div v-if="step !== 'done'" style="margin-top:1rem;text-align:center;">
        <a
          href="#"
          @click.prevent="emit('back-to-login')"
          style="color:#3498db;font-size:0.9rem;text-decoration:none;"
        >
          Back to Login
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const BASE = 'http://localhost:8080/api'

const emit = defineEmits(['back-to-login'])

const step = ref('request')
const email = ref('')
const resetTokenInput = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

async function requestReset() {
  error.value = ''
  loading.value = true
  try {
    const res = await axios.post(`${BASE}/forgot-password`, { email: email.value })
    // In this demo the token is returned directly; pre-fill it for convenience.
    if (res.data.reset_token) {
      resetTokenInput.value = res.data.reset_token
    }
    step.value = 'reset'
  } catch (e) {
    error.value = e.response?.data?.error || 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}

async function doReset() {
  error.value = ''
  if (newPassword.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }
  loading.value = true
  try {
    await axios.post(`${BASE}/reset-password`, {
      token: resetTokenInput.value,
      password: newPassword.value,
    })
    step.value = 'done'
  } catch (e) {
    error.value = e.response?.data?.error || 'Reset failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
