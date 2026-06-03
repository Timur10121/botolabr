<template>
  <link rel="stylesheet" href="https://fonts-online.ru/css/lobelia">
  <link rel="stylesheet" href="https://fonts-online.ru/css/nauryzredkeds">
  <link rel="stylesheet" href="https://fonts-online.ru/css/gogol">
  <div class="login-page">
    <div class="login-left">
      <button class="back-link" @click="router.push('/')">← На главную</button>
      <div class="brand">
        <span class="brand-name">BOTOLaBR</span>
      </div>
      <h1 class="hero-title">Конструктор<br>Telegram-ботов</h1>
      <p class="hero-sub">Создавайте сценарии, подключайте ботов и автоматизируйте общение с клиентами без единой строки кода.</p>
      <div class="features">
        <div class="feature"><span class="spisok"></span> Визуальный редактор сценариев</div>
        <div class="feature"><span class="spisok"></span> Неограниченное число ботов</div>
        <div class="feature"><span class="spisok"></span> Webhook интеграция</div>
        <div class="feature"><span class="spisok"></span> Настройки аккаунта</div>
      </div>
    </div>

    <div class="login-right">
      <div class="auth-card">
        <!-- Tabs -->
        <div class="tabs">
          <button class="tab" :class="{ active: mode === 'login' }" @click="mode = 'login'">Войти</button>
          <button class="tab" :class="{ active: mode === 'register' }" @click="mode = 'register'">Регистрация</button>
        </div>

        <!-- Login -->
        <form v-if="mode === 'login'" class="auth-form" @submit.prevent="doLogin">
          <div class="form-group">
            <label>Логин</label>
            <input v-model="loginForm.username" placeholder="Ваш логин" required />
          </div>
          <div class="form-group">
            <label>Пароль</label>
            <input v-model="loginForm.password" type="password" placeholder="••••••" required />
          </div>
          <div v-if="error" class="error-msg">{{ error }}</div>
          <button class="btn btn-primary w-full" :disabled="loading" type="submit">
            {{ loading ? 'Вход...' : 'Войти' }}
          </button>
        </form>

        <!-- Register -->
        <form v-else class="auth-form" @submit.prevent="doRegister">
          <div class="form-group">
            <label>Логин</label>
            <input v-model="regForm.username" placeholder="Минимум 3 символа" required />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="regForm.email" type="email" placeholder="you@example.com" required />
          </div>
          <div class="form-group">
            <label>Пароль</label>
            <input v-model="regForm.password" type="password" placeholder="Минимум 6 символов" required />
          </div>
          <div v-if="error" class="error-msg">{{ error }}</div>
          <button class="btn btn-primary w-full" :disabled="loading" type="submit">
            {{ loading ? 'Регистрация...' : 'Создать аккаунт' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route  = useRoute()
const auth   = useAuthStore()

const mode    = ref(route.query.mode === 'register' ? 'register' : 'login')
const loading = ref(false)
const error   = ref('')

const loginForm = ref({ username: '', password: '' })
const regForm   = ref({ username: '', email: '', password: '' })

async function doLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(loginForm.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка входа'
  } finally {
    loading.value = false
  }
}

async function doRegister() {
  error.value = ''
  loading.value = true
  try {
    await auth.register(regForm.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
}

/* ── Left ── */
.login-left {
  flex: 1;
  background: linear-gradient(135deg, #0B5000 40%, #ADF36C 100%);
  padding: 60px 64px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-right: 1px solid var(--green-dark);
}

.back-link {
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: clamp(14px, 2vw, 18px);
  cursor: pointer;
  padding: 0;
  margin-bottom: 40px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: color .2s;
}
.back-link:hover { color: #F6FEDE; }

.brand {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 48px;
}

.brand-name {
  font-size: clamp(44px, 6vw, 72px);
  font-family: 'Lobelia', serif;
  font-weight: 400;
  background: linear-gradient(135deg, var(--green-light));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-title {
  font-size: 44px; font-weight: 800; line-height: 1.2;
  margin-bottom: 16px;
  font-family: 'NauryzRedKeds', serif;
  line-height: 115%;
  letter-spacing: 3px;
  color: var(--text);
}

.hero-sub {
  font-size: clamp(14px, 2vw, 18px);
  color: var(--text);
  line-height: 1.6;
  max-width: 420px;
  margin-bottom: 40px;
}

.spisok {
  display: inline-block;
  width: 14px;
  height: 14px;
  min-width: 14px;
  border-radius: 50%;
  border: 2px solid #ADF36C;
  margin-top: 3px;
  flex-shrink: 0;
}

.features { display: flex; flex-direction: column; gap: 12px; }
.feature {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: clamp(14px, 2vw, 18px);
  color: var(--text-muted);
}

/* ── Right ── */
.login-right {
  width: 480px;
  min-width: 480px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: linear-gradient(45deg, #ADF36C 10%, #0B5000 100%);
}

.auth-card {
  width: 100%; max-width: 400px;
  background: var(--surface);
  border: 1px solid var(--pink-dark);
  border-radius: var(--radius);
  padding: 32px;
}

/* ── Tabs ── */
.tabs {
  display: flex; gap: 0;
  background: var(--surface2);
  border-radius: 8px;
  padding: 4px;
  margin-bottom: 28px;
}
.tab {
  flex: 1; padding: 9px;
  border-radius: 6px;
  font-size: clamp(12px, 2vw, 16px);
  font-weight: 500;
  background: transparent; color: var(--pink-dark);
  transition: all .18s;
}
.tab.active {
  background: var(--pink-dark);
  color: var(--text);
  box-shadow: 0 1px 4px rgba(0,0,0,.3);
}

.btn-primary   { background: var(--pink-dark);  color: #F6FEDE; }
.btn-primary:hover  { background: var(--surface2); }

/* ── Form ── */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.error-msg {
  background: rgba(239,68,68,.12);
  border: 1px solid rgba(239,68,68,.3);
  color: #fca5a5;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 13px;
  margin-bottom: 4px;
}

.w-full { width: 100%; justify-content: center; margin-top: 8px; padding: 12px; }
</style>
