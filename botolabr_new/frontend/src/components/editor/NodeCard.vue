<template>
  <div class="node-card" :class="[`node-${data.type}`, { selected: selected }]" @click.stop>
    <!-- Header -->
    <div class="node-header">
      <span class="node-icon">{{ nodeIcon }}</span>
      <span class="node-title">{{ nodeLabel }}</span>
      <button class="node-del" @click.stop="$emit('delete', id)">✕</button>
    </div>

    <!-- Body -->
    <div class="node-body">
      <!-- message -->
      <template v-if="data.type === 'message'">
        <textarea
          :value="data.text"
          placeholder="Текст сообщения..."
          rows="3"
          class="node-textarea"
          @input="update('text', $event.target.value)"
        />
      </template>

      <!-- buttons -->
      <template v-else-if="data.type === 'buttons'">
        <textarea
          :value="data.text"
          placeholder="Текст над кнопками..."
          rows="2"
          class="node-textarea"
          @input="update('text', $event.target.value)"
        />
        <div class="buttons-list">
          <div v-for="(btn, i) in data.buttons || []" :key="i" class="btn-row">
            <input
              :value="btn.text"
              placeholder="Текст кнопки"
              class="node-input"
              @input="updateBtn(i, 'text', $event.target.value)"
            />
            <input
              :value="btn.next"
              placeholder="ID блока"
              class="node-input node-input-sm"
              @input="updateBtn(i, 'next', $event.target.value)"
            />
            <button class="btn-remove" @click="removeBtn(i)">✕</button>
          </div>
        </div>
        <button class="add-btn-btn" @click="addBtn">+ Добавить кнопку</button>
      </template>

      <!-- image -->
      <template v-else-if="data.type === 'image'">
        <input
          :value="data.url"
          placeholder="URL изображения"
          class="node-input"
          @input="update('url', $event.target.value)"
        />
        <input
          :value="data.caption"
          placeholder="Подпись (необязательно)"
          class="node-input"
          style="margin-top:6px"
          @input="update('caption', $event.target.value)"
        />
      </template>

      <!-- delay -->
      <template v-else-if="data.type === 'delay'">
        <div class="delay-row">
          <input
            :value="data.seconds || 2"
            type="number" min="1" max="10"
            class="node-input"
            style="width:70px"
            @input="update('seconds', +$event.target.value)"
          />
          <span class="delay-label">секунд</span>
        </div>
      </template>

      <!-- input -->
      <template v-else-if="data.type === 'input'">
        <input
          :value="data.text"
          placeholder="Вопрос пользователю..."
          class="node-input"
          @input="update('text', $event.target.value)"
        />
        <input
          :value="data.variable"
          placeholder="Имя переменной (напр. name)"
          class="node-input"
          style="margin-top:6px"
          @input="update('variable', $event.target.value)"
        />
      </template>

      <!-- condition -->
      <template v-else-if="data.type === 'condition'">
        <input
          :value="data.variable"
          placeholder="Переменная"
          class="node-input"
          @input="update('variable', $event.target.value)"
        />
        <div class="condition-row">
          <select
            :value="data.operator || '=='"
            class="node-select"
            @change="update('operator', $event.target.value)"
          >
            <option value="==">равно</option>
            <option value="!=">не равно</option>
            <option value="contains">содержит</option>
          </select>
          <input
            :value="data.value"
            placeholder="Значение"
            class="node-input"
            @input="update('value', $event.target.value)"
          />
        </div>
        <div class="condition-hint">
          <span class="cond-true">→ true</span>
          <span class="cond-false">→ false</span>
        </div>
      </template>

      <!-- goto -->
      <template v-else-if="data.type === 'goto'">
        <input
          :value="data.target"
          placeholder="ID целевого блока"
          class="node-input"
          @input="update('target', $event.target.value)"
        />
      </template>

      <!-- start / end -->
      <template v-else-if="data.type === 'start'">
        <div class="node-hint">Начало сценария</div>
      </template>
      <template v-else-if="data.type === 'end'">
        <div class="node-hint">Конец сценария</div>
      </template>
    </div>

    <!-- Node ID badge -->
    <div class="node-id">ID: {{ id }}</div>

    <!-- Handles rendered by parent via vue-flow slots -->
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  id:       { type: String, required: true },
  data:     { type: Object, required: true },
  selected: { type: Boolean, default: false },
})
const emit = defineEmits(['update', 'delete'])

const NODE_META = {
  start:     { icon: '▶', label: 'Старт' },
  end:       { icon: '⏹', label: 'Конец' },
  message:   { icon: '💬', label: 'Сообщение' },
  buttons:   { icon: '🔘', label: 'Кнопки' },
  image:     { icon: '🖼', label: 'Изображение' },
  delay:     { icon: '⏱', label: 'Задержка' },
  input:     { icon: '⌨', label: 'Ввод текста' },
  condition: { icon: '🔀', label: 'Условие' },
  goto:      { icon: '↩', label: 'Переход' },
}

const nodeIcon  = computed(() => NODE_META[props.data.type]?.icon  || '📦')
const nodeLabel = computed(() => NODE_META[props.data.type]?.label || props.data.type)

function update(key, val) {
  emit('update', props.id, { ...props.data, [key]: val })
}

function updateBtn(i, key, val) {
  const btns = [...(props.data.buttons || [])]
  btns[i] = { ...btns[i], [key]: val }
  emit('update', props.id, { ...props.data, buttons: btns })
}

function addBtn() {
  const btns = [...(props.data.buttons || []), { text: '', next: '' }]
  emit('update', props.id, { ...props.data, buttons: btns })
}

function removeBtn(i) {
  const btns = (props.data.buttons || []).filter((_, idx) => idx !== i)
  emit('update', props.id, { ...props.data, buttons: btns })
}
</script>

<style scoped>
.node-card {
  background: var(--green-light);
  border: 2px solid var(--green-light);
  border-radius: 10px;
  min-width: 200px;
  max-width: 250px;
  font-size: 13px;
  font-family: 'Roboto slab', serif;
  transition: border-color .18s;
  cursor: default;
}
.node-card.selected { border-color: var(--green-light); }

/* type colours */
.node-message   { border-top: 3px solid #3b82f6; }
.node-buttons   { border-top: 3px solid #a855f7; }
.node-image     { border-top: 3px solid #f59e0b; }
.node-delay     { border-top: 3px solid #6366f1; }
.node-input     { border-top: 3px solid #22c55e; }
.node-condition { border-top: 3px solid #ef4444; }
.node-goto      { border-top: 3px solid #ec4899; }
.node-start     { border-top: 3px solid #22c55e; }
.node-end       { border-top: 3px solid #94a3b8; }

.node-header {
  display: flex; align-items: center; gap: 7px;
  padding: 8px 10px 6px;
  background: var(--green-dark);
  border-bottom: 1px solid var(--green-light);
}
.node-icon  { font-size: 14px; }
.node-title { flex: 1; font-weight: 600; font-size: 14px; color: var(--text)}
.node-del {
  background: transparent;
  border: none;
  color: var(--green-light);
  font-size: 12px;
  padding: 2px 4px;
  cursor: pointer;
  border-radius: 4px;
  transition: color .15s;
}
.node-del:hover { color: var(--red); }

.node-body { padding: 10px; display: flex; flex-direction: column; gap: 6px; }

.node-textarea {
  width: 100%;
  background: var(--text);
  border: 1px solid var(--green-dark);
  color: var(--green-dark);
  border-radius: 6px;
  padding: 7px 9px;
  font-size: 12px;
  font-family: 'Roboto slab', serif;
  resize: vertical;
  transition: border-color .18s;
}
.node-textarea:focus { border-color: var(--green-light); outline: none; }

.node-input {
  width: 100%;
  background: var(--text);
  border: 1px solid var(--green-dark);
  color: var(--green-dark);
  border-radius: 6px;
  padding: 6px 9px;
  font-size: 12px;
  font-family: 'Roboto slab', serif;
  transition: border-color .18s;
}
.node-input:focus { border-color: var(--green-light); outline: none; }
.node-input-sm { width: 80px !important; min-width: 80px; }

.node-select {
  background: var(--text);
  border: 1px solid var(--green-dark);
  color: var(--green-dark);
  border-radius: 6px;
  padding: 6px 9px;
  font-size: 12px;
  font-family: 'Roboto slab', serif;
}

input::placeholder, textarea::placeholder { color: var(--green-dark); }

/* Buttons editor */
.buttons-list { display: flex; flex-direction: column; gap: 5px; }
.btn-row { display: flex; gap: 5px; align-items: center; }
.btn-remove {
  background: transparent;
  border: none;
  color: var(--green-dark);
  cursor: pointer;
  font-size: 12px;
  flex-shrink: 0;
  padding: 4px;
}
.btn-remove:hover { color: var(--red); }
.add-btn-btn {
  background: var(--green-dark);
  border: 1px dashed var(--text);
  color: var(--text);
  border-radius: 6px;
  padding: 5px;
  font-size: 12px;
  cursor: pointer;
  width: 100%;
  transition: border-color .18s;
}
.add-btn-btn:hover { border-color: var(--green-light); color: var(--text); }

/* Delay */
.delay-row { display: flex; align-items: center; gap: 8px; }
.delay-label { color: var(--text); font-size: 13px; }

/* Condition */
.condition-row { display: flex; gap: 6px; }
.condition-hint { display: flex; gap: 12px; font-size: 11px; margin-top: 2px; }
.cond-true  { color: var(--green-dark); }
.cond-false { color: var(--green-dark); }

/* Hint / ID */
.node-hint { color: var(--green-dark); font-size: 12px; text-align: center; padding: 4px 0; }
.node-id   { font-size: 10px; color: var(--green-dark); text-align: right; padding: 2px 8px 4px; }
</style>
