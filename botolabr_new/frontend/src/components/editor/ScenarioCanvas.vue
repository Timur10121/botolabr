<template>
  <div class="canvas-wrap">
    <VueFlow
      :nodes="flowNodes"
      :edges="flowEdges"
      :default-edge-options="edgeOptions"
      :node-types="nodeTypes"
      fit-view-on-init
      :zoom-on-scroll="true"
      :pan-on-scroll="false"
      :pan-on-drag="true"
      :zoom-on-double-click="false"
      :prevent-scrolling="true"
      class="vue-flow-canvas"
      @connect="onConnect"
      @node-drag-stop="onNodeDragStop"
      @pane-click="selectedNode = null"
    >
      <Background pattern-color="#2e3347" :gap="20" />

      <template #node-custom="nodeProps">
        <Handle type="target" :position="Position.Top"    class="flow-handle flow-handle-top" />
        <Handle type="source" :position="Position.Bottom" class="flow-handle flow-handle-bot" />
        <NodeCard
          :id="nodeProps.id"
          :data="nodeProps.data"
          :selected="nodeProps.selected"
          @update="onNodeDataUpdate"
          @delete="onNodeDelete"
        />
      </template>

      <template #node-start-node="nodeProps">
        <Handle type="source" :position="Position.Bottom" class="flow-handle flow-handle-bot" />
        <NodeCard
          :id="nodeProps.id"
          :data="nodeProps.data"
          :selected="nodeProps.selected"
          @update="onNodeDataUpdate"
          @delete="onNodeDelete"
        />
      </template>

      <template #node-end-node="nodeProps">
        <Handle type="target" :position="Position.Top" class="flow-handle flow-handle-top" />
        <NodeCard
          :id="nodeProps.id"
          :data="nodeProps.data"
          :selected="nodeProps.selected"
          @update="onNodeDataUpdate"
          @delete="onNodeDelete"
        />
      </template>
    </VueFlow>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import {
  VueFlow,
  Handle, Position,
  MarkerType,
} from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'

import NodeCard from './NodeCard.vue'

const props = defineProps({
  nodes: { type: Array, default: () => [] },
  edges: { type: Array, default: () => [] },
})
const emit = defineEmits(['update:nodes', 'update:edges'])

const nodeTypes = {
  custom:       'custom',
  'start-node': 'start-node',
  'end-node':   'end-node',
}

const selectedNode = ref(null)

const posCache = ref({})

// Инициализируем кэш при первой загрузке нод
watch(
  () => props.nodes,
  (newNodes) => {
    newNodes.forEach(n => {
      // Добавляем в кэш только новые ноды (чтобы не сбрасывать перетащенные)
      if (!(n.id in posCache.value)) {
        posCache.value[n.id] = { x: n.x ?? 100, y: n.y ?? 100 }
      }
    })
    // Удаляем из кэша ноды которых больше нет
    const ids = new Set(newNodes.map(n => n.id))
    Object.keys(posCache.value).forEach(id => {
      if (!ids.has(id)) delete posCache.value[id]
    })
  },
  { immediate: true, deep: false }
)

// ── flowNodes берёт позиции из posCache, а не из props.nodes ──────────────
const flowNodes = computed(() =>
  props.nodes.map(n => ({
    id:       n.id,
    type:     n.type === 'start' ? 'start-node'
            : n.type === 'end'   ? 'end-node'
            : 'custom',
    // Позиция из локального кэша — не сбрасывается при редактировании данных
    position: posCache.value[n.id] ?? { x: n.x ?? 100, y: n.y ?? 100 },
    data:     { type: n.type, ...(n.data || {}), _id: n.id },
  }))
)

const flowEdges = computed(() =>
  props.edges.map(e => ({
    id:           e.id,
    source:       e.source,
    target:       e.target,
    label:        e.label || '',
    animated:     true,
    markerEnd:    { type: MarkerType.ArrowClosed, color: '#22c55e' },
    style:        { stroke: '#22c55e', strokeWidth: 2 },
    labelStyle:   { fill: '#94a3b8', fontSize: 11 },
    labelBgStyle: { fill: '#1a1d27' },
  }))
)

const edgeOptions = {
  animated:  true,
  markerEnd: { type: MarkerType.ArrowClosed, color: '#22c55e' },
  style:     { stroke: '#22c55e', strokeWidth: 2 },
}

// ── Drag: обновляем кэш И пропсы ──────────────────────────────────────────
function onNodeDragStop({ node }) {
  const x = Math.round(node.position.x)
  const y = Math.round(node.position.y)

  // Сохраняем в локальный кэш — это главное
  posCache.value[node.id] = { x, y }

  // Обновляем props чтобы позиция сохранялась при save
  const updated = props.nodes.map(n =>
    n.id === node.id ? { ...n, x, y } : n
  )
  emit('update:nodes', updated)
}

// ── Соединение нод ─────────────────────────────────────────────────────────
function onConnect(params) {
  const newEdge = {
    id:     `e${params.source}-${params.target}-${Date.now()}`,
    source: params.source,
    target: params.target,
    label:  '',
  }
  emit('update:edges', [...props.edges, newEdge])
}

// ── Редактирование данных ноды — позиции НЕ трогаем ───────────────────────
function onNodeDataUpdate(nodeId, newData) {
  const updated = props.nodes.map(n =>
    n.id === nodeId ? { ...n, data: { ...newData } } : n
  )
  emit('update:nodes', updated)
}

function onNodeDelete(nodeId) {
  delete posCache.value[nodeId]
  emit('update:nodes', props.nodes.filter(n => n.id !== nodeId))
  emit('update:edges', props.edges.filter(e => e.source !== nodeId && e.target !== nodeId))
}
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

.canvas-wrap {
  flex: 1;
  height: 100%;
  position: relative;
}
.vue-flow-canvas {
  width: 100%;
  height: 100%;
  background: var(--text);
}

:deep(.flow-handle) {
  width: 12px !important;
  height: 12px !important;
  background: var(--green-dark) !important;
  border: 2px solid var(--green-light) !important;
  border-radius: 50% !important;
}
:deep(.flow-handle-top) { top: -6px !important; }
:deep(.flow-handle-bot) { bottom: -6px !important; }

:deep(.vue-flow__edge-path) { stroke: var(--green-dark) !important; }

/* Скрываем панели */
:deep(.vue-flow__minimap)  { display: none !important; }
:deep(.vue-flow__controls) { display: none !important; }
</style>