<template>
  <div>
    <h2>Users</h2>
    <form @submit.prevent="submitForm" style="margin-bottom:1rem;display:flex;gap:0.5rem;flex-wrap:wrap;">
      <input v-model="form.name" placeholder="Name" required style="padding:0.4rem;" />
      <input v-model="form.email" placeholder="Email" required style="padding:0.4rem;" />
      <button type="submit" style="padding:0.4rem 1rem;background:#27ae60;color:white;border:none;border-radius:4px;cursor:pointer;">
        {{ editingId ? 'Update' : 'Create' }}
      </button>
      <button v-if="editingId" type="button" @click="cancelEdit" style="padding:0.4rem 1rem;background:#95a5a6;color:white;border:none;border-radius:4px;cursor:pointer;">Cancel</button>
    </form>
    <table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;">
      <thead style="background:#ecf0f1;">
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Created At</th><th>Actions</th></tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ new Date(user.created_at).toLocaleString() }}</td>
          <td>
            <button @click="startEdit(user)" style="margin-right:0.5rem;padding:0.3rem 0.7rem;background:#3498db;color:white;border:none;border-radius:4px;cursor:pointer;">Edit</button>
            <button @click="deleteUser(user.id)" style="padding:0.3rem 0.7rem;background:#e74c3c;color:white;border:none;border-radius:4px;cursor:pointer;">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="error" style="color:red;">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API_BASE } from '../config.js'

const BASE = API_BASE
const users = ref([])
const error = ref('')
const editingId = ref(null)
const form = ref({ name: '', email: '' })

async function fetchUsers() {
  try {
    const res = await axios.get(`${BASE}/users`)
    users.value = res.data || []
  } catch (e) {
    error.value = `Failed to fetch users: ${e.message}`
  }
}

function startEdit(user) {
  editingId.value = user.id
  form.value = { name: user.name, email: user.email }
}

function cancelEdit() {
  editingId.value = null
  form.value = { name: '', email: '' }
}

async function submitForm() {
  try {
    if (editingId.value) {
      await axios.put(`${BASE}/users/${editingId.value}`, form.value)
    } else {
      await axios.post(`${BASE}/users`, form.value)
    }
    cancelEdit()
    await fetchUsers()
  } catch (e) {
    error.value = `${editingId.value ? 'Update' : 'Create'} failed: ${e.message}`
  }
}

async function deleteUser(id) {
  try {
    await axios.delete(`${BASE}/users/${id}`)
    await fetchUsers()
  } catch (e) {
    error.value = `Delete failed: ${e.message}`
  }
}

onMounted(fetchUsers)
</script>
