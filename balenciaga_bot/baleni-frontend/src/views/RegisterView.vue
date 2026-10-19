<template>
  <div class="wrapper">
    <div class="card">
      <div class="logo" style="margin-bottom: 48px">
        <img src="/static/logo.svg" alt="Логотип сайта" />
      </div>
      <form @submit.prevent="onSubmit">
        <h2>Регистрация</h2>
        <p v-if="error" class="form-error">{{ error }}</p>

        <div class="field">
          <label>Никнейм</label>
          <input v-model="form.nickname" type="text" required />
        </div>
        <div class="field">
          <label>Email</label>
          <input v-model="form.email" type="email" required />
        </div>
        <div class="field">
          <label>Телефон</label>
          <input v-model="form.telephone" type="text" required />
        </div>
        <div class="field">
          <label>Пароль</label>
          <input v-model="form.password" type="password" required />
        </div>
        <div class="field">
          <label>Повторите пароль</label>
          <input v-model="form.password2" type="password" required />
        </div>

        <button class="submit-btn" type="submit">Зарегистрироваться</button>
        <p class="login-link">
          Уже есть аккаунт?
          <router-link :to="{ name: 'login' }">Войти</router-link>
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
const form = reactive({
  nickname: '', email: '', telephone: '', password: '', password2: '',
})

async function onSubmit() {
  error.value = ''
  try {
    await auth.register(form)
    router.push({ name: 'catalog' })
  } catch (e) {
    error.value = e.message || 'Ошибка регистрации'
  }
}
</script>