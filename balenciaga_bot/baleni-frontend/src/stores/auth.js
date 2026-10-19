import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { usersApi } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const token = ref(localStorage.getItem('token') || null)

  const isAuthenticated = computed(() => !!user.value)
  const nickname = computed(() => user.value?.nickname || '')

  function persist() {
    if (user.value) {
      localStorage.setItem('user', JSON.stringify(user.value))
      localStorage.setItem('token', token.value)
    } else {
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    }
  }

  async function login({ nickname: nick, password }) {
    const { data } = await usersApi.login({ nickname: nick, password })
    user.value = data.user
    token.value = data.token
    persist()
  }

  async function register(payload) {
    if (payload.password !== payload.password2) {
      throw new Error('Пароли не совпадают')
    }
    if (payload.password.length < 6) {
      throw new Error('Пароль минимум 6 символов')
    }
    const { data } = await usersApi.create({
      nickname: payload.nickname,
      email: payload.email,
      telephone: payload.telephone,
      password: payload.password,
    })
    user.value = data
    persist()
  }

  function logout() {
    user.value = null
    token.value = null
    persist()
  }

  return { user, token, isAuthenticated, nickname, login, register, logout }
})