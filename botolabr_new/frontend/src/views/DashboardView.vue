<template>
  <AppLayout>
  <link rel="stylesheet" href="https://fonts-online.ru/css/lobelia">
  <link rel="stylesheet" href="https://fonts-online.ru/css/nauryzredkeds">
  <link rel="stylesheet" href="https://fonts-online.ru/css/gogol">
    <div class="dashboard">
      <div class="page-header">
        <div>
          <h2>Добро пожаловать, {{ userName }}</h2>
          <p class="sub">Вот что происходит с вашими ботами</p>
        </div>
        <router-link to="/bots" class="btn btn-primary">
          + Подключить бота
        </router-link>
      </div>

      <!-- Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">🤖</div>
          <div class="stat-body">
            <div class="stat-value">{{ stats.bots }}</div>
            <div class="stat-label">Ботов подключено</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📋</div>
          <div class="stat-body">
            <div class="stat-value">{{ stats.scenarios }}</div>
            <div class="stat-label">Сценариев создано</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-body">
            <div class="stat-value">{{ stats.active }}</div>
            <div class="stat-label">Активных сценариев</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🔗</div>
          <div class="stat-body">
            <div class="stat-value">{{ stats.botsActive }}</div>
            <div class="stat-label">Ботов активно</div>
          </div>
        </div>
      </div>

      <!-- Content grid -->
      <div class="content-grid">
        <!-- Recent scenarios -->
        <div class="card">
          <div class="card-header">
            <h3>Последние сценарии</h3>
            <router-link to="/bots" class="btn btn-ghost btn-sm">Все →</router-link>
          </div>
          <div v-if="loading" class="empty-state">Загрузка...</div>
          <div v-else-if="!recentScenarios.length" class="empty-state">
            <p>Сценариев пока нет</p>
            <router-link to="/bots" class="btn btn-secondary btn-sm" style="margin-top:12px">
              Создать первый сценарий
            </router-link>
          </div>
          <div v-else class="scenario-list">
            <div
              v-for="s in recentScenarios"
              :key="s.id"
              class="scenario-item"
              @click="openScenario(s.id)"
            >
              <div class="scenario-info">
                <div class="scenario-name">{{ s.name }}</div>
                <div class="scenario-meta">
                  {{ s.trigger ? `/${s.trigger}` : 'Без триггера' }} ·
                  {{ s.nodes?.length || 0 }} блоков
                </div>
              </div>
              <span class="badge" :class="s.active ? 'badge-green' : 'badge-gray'">
                {{ s.active ? 'Активен' : 'Черновик' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Bots list -->
        <div class="card">
          <div class="card-header">
            <h3>Мои боты</h3>
            <router-link to="/bots" class="btn btn-ghost btn-sm">Управление →</router-link>
          </div>
          <div v-if="loading" class="empty-state">Загрузка...</div>
          <div v-else-if="!bots.length" class="empty-state">
            <p>Нет подключённых ботов</p>
            <router-link to="/bots" class="btn btn-primary btn-sm" style="margin-top:12px">
              + Подключить бота
            </router-link>
          </div>
          <div v-else class="bot-list">
            <div v-for="b in bots" :key="b.id" class="bot-item">
              <div class="bot-avatar">🤖</div>
              <div class="bot-info">
                <div class="bot-name">@{{ b.bot_username }}</div>
                <div class="bot-sub">{{ b.bot_name }}</div>
              </div>
              <span class="badge" :class="b.active ? 'badge-green' : 'badge-gray'">
                {{ b.active ? 'Активен' : 'Выкл' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick start -->
      <div v-if="!bots.length && !loading" class="quickstart card">
        <h3>Быстрый старт</h3>
        <p>Чтобы начать работу с BOTOLABR, выполните несколько простых шагов:</p>
        <div class="steps">
          <div class="step">
            <div class="step-num">1</div>
            <div>
              <div class="step-title">Создайте бота в Telegram</div>
              <div class="step-desc">Напишите @BotFather команду /newbot и получите токен</div>
            </div>
          </div>
          <div class="step">
            <div class="step-num">2</div>
            <div>
              <div class="step-title">Подключите бота</div>
              <div class="step-desc">Вставьте токен в разделе «Боты»</div>
            </div>
          </div>
          <div class="step">
            <div class="step-num">3</div>
            <div>
              <div class="step-title">Создайте сценарий</div>
              <div class="step-desc">Используйте визуальный редактор для построения диалога</div>
            </div>
          </div>
          <div class="step">
            <div class="step-num">4</div>
            <div>
              <div class="step-title">Активируйте webhook</div>
              <div class="step-desc">Укажите URL вашего сервера и бот начнёт отвечать</div>
            </div>
          </div>
        </div>
        <router-link to="/bots" class="btn btn-primary" style="margin-top:20px">
          Начать →
        </router-link>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { BotsAPI, ScenariosAPI } from '../api/index'
import AppLayout from '../components/AppLayout.vue'

const router  = useRouter()
const auth    = useAuthStore()
const loading = ref(true)
const bots    = ref([])
const allScenarios = ref([])

const userName = computed(() => {
  const u = auth.user
  return u?.name || u?.username || 'Пользователь'
})

const recentScenarios = computed(() => allScenarios.value.slice(0, 5))

const stats = computed(() => ({
  bots:       bots.value.length,
  botsActive: bots.value.filter(b => b.active).length,
  scenarios:  allScenarios.value.length,
  active:     allScenarios.value.filter(s => s.active).length,
}))

async function load() {
  loading.value = true
  try {
    const [botsRes, scenRes] = await Promise.all([
      BotsAPI.getAll(),
      ScenariosAPI.getAll(),
    ])
    bots.value         = botsRes.data
    allScenarios.value = scenRes.data
  } catch {}
  loading.value = false
}

function openScenario(id) {
  router.push(`/scenario/${id}`)
}

onMounted(load)
</script>

<style scoped>
.dashboard { padding: 32px; max-width: 1200px; }

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 32px;
}
.page-header h2 {
  font-size: 24px;
  font-size: clamp(18px, 6vw, 40px);
  font-family: 'Lobelia', serif;
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--green-dark);
}
.sub {
  color: var(--green-light);
  font-size: clamp(16px, 2vw, 20px);
  font-family: 'NauryzRedKeds', serif;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}
.stat-card {
  background: linear-gradient(135deg, var(--green-light) 10%, var(--text) 100%);;
  border: 1px solid var(--green-dark);
  border-radius: var(--radius);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.stat-icon { font-size: 28px; }
.stat-value {
  font-size: clamp(24px, 4vw, 36px);
  font-weight: 700;
  line-height: 1;
  color: var(--green-dark);
}
.stat-label {
  font-size: clamp(12px, 2vw, 16px);
  font-weight: 600;
  color: var(--green-dark);
  margin-top: 4px;
}

/* Content grid */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.card-header h3 {
  font-size: clamp(18px, 2vw, 22px); 
  font-weight: 400;
  color: var(--text);
  font-family: 'NauryzRedKeds';
}

.empty-state {
  text-align: center;
  padding: 32px 16px;
  color: var(--text);
  font-size: clamp(12px, 2vw, 16px);
}

/* Scenario list */
.scenario-list { display: flex; flex-direction: column; gap: 8px; }
.scenario-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px; border-radius: 8px;
  border: 1px solid var(--text);
  cursor: pointer; transition: border-color .18s;
}
.scenario-item:hover { border-color: var(--green-dark); }
.scenario-name { font-size: 14px; font-weight: 500; }
.scenario-meta { font-size: 12px; color: var(--green-light); margin-top: 2px; }

/* Bot list */
.bot-list { display: flex; flex-direction: column; gap: 8px; }
.bot-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px; border-radius: 8px;
  border: 1px solid var(--text);
}
.bot-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: var(--text);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; flex-shrink: 0;
}
.bot-info { flex: 1; min-width: 0; }
.bot-name { font-size: 14px; font-weight: 500; }
.bot-sub  { font-size: 12px; color: var(--text-muted); }

/* Quick start */
.quickstart { margin-top: 8px; }
.quickstart h3 { font-size: clamp(18px, 2vw, 22px); font-family: 'NauryzRedKeds'; font-weight: 400; margin-bottom: 8px; }
.quickstart > p { color: var(--green-light); font-size: clamp(12px, 2vw, 16px); font-weight: 600; margin-bottom: 24px; }
.steps { display: flex; flex-direction: column; gap: 16px; }
.step { display: flex; gap: 16px; align-items: flex-start; }
.step-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--green-light); color: var(--green-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: clamp(12px, 2vw, 16px);
  font-weight: 700;
  flex-shrink: 0;
}
.step-title { font-size: clamp(12px, 2vw, 16px); font-weight: 600; }
.step-desc  { font-size: clamp(11px, 2vw, 13px); color: var(--green-light); margin-top: 2px; }

</style>
