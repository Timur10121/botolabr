import { createRouter, createWebHistory } from 'vue-router'

import LandingView        from '../views/LandingView.vue'
import LoginView          from '../views/LoginView.vue'
import DashboardView      from '../views/DashboardView.vue'
import BotsView           from '../views/BotsView.vue'
import ScenarioEditorView from '../views/ScenarioEditorView.vue'
import SettingsView       from '../views/SettingsView.vue'   // ← новое

const routes = [
  { path: '/',               component: LandingView,        meta: { public: true } },
  { path: '/login',          component: LoginView,          meta: { public: true } },
  { path: '/dashboard',      component: DashboardView },
  { path: '/bots',           component: BotsView },
  { path: '/scenario/:id',   component: ScenarioEditorView },
  { path: '/settings',       component: SettingsView },      // ← новое
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ── Route guard ─────────────────────────────────────────────────────────────
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  if (!token && !to.meta.public) {
    return next('/')
  }
  // Если авторизован и пытается открыть лендинг или логин — редиректим в кабинет
  if (token && (to.path === '/' || to.path === '/login')) {
    return next('/dashboard')
  }
  next()
})

export default router