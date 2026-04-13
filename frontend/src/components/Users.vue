<template>
  <div>
    <h2>Users</h2>
    <form @submit.prevent="submitForm" class="user-form">
      <input v-model="form.name" placeholder="Name" required class="form-input" />
      <input v-model="form.email" placeholder="Email" required class="form-input" />
      <button type="submit" class="btn btn-create">
        {{ editingId ? 'Update' : 'Create' }}
      </button>
      <button v-if="editingId" type="button" @click="cancelEdit" class="btn btn-cancel">Cancel</button>
    </form>
    <table class="data-table">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Created At</th><th>Actions</th></tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ new Date(user.created_at).toLocaleString() }}</td>
          <td>
            <button @click="startEdit(user)" class="btn btn-edit">Edit</button>
            <button @click="deleteUser(user.id)" class="btn btn-delete">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="error" class="error-text">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const BASE = 'http://localhost:8080/api'
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

<style scoped>
.user-form {
  margin-bottom: 1rem;
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.form-input {
  padding: 0.4rem;
}

.data-table {
  border-collapse: collapse;
  width: 100%;
}

.data-table th,
.data-table td {
  border: 1px solid #ccc;
  padding: 6px;
}

.data-table thead {
  background: #ecf0f1;
}

.btn {
  border: none;
  border-radius: 4px;
  cursor: pointer;
  color: white;
}

.btn-create {
  padding: 0.4rem 1rem;
  background: #27ae60;
}

.btn-cancel {
  padding: 0.4rem 1rem;
  background: #95a5a6;
}

.btn-edit {
  margin-right: 0.5rem;
  padding: 0.3rem 0.7rem;
  background: #3498db;
}

.btn-delete {
  padding: 0.3rem 0.7rem;
  background: #e74c3c;
}

.error-text {
  color: red;
}
</style>
