<template>
  <div class="editor-page">

    <!-- Top bar -->
    <div class="editor-topbar">
      <div class="topbar-left">
        <button class="btn btn-ghost btn-sm" @click="$router.back()">← Назад</button>
        <div class="scenario-title-wrap">
          <span v-if="!editingTitle" class="scenario-title" @dblclick="startEditTitle">
            {{ scenario.name || 'Без названия' }}
          </span>
          <input
            v-else
            v-model="titleDraft"
            class="title-input"
            @blur="saveTitle"
            @keyup.enter="saveTitle"
            @keyup.escape="editingTitle = false"
            ref="titleInputRef"
          />
        </div>
        <span class="badge" :class="scenario.active ? 'badge-green' : 'badge-gray'">
          {{ scenario.active ? 'Активен' : 'Черновик' }}
        </span>
      </div>

      <div class="topbar-right">
        <span v-if="saving" class="saving-hint">Сохранение...</span>
        <span v-else-if="lastSaved" class="saving-hint saved">✅ Сохранено</span>
        <button class="btn btn-secondary btn-sm" @click="toggleActive">
          {{ scenario.active ? '⏸ Деактивировать' : '▶ Активировать' }}
        </button>
        <button class="btn btn-primary btn-sm" :disabled="saving" @click="save">
          💾 Сохранить
        </button>
      </div>
    </div>

    <!-- Editor body -->
    <div class="editor-body">
      <!-- Toolbar -->
      <Toolbar
        v-model:trigger="scenario.trigger"
        @add="addNode"
      />

      <!-- Canvas -->
      <ScenarioCanvas
        v-if="!loading"
        v-model:nodes="scenario.nodes"
        v-model:edges="scenario.edges"
      />
      <div v-else class="canvas-loading">Загрузка сценария...</div>
    </div>

    <!-- Toast -->
    <div class="toast-wrap">
      <div v-for="t in toasts" :key="t.id" class="toast" :class="t.type">{{ t.msg }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Toolbar        from '../components/editor/Toolbar.vue'
import ScenarioCanvas from '../components/editor/ScenarioCanvas.vue'
import { ScenariosAPI } from '../api/index'
import { useToast } from '../composables/useToast'

const route  = useRoute()
const router = useRouter()
const toast  = useToast()
const { toasts } = toast

// ── State ──────────────────────────────────────────────────────────────────
const loading = ref(true)
const saving  = ref(false)
const lastSaved = ref(false)

const scenario = reactive({
  id:          null,
  name:        '',
  description: '',
  trigger:     '',
  active:      false,
  nodes:       [],
  edges:       [],
})

// Title editing
const editingTitle  = ref(false)
const titleDraft    = ref('')
const titleInputRef = ref(null)

// ── Node ID counter ────────────────────────────────────────────────────────
let nodeCounter = 1
function nextId() {
  // Make sure id doesn't collide with existing
  const existing = new Set(scenario.nodes.map(n => n.id))
  let id = `node_${nodeCounter++}`
  while (existing.has(id)) id = `node_${nodeCounter++}`
  return id
}

// ── Default data per node type ─────────────────────────────────────────────
const NODE_DEFAULTS = {
  message:   { text: '' },
  buttons:   { text: 'Выберите вариант:', buttons: [{ text: '', next: '' }] },
  image:     { url: '', caption: '' },
  delay:     { seconds: 2 },
  input:     { text: '', variable: '' },
  condition: { variable: '', operator: '==', value: '' },
  goto:      { target: '' },
  start:     {},
  end:       {},
}

// ── Load scenario ──────────────────────────────────────────────────────────
async function load() {
  loading.value = true
  try {
    const res = await ScenariosAPI.get(route.params.id)
    const d   = res.data
    scenario.id          = d.id
    scenario.name        = d.name
    scenario.description = d.description
    scenario.trigger     = d.trigger
    scenario.active      = !!d.active
    scenario.nodes       = d.nodes || []
    scenario.edges       = d.edges || []

    // Seed counter above max existing node id
    scenario.nodes.forEach(n => {
      const m = n.id.match(/node_(\d+)/)
      if (m) nodeCounter = Math.max(nodeCounter, +m[1] + 1)
    })

    // Ensure there's always a start node
    if (!scenario.nodes.find(n => n.type === 'start')) {
      scenario.nodes.unshift({
        id: 'node_start', type: 'start', x: 100, y: 60, data: { type: 'start' },
      })
    }
  } catch {
    toast.error('Ошибка загрузки сценария')
    router.back()
  }
  loading.value = false
}

// ── Save ───────────────────────────────────────────────────────────────────
async function save() {
  saving.value  = true
  lastSaved.value = false
  try {
    await ScenariosAPI.update(scenario.id, {
      name:    scenario.name,
      trigger: scenario.trigger,
      nodes:   scenario.nodes,
      edges:   scenario.edges,
    })
    lastSaved.value = true
    setTimeout(() => { lastSaved.value = false }, 3000)
  } catch {
    toast.error('Ошибка сохранения')
  }
  saving.value = false
}

async function toggleActive() {
  try {
    const res = await ScenariosAPI.update(scenario.id, { active: !scenario.active })
    scenario.active = !!res.data.active
    toast.info(scenario.active ? 'Сценарий активирован' : 'Сценарий деактивирован')
  } catch { toast.error('Ошибка') }
}

// ── Title edit ─────────────────────────────────────────────────────────────
function startEditTitle() {
  titleDraft.value  = scenario.name
  editingTitle.value = true
  nextTick(() => titleInputRef.value?.focus())
}
async function saveTitle() {
  if (titleDraft.value.trim()) {
    scenario.name = titleDraft.value.trim()
    try {
      await ScenariosAPI.update(scenario.id, { name: scenario.name })
    } catch {}
  }
  editingTitle.value = false
}

// ── Add node ───────────────────────────────────────────────────────────────
function addNode(type) {
  const id = nextId()
  // Spread new nodes so canvas sees change
  const spreadX = 180 + Math.floor(Math.random() * 120)
  const spreadY = 160 + scenario.nodes.length * 140

  scenario.nodes = [
    ...scenario.nodes,
    {
      id,
      type,
      x: spreadX,
      y: spreadY,
      data: { type, ...NODE_DEFAULTS[type] },
    },
  ]
}

onMounted(load)
</script>

<style scoped>
@font-face {
    font-family: 'Lobelia';
    src: url('../frontend/fonts/Lobelia.ttf') format('truetype');
}

@font-face {
    font-family: 'NauryzRedKeds';
    src: url('../frontend/fonts/NauryzRedKeds.ttf') format('truetype');
}

@font-face {
    font-family: 'Gogol';
    src: url('../frontend/fonts/gogol_regular.otf') format('truetype');
}

.editor-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  background: var(--text);
}

/* ── Topbar ── */
.editor-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background: var(--green-light);
  border-bottom: 1px solid var(--green-dark);
  min-height: 54px;
  flex-shrink: 0;
  gap: 12px;
}

.topbar-left  { display: flex; align-items: center; gap: 12px; }
.topbar-right { display: flex; align-items: center; gap: 10px; }

.scenario-title-wrap { display: flex; align-items: center; }
.scenario-title {
  font-size: 20px;
  font-weight: 600;
  font-family: 'NauryzRedKeds';
  color: var(--green-dark);
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 6px;
  transition: background .15s;
}
.scenario-title:hover { background: var(--text); }
.title-input {
  font-size: 18px;
  font-weight: 600;
  background: var(--green-dark);
  border: 1px solid var(--green-light);
  color: var(--text);
  border-radius: 6px;
  padding: 4px 8px;
  width: 240px;
}

.saving-hint { font-size: 14px; color: var(--green-dark); }
.saving-hint.saved { color: var(--green-dark); }

/* ── Body ── */
.editor-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.canvas-loading {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text);
  font-size: 14px;
}

/* ── Toast (local) ── */
.toast-wrap {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 9999;
}
.toast {
  padding: 12px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  animation: toastIn .25s ease;
}
.toast.success { background: var(--green-dark); color: var(--text); }
.toast.error   { background: var(--red);   color: var(--text); }
.toast.info    { background: var(--green-dark); color: var(--text); border: 1px solid var(--green-light); }
@keyframes toastIn {
  from { transform: translateX(40px); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}
</style>
