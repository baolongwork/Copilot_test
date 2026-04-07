<template>
  <div>
    <h2>Products</h2>
    <form @submit.prevent="submitForm" style="margin-bottom:1rem;display:flex;gap:0.5rem;flex-wrap:wrap;">
      <input v-model="form.name" placeholder="Name" required style="padding:0.4rem;" />
      <input v-model="form.description" placeholder="Description" style="padding:0.4rem;" />
      <input v-model.number="form.price" placeholder="Price" type="number" step="0.01" required style="padding:0.4rem;" />
      <button type="submit" style="padding:0.4rem 1rem;background:#27ae60;color:white;border:none;border-radius:4px;cursor:pointer;">
        {{ editingId ? 'Update' : 'Create' }}
      </button>
      <button v-if="editingId" type="button" @click="cancelEdit" style="padding:0.4rem 1rem;background:#95a5a6;color:white;border:none;border-radius:4px;cursor:pointer;">Cancel</button>
    </form>
    <table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;">
      <thead style="background:#ecf0f1;">
        <tr><th>ID</th><th>Name</th><th>Description</th><th>Price</th><th>Created At</th><th>Actions</th></tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id">
          <td>{{ product.id }}</td>
          <td>{{ product.name }}</td>
          <td>{{ product.description }}</td>
          <td>${{ (product.price ?? 0).toFixed(2) }}</td>
          <td>{{ new Date(product.created_at).toLocaleString() }}</td>
          <td>
            <button @click="startEdit(product)" style="margin-right:0.5rem;padding:0.3rem 0.7rem;background:#3498db;color:white;border:none;border-radius:4px;cursor:pointer;">Edit</button>
            <button @click="deleteProduct(product.id)" style="padding:0.3rem 0.7rem;background:#e74c3c;color:white;border:none;border-radius:4px;cursor:pointer;">Delete</button>
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
const products = ref([])
const error = ref('')
const editingId = ref(null)
const form = ref({ name: '', description: '', price: 0 })

async function fetchProducts() {
  try {
    const res = await axios.get(`${BASE}/products`)
    products.value = res.data || []
  } catch (e) {
    error.value = `Failed to fetch products: ${e.message}`
  }
}

function startEdit(product) {
  editingId.value = product.id
  form.value = { name: product.name, description: product.description, price: product.price }
}

function cancelEdit() {
  editingId.value = null
  form.value = { name: '', description: '', price: 0 }
}

async function submitForm() {
  try {
    if (editingId.value) {
      await axios.put(`${BASE}/products/${editingId.value}`, form.value)
    } else {
      await axios.post(`${BASE}/products`, form.value)
    }
    cancelEdit()
    await fetchProducts()
  } catch (e) {
    error.value = `${editingId.value ? 'Update' : 'Create'} failed: ${e.message}`
  }
}

async function deleteProduct(id) {
  try {
    await axios.delete(`${BASE}/products/${id}`)
    await fetchProducts()
  } catch (e) {
    error.value = `Delete failed: ${e.message}`
  }
}

onMounted(fetchProducts)
</script>
