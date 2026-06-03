<template>

  <div class="layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <span class="logo-text">BOTOLaBR</span>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-link">
          <span class="nav-icon">🏠</span> Главная
        </router-link>
        <router-link to="/bots" class="nav-link">
          <span class="nav-icon">🤖</span> Боты
        </router-link>
      </nav>

      <div class="sidebar-bottom">
        <!-- User card — кликабельный, ведёт в настройки -->
        <router-link to="/settings" class="user-card">
          <div class="user-avatar">
            <img v-if="user?.avatar" :src="user.avatar" alt="avatar" />
            <span v-else>{{ initials }}</span>
          </div>
          <div class="user-info">
            <div class="user-name">{{ user?.name || user?.username || 'Пользователь' }}</div>
            <div class="user-sub">@{{ user?.username }}</div>
          </div>
          <span class="settings-icon" title="Настройки">⚙️</span>
        </router-link>

        <button class="btn btn-ghost btn-sm logout-btn" @click="handleLogout">
          Выйти
        </button>
      </div>
    </aside>

    <!-- Content -->
    <main class="content">
      <slot />
    </main>

    <!-- Toast container -->
    <div class="toast-wrap">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="toast"
        :class="t.type"
      >{{ t.msg }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'

const auth   = useAuthStore()
const router = useRouter()
const { toasts } = useToast()

const user = computed(() => auth.user)
const initials = computed(() => {
  const n = user.value?.name || user.value?.username || '?'
  return n.slice(0, 2).toUpperCase()
})

async function handleLogout() {
  await auth.logout()
  router.push('/')
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

/* ── Sidebar ──────────────────────────────────────────────────────────── */
.sidebar {
  width: 240px;
  min-width: 240px;
  background: linear-gradient(135deg, var(--green-dark) 10%, #3F9C30 100%);
  border-right: 1px solid var(--green-light);
  display: flex;
  flex-direction: column;
  padding: 0;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 24px 20px 20px;
  border-bottom: 1px solid var(--green-light);
}
.logo-text {
  font-weight: 700;
  font-size: clamp(16px, 2vw, 20px);
  font-family: 'Lobelia', serif;
  background: var(--green-light);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: clamp(12px, 2vw, 16px);
  color: var(--green-light);
  transition: all .18s;
}
.nav-link:hover { background: var(--green-light); color: var(--green-dark); }
.nav-link.router-link-active {
  background: rgba(22,101,52,.25);
  color: var(--green-light);
}
.nav-icon { font-size: 16px; }

.sidebar-bottom {
  padding: 16px 12px;
  border-top: 1px solid var(--green-light);
}

/* User card — теперь это ссылка */
.user-card {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  padding: 8px 6px;
  border-radius: 8px;
  text-decoration: none;
  background: var(--green-light);
  transition: background .18s;
  cursor: pointer;
}
.user-card:hover {
  background: var(--text);
}
.user-card.router-link-active {
  background: rgba(22,101,52,.25);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--green-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: var(--green-light);
  overflow: hidden;
  flex-shrink: 0;
}
.user-avatar img { width: 100%; height: 100%; object-fit: cover; }
.user-info { min-width: 0; flex: 1; }
.user-name { font-size: 13px; font-weight: 600; color: var(--green-dark) ;overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.user-sub  { font-size: 11px; color: var(--green-dark); }

.settings-icon {
  font-size: 16px;
  opacity: .6;
  flex-shrink: 0;
  transition: opacity .18s, transform .25s;
}
.user-card:hover .settings-icon {
  opacity: 1;
  transform: rotate(60deg);
}

.logout-btn { background: var(--green-light); width: 100%; justify-content: center; }

/* ── Content ──────────────────────────────────────────────────────────── */
.content {
  flex: 1;
  overflow-y: auto;
  min-width: 0;
}
</style>