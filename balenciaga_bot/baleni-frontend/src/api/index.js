import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const usersApi = {
  list: () => api.get('/users/'),
  create: (data) => api.post('/users/', data),
  update: (id, data) => api.patch(`/users/${id}/`, data),
  login: (credentials) => api.post('/users/login/', credentials),
}

export const productsApi = {
  list: (params) => api.get('/products/', { params }),
  detail: (id) => api.get(`/products/${id}/`),
}

export const categoriesApi = {
  list: () => api.get('/categories/'),
}

export const sizesApi = {
  list: () => api.get('/sizes/'),
}

export const commissionsApi = {
  list: () => api.get('/commissions/'),
  create: (data) => api.post('/commissions/', data),
}

export default api