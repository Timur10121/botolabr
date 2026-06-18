<template>
  <AppLayout>
    <div class="bots-page">

      <!-- Header -->
      <div class="page-header">
        <div>
          <h2>Мои боты</h2>
          <p class="sub">Управляйте Telegram-ботами и их сценариями</p>
        </div>
        <button class="btn btn-primary" @click="showConnectModal = true">
          + Подключить бота
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="empty-state">Загрузка...</div>

      <!-- No bots -->
      <div v-else-if="!bots.length" class="no-bots card">
        <div class="no-bots-icon"><img src="\icons.svg" alt="BOTOLABR" @error="e => e.target.style.display='none'" /></div>
        <h3>Нет подключённых ботов</h3>
        <p>Создайте бота через @BotFather в Telegram и подключите его здесь</p>
        <button class="btn btn-primary" @click="showConnectModal = true">
          + Подключить первого бота
        </button>
      </div>

      <!-- Bots list -->
      <div v-else class="bots-grid">
        <div v-for="bot in bots" :key="bot.id" class="bot-card card">
          <div class="bot-card-header">
            <div class="bot-info">
              <div class="bot-username">@{{ bot.bot_username }}</div>
              <div class="bot-name">{{ bot.bot_name }}</div>
            </div>
            <span class="badge" :class="bot.active ? 'badge-green' : 'badge-gray'">
              {{ bot.active ? 'Активен' : 'Выключен' }}
            </span>
          </div>

          <!-- Webhook status -->
          <div class="webhook-row">
            <div class="webhook-label">Webhook:</div>
            <div class="webhook-val">
              <span v-if="webhookMap[bot.id] === undefined" class="wh-unknown">Загрузка...</span>
              <span v-else-if="webhookMap[bot.id]" class="wh-ok">Активен</span>
              <span v-else class="wh-none">Не установлен</span>
            </div>
          </div>

          <!-- Webhook URL input -->
          <div v-if="activeWebhookBot === bot.id" class="webhook-form">
            <input
              v-model="webhookUrl"
              placeholder="https://your-server.com"
              @keyup.enter="setWebhook(bot)"
            />
            <div class="webhook-actions">
              <button class="btn btn-primary btn-sm" :disabled="whLoading" @click="setWebhook(bot)">
                {{ whLoading ? '...' : 'Установить' }}
              </button>
              <button class="btn btn-secondary btn-sm" @click="activeWebhookBot = null">
                Отмена
              </button>
            </div>
          </div>

          <!-- Scenarios count -->
          <div class="scenarios-count">
            <img src="/image/file.svg" alt="" class="scenarios-count__icon" />
            {{ scenariosCount(bot.id) }} сценариев
          </div>

          <!-- Actions -->
          <div class="bot-actions">
           <button
              class="btn btn-secondary btn-sm"
              @click="openScenarios(bot)"
            >
              <img
                src="/image/link.svg"
                alt=""
                class="btn-icon"
              />
              Сценарии
          </button>
          <button
            class="btn btn-secondary btn-sm"
            @click="toggleWebhookForm(bot)"
          >
            <img
            src="/image/robot-face.svg"
            alt=""
            class="btn-icon"
          />
          Webhook
        </button>
            <button
              v-if="webhookMap[bot.id]"
              class="btn btn-secondary btn-sm"
              @click="deleteWebhook(bot)"
            >
              ❌ Снять webhook
            </button>
            <button class="btn btn-secondary btn-sm" @click="toggleBot(bot)">
              {{ bot.active ? '⏸ Выкл' : '▶ Вкл' }}
            </button>
            <button class="btn btn-danger btn-sm" @click="confirmDelete(bot)">
              🗑
            </button>
          </div>
        </div>
      </div>

      <!-- ── Scenarios panel ── -->
      <div v-if="selectedBot" class="scenarios-section">
        <div class="scenarios-header">
          <h3>Сценарии бота @{{ selectedBot.bot_username }}</h3>
          <button class="btn btn-primary btn-sm" @click="showCreateScenario = true">
            + Новый сценарий
          </button>
        </div>

        <div v-if="scenariosLoading" class="empty-state">Загрузка сценариев...</div>
        <div v-else-if="!scenarios.length" class="empty-state">
          Нет сценариев. Создайте первый!
        </div>
        <div v-else class="scenarios-list">
          <div v-for="s in scenarios" :key="s.id" class="scenario-row card">
            <div class="scenario-left">
              <div class="scenario-name">{{ s.name }}</div>
              <div class="scenario-meta">
                <span v-if="s.trigger" class="trigger-badge">{{ s.trigger }}</span>
                <span class="meta-item">{{ s.nodes?.length || 0 }} блоков</span>
                <span class="meta-item">{{ s.edges?.length || 0 }} переходов</span>
              </div>
            </div>
            <div class="scenario-right">
              <span class="badge" :class="s.active ? 'badge-green' : 'badge-gray'">
                {{ s.active ? 'Активен' : 'Черновик' }}
              </span>
              <button
                class="btn btn-sm"
                :class="s.active ? 'btn-secondary' : 'btn-primary'"
                @click="toggleScenario(s)"
              >
                {{ s.active ? 'Деактивировать' : 'Активировать' }}
              </button>
              <button
                class="btn btn-secondary btn-sm"
                @click="editScenario(s)"
              >
                <img
                  src="/image/pencil.svg"
                  alt=""
                  class="btn-icon"
                />
                Редактор
              </button>
              <button class="btn btn-danger btn-sm" @click="confirmDeleteScenario(s)">
                🗑
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ── Connect bot modal ── -->
      <div v-if="showConnectModal" class="modal-overlay" @click.self="closeConnectModal">
        <div class="modal">
          <h3>Подключить Telegram-бота</h3>

          <div v-if="connectStep === 1">
            <p class="modal-hint">
              1. Напишите <strong>@BotFather</strong> в Telegram<br>
              2. Отправьте команду <code>/newbot</code><br>
              3. Скопируйте полученный токен
            </p>
            <div class="form-group" style="margin-top:16px">
              <label>Токен бота</label>
              <input
                v-model="newBotToken"
                placeholder="1234567890:AABBCC..."
                @keyup.enter="checkBot"
              />
            </div>
            <div v-if="connectError" class="error-msg">{{ connectError }}</div>
            <div class="modal-actions">
              <button class="btn btn-secondary" @click="closeConnectModal">Отмена</button>
              <button class="btn btn-primary" :disabled="connectLoading" @click="checkBot">
                {{ connectLoading ? 'Проверка...' : 'Проверить токен' }}
              </button>
            </div>
          </div>

          <div v-if="connectStep === 2">
            <div class="bot-preview">
              <div class="bp-avatar">
                <img src="/image/robot-face.svg"/>
              </div>
              <div>
                <div class="bp-name">{{ checkedBot.bot_name }}</div>
                <div class="bp-user">@{{ checkedBot.bot_username }}</div>
              </div>
              <span class="badge badge-green">Найден</span>
            </div>
            <p class="modal-hint" style="margin-top:12px">
              Бот найден! Подключаем его к вашему аккаунту.
            </p>
            <div v-if="connectError" class="error-msg">{{ connectError }}</div>
            <div class="modal-actions">
              <button class="btn btn-secondary" @click="connectStep = 1">Назад</button>
              <button class="btn btn-primary" :disabled="connectLoading" @click="connectBot">
                {{ connectLoading ? 'Подключение...' : 'Подключить' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ── Create scenario modal ── -->
      <div v-if="showCreateScenario" class="modal-overlay" @click.self="showCreateScenario = false">
        <div class="modal">
          <h3>Новый сценарий</h3>
          <div class="form-group">
            <label>Название</label>
            <input v-model="newScenario.name" placeholder="Например: Приветствие" />
          </div>
          <div class="form-group">
            <label>Описание (необязательно)</label>
            <input v-model="newScenario.description" placeholder="Краткое описание" />
          </div>
          <div class="form-group">
            <label>Триггер (команда)</label>
            <input v-model="newScenario.trigger" placeholder="/start" />
            <div class="field-hint">Команда, запускающая сценарий. Например: /start, /help</div>
          </div>
          <div v-if="createError" class="error-msg">{{ createError }}</div>
          <div class="modal-actions">
            <button class="btn btn-secondary" @click="showCreateScenario = false">Отмена</button>
            <button class="btn btn-primary" :disabled="createLoading" @click="createScenario">
              {{ createLoading ? 'Создание...' : 'Создать' }}
            </button>
          </div>
        </div>
      </div>

      <!-- ── Delete bot confirm ── -->
      <div v-if="deleteBotTarget" class="modal-overlay" @click.self="deleteBotTarget = null">
        <div class="modal">
          <h3>Удалить бота?</h3>
          <p style="color:var(--text-muted);font-size:14px;margin-bottom:20px">
            Бот <strong>@{{ deleteBotTarget.bot_username }}</strong> и все его сценарии будут удалены. Это действие нельзя отменить.
          </p>
          <div class="modal-actions">
            <button class="btn btn-secondary" @click="deleteBotTarget = null">Отмена</button>
            <button class="btn btn-danger" @click="deleteBot">Удалить</button>
          </div>
        </div>
      </div>

      <!-- ── Delete scenario confirm ── -->
      <div v-if="deleteScenarioTarget" class="modal-overlay" @click.self="deleteScenarioTarget = null">
        <div class="modal">
          <h3>Удалить сценарий?</h3>
          <p style="color:var(--text-muted);font-size:14px;margin-bottom:20px">
            Сценарий <strong>{{ deleteScenarioTarget.name }}</strong> будет удалён безвозвратно.
          </p>
          <div class="modal-actions">
            <button class="btn btn-secondary" @click="deleteScenarioTarget = null">Отмена</button>
            <button class="btn btn-danger" @click="doDeleteScenario">Удалить</button>
          </div>
        </div>
      </div>

    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { BotsAPI, ScenariosAPI } from '../api/index'
import { useToast } from '../composables/useToast'

const router = useRouter()
const toast  = useToast()

// ── State ──────────────────────────────────────────────────────────────────
const loading          = ref(true)
const bots             = ref([])
const webhookMap       = ref({})          // botId → bool
const scenariosMap     = ref({})          // botId → scenarios[]
const selectedBot      = ref(null)
const scenarios        = ref([])
const scenariosLoading = ref(false)

// Connect modal
const showConnectModal = ref(false)
const connectStep      = ref(1)
const newBotToken      = ref('')
const checkedBot       = ref(null)
const connectLoading   = ref(false)
const connectError     = ref('')

// Webhook
const activeWebhookBot = ref(null)
const webhookUrl       = ref('')
const whLoading        = ref(false)

// Create scenario
const showCreateScenario = ref(false)
const newScenario        = ref({ name: '', description: '', trigger: '/start' })
const createLoading      = ref(false)
const createError        = ref('')

// Delete
const deleteBotTarget      = ref(null)
const deleteScenarioTarget = ref(null)

// ── Computed ───────────────────────────────────────────────────────────────
function scenariosCount(botId) {
  return scenariosMap.value[botId]?.length || 0
}

// ── Load ───────────────────────────────────────────────────────────────────
async function load() {
  loading.value = true
  try {
    const res = await BotsAPI.getAll()
    bots.value = res.data
    // Load webhook info & scenarios count for each bot
    bots.value.forEach(bot => {
      loadWebhookInfo(bot)
      loadScenariosCount(bot.id)
    })
  } catch (e) {
    toast.error('Ошибка загрузки ботов')
  }
  loading.value = false
}

async function loadWebhookInfo(bot) {
  try {
    const res = await BotsAPI.webhookInfo(bot.id)
    webhookMap.value[bot.id] = !!(res.data?.result?.url)
  } catch {
    webhookMap.value[bot.id] = false
  }
}

async function loadScenariosCount(botId) {
  try {
    const res = await ScenariosAPI.getAll(botId)
    scenariosMap.value[botId] = res.data
  } catch {}
}

// ── Connect bot ────────────────────────────────────────────────────────────
function closeConnectModal() {
  showConnectModal.value = false
  connectStep.value = 1
  newBotToken.value = ''
  connectError.value = ''
  checkedBot.value = null
}

async function checkBot() {
  if (!newBotToken.value.trim()) return
  connectError.value = ''
  connectLoading.value = true
  try {
    const res = await BotsAPI.check(newBotToken.value.trim())
    checkedBot.value = res.data
    connectStep.value = 2
  } catch (e) {
    connectError.value = e.response?.data?.detail || 'Неверный токен'
  }
  connectLoading.value = false
}

async function connectBot() {
  connectError.value = ''
  connectLoading.value = true
  try {
    const res = await BotsAPI.connect(newBotToken.value.trim())
    bots.value.unshift(res.data)
    webhookMap.value[res.data.id] = false
    scenariosMap.value[res.data.id] = []
    toast.success(`Бот @${res.data.bot_username} подключён!`)
    closeConnectModal()
  } catch (e) {
    connectError.value = e.response?.data?.detail || 'Ошибка подключения'
  }
  connectLoading.value = false
}

// ── Toggle bot ─────────────────────────────────────────────────────────────
async function toggleBot(bot) {
  try {
    const res = await BotsAPI.toggle(bot.id)
    bot.active = res.data.active
    toast.info(`Бот ${bot.active ? 'включён' : 'выключен'}`)
  } catch {
    toast.error('Ошибка')
  }
}

// ── Delete bot ─────────────────────────────────────────────────────────────
function confirmDelete(bot) { deleteBotTarget.value = bot }

async function deleteBot() {
  try {
    await BotsAPI.delete(deleteBotTarget.value.id)
    bots.value = bots.value.filter(b => b.id !== deleteBotTarget.value.id)
    if (selectedBot.value?.id === deleteBotTarget.value.id) selectedBot.value = null
    toast.success('Бот удалён')
  } catch { toast.error('Ошибка удаления') }
  deleteBotTarget.value = null
}

// ── Webhook ────────────────────────────────────────────────────────────────
function toggleWebhookForm(bot) {
  activeWebhookBot.value = activeWebhookBot.value === bot.id ? null : bot.id
  webhookUrl.value = ''
}

async function setWebhook(bot) {
  if (!webhookUrl.value.trim()) return
  whLoading.value = true
  try {
    await BotsAPI.setWebhook(bot.id, webhookUrl.value.trim())
    webhookMap.value[bot.id] = true
    activeWebhookBot.value = null
    toast.success('Webhook установлен!')
  } catch (e) {
    toast.error(e.response?.data?.detail || 'Ошибка webhook')
  }
  whLoading.value = false
}

async function deleteWebhook(bot) {
  try {
    await BotsAPI.delWebhook(bot.id)
    webhookMap.value[bot.id] = false
    toast.info('Webhook снят')
  } catch { toast.error('Ошибка') }
}

// ── Scenarios ──────────────────────────────────────────────────────────────
async function openScenarios(bot) {
  selectedBot.value = bot
  scenariosLoading.value = true
  try {
    const res = await ScenariosAPI.getAll(bot.id)
    scenarios.value = res.data
    scenariosMap.value[bot.id] = res.data
  } catch { toast.error('Ошибка загрузки сценариев') }
  scenariosLoading.value = false
  // Scroll to scenarios
  setTimeout(() => {
    document.querySelector('.scenarios-section')?.scrollIntoView({ behavior: 'smooth' })
  }, 100)
}

async function toggleScenario(s) {
  try {
    const res = await ScenariosAPI.update(s.id, { active: !s.active })
    Object.assign(s, res.data)
    toast.info(`Сценарий ${s.active ? 'активирован' : 'деактивирован'}`)
  } catch { toast.error('Ошибка') }
}

function editScenario(s) {
  router.push(`/scenario/${s.id}`)
}

function confirmDeleteScenario(s) { deleteScenarioTarget.value = s }

async function doDeleteScenario() {
  try {
    await ScenariosAPI.delete(deleteScenarioTarget.value.id)
    scenarios.value = scenarios.value.filter(s => s.id !== deleteScenarioTarget.value.id)
    if (selectedBot.value) scenariosMap.value[selectedBot.value.id] = scenarios.value
    toast.success('Сценарий удалён')
  } catch { toast.error('Ошибка') }
  deleteScenarioTarget.value = null
}

async function createScenario() {
  if (!newScenario.value.name.trim()) {
    createError.value = 'Введите название'
    return
  }
  createError.value = ''
  createLoading.value = true
  try {
    const res = await ScenariosAPI.create({
      bot_id:      selectedBot.value.id,
      name:        newScenario.value.name.trim(),
      description: newScenario.value.description.trim(),
      trigger:     newScenario.value.trigger.trim(),
      nodes:       [],
      edges:       [],
    })
    scenarios.value.unshift(res.data)
    if (selectedBot.value) scenariosMap.value[selectedBot.value.id] = scenarios.value
    showCreateScenario.value = false
    newScenario.value = { name: '', description: '', trigger: '/start' }
    toast.success('Сценарий создан!')
    router.push(`/scenario/${res.data.id}`)
  } catch (e) {
    createError.value = e.response?.data?.detail || 'Ошибка создания'
  }
  createLoading.value = false
}

onMounted(load)
</script>

<style scoped>
.bots-page{
  padding: 32px;
  max-width: 1100px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 28px;
}
.page-header h2 {
  font-size: clamp(18px, 6vw, 40px);
  font-family: 'Lobelia', serif;
  font-weight: 400;
  margin-bottom: 4px;
  color: var(--green-dark);
}
.sub {
  color: var(--green-light);
  font-size: clamp(16px, 2vw, 20px);
  font-family: 'NauryzRedKeds', serif;
}

/* No bots */
.no-bots {
  text-align: center;
  padding: 60px 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
.no-bots-icon { font-size: 48px; }
.no-bots h3   { font-size: clamp(18px, 2vw, 22px); font-weight: 600; font-family: 'Roboto slab', serif; }
.no-bots p    { color: var(--text); font-size: clamp(12px, 2vw, 18px); max-width: 320px; }

/* Bots grid */
.bots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.bot-card { display: flex; flex-direction: column; gap: 12px; }

.bot-card-header { display: flex; align-items: center; gap: 12px; }
.bot-avatar {
  width: 44px; height: 44px; border-radius: 50%;
  background: var(--surface2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px; flex-shrink: 0;
}
.bot-info { flex: 1; }
.bot-username { font-size: clamp(18px, 2vw, 22px); font-weight: 600; font-family: 'Roboto slab', serif; }
.bot-name     { font-size: clamp(12px, 2vw, 18px); color: var(--green-light); font-family: 'Roboto slab', serif; }

/* Webhook row */
.webhook-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: clamp(12px, 2vw, 18px);
  color: var(--green-dark);
  background: var(--text);
  border-radius: 8px;
  padding: 8px 12px;
}
.webhook-label { font-weight: 500; }
.wh-ok    { color: var(--green-dark); }
.wh-none  { color: var(--green-dark); }
.wh-unknown { color: var(--green-dark); }

input, textarea, select {
  font-family: 'Roboto slab';
  outline: none;
  background: var(--text);
  border: 1px solid var(--green-dark);
  color: var(--pink-dark);
  border-radius: 8px;
  padding: 10px 14px;
  width: 100%;
  font-size: clamp(12px, 2vw, 16px);
  transition: border-color .2s;
}
input:focus, textarea:focus, select:focus {
  border-color: var(--text);
}
input::placeholder, textarea::placeholder { color: var(--green-dark); }

/* Webhook form */
.webhook-form { display: flex; flex-direction: column; gap: 8px; }
.webhook-actions { display: flex; gap: 8px; }

/* Scenarios count */
.scenarios-count { font-size: 13px; color: var(--text); }

/* Bot actions */
.bot-actions { display: flex; flex-wrap: wrap; gap: 6px; }

/* ── Scenarios section ── */
.scenarios-section {
  margin-top: 8px;
  border-top: 1px solid var(--green-dark);
  padding-top: 28px;
}
.scenarios-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 16px;
}
.scenarios-header h3 { font-size: 18px; font-weight: 600; }

.scenarios-list { display: flex; flex-direction: column; gap: 10px; }

.scenario-row {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; flex-wrap: wrap;
}
.scenario-left { flex: 1; min-width: 0; }
.scenario-name { font-size: 15px; font-weight: 600; margin-bottom: 4px; }
.scenario-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.trigger-badge {
  background: rgba(22,101,52,.25); color: var(--green-light);
  padding: 2px 8px; border-radius: 20px; font-size: 12px; font-family: monospace;
}
.meta-item { font-size: 12px; color: var(--text-muted); }

.scenario-right { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }

/* Modal extras */
.modal-hint {
  font-size: clamp(12px, 2vw, 16px); font-family: 'Roboto slab', serif; color: var(--text); line-height: 1.6;
  background: var(--surface2); border-radius: 8px; padding: 12px 14px;
  margin-bottom: 4px;
}
.modal-hint code {
  background: var(--pink-dark); padding: 2px 6px; border-radius: 4px;
  font-size: 13px;
}

.bot-preview {
  display: flex; align-items: center; gap: 12px;
  background: var(--surface2); border-radius: 10px; padding: 14px;
}
.bp-avatar { font-size: 28px; }
.bp-name   { font-size: 15px; font-weight: 600; }
.bp-user   { font-size: 13px; color: var(--text); }

.field-hint { font-size: 12px; color: var(--text); margin-top: 4px; }

.empty-state {
  text-align: center; padding: 40px;
  color: var(--green-dark); font-size: 14px;
}

.error-msg {
  background: rgba(239,68,68,.12);
  border: 1px solid rgba(239,68,68,.3);
  color: #fca5a5; border-radius: 8px;
  padding: 10px 14px; font-size: 13px;
  margin-bottom: 4px;
}

</style>
