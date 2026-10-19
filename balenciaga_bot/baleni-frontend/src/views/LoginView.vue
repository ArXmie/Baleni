<template>
  <div class="wrapper">
    <div class="card">
      <div class="logo" style="margin-bottom: 48px">
        <img src="/static/logo.svg" alt="Логотип сайта" />
      </div>
      <form @submit.prevent="onSubmit">
        <h2>Вход</h2>
        <p v-if="error" class="form-error">{{ error }}</p>

        <div class="field">
          <label>Никнейм</label>
          <input v-model="form.nickname" type="text" placeholder="nickname" required />
        </div>

        <div class="field">
          <label>Пароль</label>
          <input v-model="form.password" type="password" required />
        </div>

        <button class="submit-btn" type="submit">Войти</button>
        <p class="register-link">
          Нет аккаунта?
          <router-link :to="{ name: 'register' }">Зарегистрироваться</router-link>
        </p>
      </form>
    </div>
    <div class="footer-bar"></div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const error = ref('')
const form = reactive({ nickname: '', password: '' })

async function onSubmit() {
  error.value = ''
  try {
    await auth.login(form)
    router.push({ name: 'catalog' })
  } catch (e) {
    error.value = e.response?.data?.detail || 'Неверный логин или пароль'
  }
}
</script>