<template>
  <div>
    <h2>Products</h2>
    <form @submit.prevent="submitForm" class="product-form">
      <input v-model="form.name" placeholder="Name" required class="form-input" />
      <input v-model="form.description" placeholder="Description" class="form-input" />
      <input v-model.number="form.price" placeholder="Price" type="number" step="0.01" required class="form-input" />
      <button type="submit" class="btn btn-create">
        {{ editingId ? 'Update' : 'Create' }}
      </button>
      <button v-if="editingId" type="button" @click="cancelEdit" class="btn btn-cancel">Cancel</button>
    </form>
    <table class="data-table">
      <thead>
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
            <button @click="startEdit(product)" class="btn btn-edit">Edit</button>
            <button @click="deleteProduct(product.id)" class="btn btn-delete">Delete</button>
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

<style scoped>
.product-form {
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
