<template>
  <div class="toolbar">
    <div class="toolbar-title">Блоки</div>
    <div class="toolbar-list">
      <button
        v-for="t in nodeTypes"
        :key="t.type"
        class="tool-btn"
        :title="t.label"
        @click="$emit('add', t.type)"
      >
        <span class="tool-icon">{{ t.icon }}</span>
        <span class="tool-label">{{ t.label }}</span>
      </button>
    </div>

    <div class="toolbar-divider" />

    <div class="toolbar-title">Настройки</div>
    <div class="trigger-box">
      <label>Триггер</label>
      <input
        :value="trigger"
        placeholder="/start"
        @input="$emit('update:trigger', $event.target.value)"
      />
      <div class="field-hint">Команда запуска сценария</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  trigger: { type: String, default: '' },
})
defineEmits(['add', 'update:trigger'])

const nodeTypes = [
  { type: 'message',   icon: '💬', label: 'Сообщение' },
  { type: 'buttons',   icon: '🔘', label: 'Кнопки' },
  { type: 'image',     icon: '🖼', label: 'Изображение' },
  { type: 'input',     icon: '⌨',  label: 'Ввод текста' },
  { type: 'delay',     icon: '⏱',  label: 'Задержка' },
  { type: 'condition', icon: '🔀',  label: 'Условие' },
  { type: 'goto',      icon: '↩',  label: 'Переход' },
  { type: 'end',       icon: '⏹',  label: 'Конец' },
]
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

.toolbar {
  width: 240px;
  min-width: 240px;
  background: linear-gradient(135deg, var(--green-dark) 10%, #3F9C30 100%);
  border-right: 1px solid var(--green-dark);
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
  user-select: none;
}

.toolbar-title {
  font-size: clamp(16px, 2vw, 20px);
  font-family: 'NauryzRedKeds';
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: .06em;
  color: var(--text-muted);
  margin-bottom: 2px;
}

.toolbar-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tool-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 8px;
  background: var(--green-light);
  border: 1px solid var(--text);
  color: var(--green-dark);
  font-size: 13px;
  cursor: pointer;
  transition: all .18s;
  text-align: left;
  width: 100%;
}
.tool-btn:hover {
  border-color: var(--green-light);
  background: var(--text);
}
.tool-icon  { font-size: 15px; flex-shrink: 0; }
.tool-label { font-size: clamp(12px, 2vw, 16px); font-weight: 500; }

.toolbar-divider {
  height: 1px;
  background: var(--text);
  margin: 6px 0;
}

.trigger-box { display: flex; flex-direction: column; gap: 4px; }
.trigger-box label { font-size: clamp(12px, 2vw, 16px); color: var(--text); }
.trigger-box input {
  font-size: 13px;
  padding: 7px 10px;
  background: var(--text);
  border: 1px solid var(--green-dark);
  color: var(--green-dark);
  border-radius: 6px;
}
.trigger-box input:focus { border-color: var(--green-light); outline: none; }
.field-hint { font-size: 13px; color: var(--text); }
</style>
