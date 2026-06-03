<template>
  <AppLayout>
    <div class="settings-page">

      <!-- Header -->
      <div class="page-header">
        <h1 class="page-title">Настройки аккаунта</h1>
        <p class="page-sub">Управляйте профилем и безопасностью</p>
      </div>

      <div class="settings-grid">

        <!-- ── Аватар ────────────────────────────────────────── -->
        <section class="card avatar-card">
          <div class="card-title">Фото профиля</div>

          <div class="avatar-center">
            <div class="avatar-wrap" @click="triggerFileInput" :class="{ dragging: isDragging }"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="onDrop">
              <img v-if="previewUrl" :src="previewUrl" class="avatar-img" alt="avatar" />
              <span v-else class="avatar-initials">{{ initials }}</span>
              <div class="avatar-overlay">
                <span class="overlay-icon">📷</span>
                <span class="overlay-text">Изменить</span>
              </div>
            </div>
            <input ref="fileInput" type="file" accept="image/*" class="hidden-input" @change="onFileChange" />
          </div>

          <p class="avatar-hint">JPG, PNG или GIF · до 2 МБ<br>Нажмите или перетащите файл</p>

          <div v-if="avatarFile" class="avatar-actions">
            <button class="btn btn-ghost btn-sm" @click="cancelAvatar">Отмена</button>
            <button class="btn btn-primary btn-sm" :disabled="avatarLoading" @click="saveAvatar">
              <span v-if="avatarLoading" class="spinner"></span>
              {{ avatarLoading ? 'Сохранение...' : 'Сохранить фото' }}
            </button>
          </div>

          <div v-if="avatarSuccess" class="feedback success">✅ Фото обновлено</div>
          <div v-if="avatarError" class="feedback error">{{ avatarError }}</div>
        </section>

        <!-- ── Профиль ───────────────────────────────────────── -->
        <section class="card profile-card">
          <div class="card-title">Основная информация</div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Имя</label>
              <input v-model="profileForm.name" class="form-input" placeholder="Ваше имя" />
            </div>
            <div class="form-group">
              <label class="form-label">Фамилия</label>
              <input v-model="profileForm.lastname" class="form-input" placeholder="Фамилия" />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Имя пользователя</label>
            <div class="input-with-prefix">
              <span class="prefix">@</span>
              <input v-model="profileForm.username" class="form-input prefix-input" placeholder="username" />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Email</label>
            <input v-model="profileForm.email" type="email" class="form-input" placeholder="email@example.com" />
          </div>

          <div class="form-actions">
            <button class="btn btn-primary" :disabled="profileLoading" @click="saveProfile">
              <span v-if="profileLoading" class="spinner"></span>
              {{ profileLoading ? 'Сохранение...' : 'Сохранить изменения' }}
            </button>
          </div>

          <div v-if="profileSuccess" class="feedback success">Профиль обновлён</div>
          <div v-if="profileError" class="feedback error">{{ profileError }}</div>
        </section>

        <!-- ── Пароль ────────────────────────────────────────── -->
        <section class="card password-card">
          <div class="card-title">Безопасность</div>
          <p class="card-sub">Для смены пароля введите текущий и новый пароль</p>

          <div class="form-group">
            <label class="form-label">Текущий пароль</label>
            <div class="input-password">
              <input
                v-model="pwForm.current"
                :type="showPw.current ? 'text' : 'password'"
                class="form-input"
                placeholder="••••••••"
                autocomplete="current-password"
              />
              <button class="pw-toggle" @click="showPw.current = !showPw.current" type="button">
                {{ showPw.current ? '🙈' : '👁️' }}
              </button>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Новый пароль</label>
            <div class="input-password">
              <input
                v-model="pwForm.new"
                :type="showPw.new ? 'text' : 'password'"
                class="form-input"
                placeholder="Минимум 6 символов"
                autocomplete="new-password"
              />
              <button class="pw-toggle" @click="showPw.new = !showPw.new" type="button">
                {{ showPw.new ? '🙈' : '👁️' }}
              </button>
            </div>
            <div v-if="pwForm.new" class="pw-strength">
              <div class="strength-bar">
                <div class="strength-fill" :class="pwStrength.cls" :style="{ width: pwStrength.pct + '%' }"></div>
              </div>
              <span class="strength-label" :class="pwStrength.cls">{{ pwStrength.label }}</span>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Повторите новый пароль</label>
            <div class="input-password">
              <input
                v-model="pwForm.confirm"
                :type="showPw.confirm ? 'text' : 'password'"
                class="form-input"
                :class="{ mismatch: pwForm.confirm && pwForm.new !== pwForm.confirm }"
                placeholder="Повторите пароль"
                autocomplete="new-password"
              />
              <button class="pw-toggle" @click="showPw.confirm = !showPw.confirm" type="button">
                {{ showPw.confirm ? '🙈' : '👁️' }}
              </button>
            </div>
            <span v-if="pwForm.confirm && pwForm.new !== pwForm.confirm" class="mismatch-hint">
              Пароли не совпадают
            </span>
          </div>

          <div class="form-actions">
            <button
              class="btn btn-primary"
              :disabled="pwLoading || !canChangePw"
              @click="changePassword"
            >
              <span v-if="pwLoading" class="spinner"></span>
              {{ pwLoading ? 'Сохранение...' : 'Изменить пароль' }}
            </button>
          </div>

          <div v-if="pwSuccess" class="feedback success">Пароль изменён</div>
          <div v-if="pwError" class="feedback error">{{ pwError }}</div>
        </section>

      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { useAuthStore } from '../stores/auth'
import { ProfileAPI } from '../api/index'

const auth = useAuthStore()

// ── Avatar ──────────────────────────────────────────────────────────────────
const fileInput   = ref(null)
const previewUrl  = ref(auth.user?.avatar || null)
const avatarFile  = ref(null)
const avatarLoading = ref(false)
const avatarSuccess = ref(false)
const avatarError   = ref('')
const isDragging    = ref(false)

const initials = computed(() => {
  const n = auth.user?.name || auth.user?.username || '?'
  return n.slice(0, 2).toUpperCase()
})

function triggerFileInput() {
  fileInput.value?.click()
}

function onFileChange(e) {
  const file = e.target.files[0]
  if (file) setAvatarFile(file)
}

function onDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) setAvatarFile(file)
}

function setAvatarFile(file) {
  if (file.size > 2 * 1024 * 1024) {
    avatarError.value = 'Файл слишком большой (макс. 2 МБ)'
    return
  }
  avatarFile.value = file
  avatarError.value = ''
  const reader = new FileReader()
  reader.onload = e => { previewUrl.value = e.target.result }
  reader.readAsDataURL(file)
}

function cancelAvatar() {
  avatarFile.value = null
  previewUrl.value = auth.user?.avatar || null
  avatarError.value = ''
  if (fileInput.value) fileInput.value.value = ''
}

async function saveAvatar() {
  if (!avatarFile.value) return
  avatarLoading.value = true
  avatarSuccess.value = false
  avatarError.value   = ''
  try {
    const reader = new FileReader()
    const base64 = await new Promise((res, rej) => {
      reader.onload  = e => res(e.target.result)
      reader.onerror = rej
      reader.readAsDataURL(avatarFile.value)
    })
    await ProfileAPI.uploadAvatar({ avatar: base64 })
    await auth.fetchMe()
    previewUrl.value  = auth.user?.avatar || base64
    avatarFile.value  = null
    avatarSuccess.value = true
    setTimeout(() => { avatarSuccess.value = false }, 3000)
  } catch (e) {
    avatarError.value = e.response?.data?.detail || 'Ошибка загрузки фото'
  }
  avatarLoading.value = false
}

// ── Profile ─────────────────────────────────────────────────────────────────
const profileForm = ref({
  name:     '',
  lastname: '',
  username: '',
  email:    '',
})
const profileLoading = ref(false)
const profileSuccess = ref(false)
const profileError   = ref('')

onMounted(async () => {
  try {
    await auth.fetchMe()
  } catch {}
  const u = auth.user
  profileForm.value = {
    name:     u?.name     || '',
    lastname: u?.lastname || '',
    username: u?.username || '',
    email:    u?.email    || '',
  }
})

async function saveProfile() {
  profileLoading.value = true
  profileSuccess.value = false
  profileError.value   = ''
  try {
    await ProfileAPI.update({
      name:     profileForm.value.name     || null,
      lastname: profileForm.value.lastname || null,
      username: profileForm.value.username || null,
      email:    profileForm.value.email    || null,
    })
    await auth.fetchMe()
    profileSuccess.value = true
    setTimeout(() => { profileSuccess.value = false }, 3000)
  } catch (e) {
    profileError.value = e.response?.data?.detail || 'Ошибка обновления профиля'
  }
  profileLoading.value = false
}

// ── Password ─────────────────────────────────────────────────────────────────
const pwForm = ref({ current: '', new: '', confirm: '' })
const showPw = ref({ current: false, new: false, confirm: false })
const pwLoading = ref(false)
const pwSuccess = ref(false)
const pwError   = ref('')

const canChangePw = computed(() =>
  pwForm.value.current &&
  pwForm.value.new.length >= 6 &&
  pwForm.value.new === pwForm.value.confirm
)

const pwStrength = computed(() => {
  const p = pwForm.value.new
  if (!p) return { pct: 0, cls: '', label: '' }
  let score = 0
  if (p.length >= 8) score++
  if (p.length >= 12) score++
  if (/[A-Z]/.test(p)) score++
  if (/[0-9]/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p)) score++
  if (score <= 1) return { pct: 20,  cls: 'weak',   label: 'Слабый' }
  if (score <= 2) return { pct: 45,  cls: 'fair',   label: 'Средний' }
  if (score <= 3) return { pct: 70,  cls: 'good',   label: 'Хороший' }
  return              { pct: 100, cls: 'strong', label: 'Надёжный' }
})

async function changePassword() {
  if (!canChangePw.value) return
  pwLoading.value = true
  pwSuccess.value = false
  pwError.value   = ''
  try {
    await ProfileAPI.changePassword({
      current_password: pwForm.value.current,
      new_password:     pwForm.value.new,
    })
    pwForm.value = { current: '', new: '', confirm: '' }
    pwSuccess.value = true
    setTimeout(() => { pwSuccess.value = false }, 3000)
  } catch (e) {
    pwError.value = e.response?.data?.detail || 'Ошибка смены пароля'
  }
  pwLoading.value = false
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
.settings-page {
  padding: 32px 36px;
  max-width: 960px;
}

/* ── Header ─────────────────────────────────────────────────────────────── */
.page-header {
  margin-bottom: 32px;
}
.page-title {
  font-size: clamp(18px, 6vw, 40px);
  font-family: 'Lobelia', serif;
  font-weight: 400;
  margin-bottom: 4px;
  color: var(--green-dark);
}
.page-sub {
  color: var(--green-light);
  font-size: clamp(16px, 2vw, 20px);
  font-family: 'NauryzRedKeds', serif;
}

/* ── Grid ───────────────────────────────────────────────────────────────── */
.settings-grid {
  display: grid;
  grid-template-columns: 280px 1fr;
  grid-template-rows: auto auto;
  gap: 20px;
}
.avatar-card   { grid-column: 1; grid-row: 1 / 3; }
.profile-card  { grid-column: 2; grid-row: 1; }
.password-card { grid-column: 2; grid-row: 2; }

@media (max-width: 760px) {
  .settings-page { padding: 20px 16px; }
  .settings-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
  }
  .avatar-card, .profile-card, .password-card {
    grid-column: 1;
    grid-row: auto;
  }
}

/* ── Card ───────────────────────────────────────────────────────────────── */
.card {
  background: linear-gradient(135deg, var(--green-light) 10%, var(--text) 100%);;
  border: 1px solid var(--green-dark);
  border-radius: 16px;
  padding: 24px;
}
.card-title {
  font-size: clamp(14px, 2vw, 18px);
  font-weight: 500;
  color: var(--green-dark);
  font-family: 'NauryzRedKeds', serif;
  margin-bottom: 4px;
}
.card-sub {
  font-size: clamp(12px, 2vw, 16px);
  font-family: 'Roboto slab', serif;
  color: var(--green-dark);
  margin: 0 0 20px;
}

/* ── Avatar card ────────────────────────────────────────────────────────── */
.avatar-center {
  display: flex;
  justify-content: center;
  margin: 20px 0 12px;
}
.avatar-wrap {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  cursor: pointer;
  overflow: hidden;
  border: 3px solid var(--green-dark);
  transition: border-color .2s, transform .15s;
  flex-shrink: 0;
}
.avatar-wrap:hover,
.avatar-wrap.dragging {
  border-color: var(--text);
  transform: scale(1.03);
}
.avatar-wrap.dragging { box-shadow: 0 0 0 4px rgba(173, 243, 108, .25); }

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.avatar-initials {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  font-weight: 700;
  color: var(--green-dark);
  background: var(--green-light);
}
.avatar-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,.55);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  opacity: 0;
  transition: opacity .18s;
}
.avatar-wrap:hover .avatar-overlay { opacity: 1; }
.overlay-icon { font-size: 22px; }
.overlay-text { font-size: 12px; color: var(--text); font-weight: 600; }

.hidden-input { display: none; }

.avatar-hint {
  font-size: clamp(12px, 2vw, 16px);
  font-family: 'Roboto slab', serif;
  color: var(--green-dark);
  text-align: center;
  line-height: 1.6;
  margin: 0 0 16px;
}
.avatar-actions {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 4px;
}

/* ── Form ───────────────────────────────────────────────────────────────── */
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.form-group {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.form-label {
  font-size: clamp(12px, 2vw, 14px);
  font-family: 'Roboto slab', serif;
  font-weight: 600;
  color: var(--green-dark);
}
.form-input {
  width: 100%;
  padding: 10px 14px;
  background: linear-gradient(135deg, var(--green-dark) 10%, #3F9C30 100%);
  border: 1px solid var(--green-dark);
  border-radius: 10px;
  color: var(--text);
  font-size: 14px;
  outline: none;
  transition: border-color .18s, box-shadow .18s;
  box-sizing: border-box;
}
.form-input:focus {
  border-color: var(--green-light);
  box-shadow: 0 0 0 3px rgba(173, 243, 108, .15);
}
.form-input.mismatch {
  border-color: #f87171;
  box-shadow: 0 0 0 3px rgba(248,113,113,.15);
}

.input-with-prefix {
  display: flex;
  align-items: center;
  background: var(--green-light);
  border: 1px solid var(--green-dark);
  border-radius: 10px;
  overflow: hidden;
  transition: border-color .18s, box-shadow .18s;
}
.input-with-prefix:focus-within {
  border-color: var(--green-dark);
  box-shadow: 0 0 0 3px rgba(173, 243, 108, .15);
}
.prefix {
  padding: 10px 0 10px 14px;
  color: var(--green-dark);
  font-size: 14px;
  font-weight: 600;
  user-select: none;
}
.prefix-input {
  border: none !important;
  box-shadow: none !important;
  border-radius: 0 !important;
  flex: 1;
  padding-left: 4px;
}

.input-password {
  position: relative;
}
.input-password .form-input {
  padding-right: 44px;
}
.pw-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 2px;
  opacity: .7;
  transition: opacity .15s;
}
.pw-toggle:hover { opacity: 1; }

input::placeholder, textarea::placeholder { color: var(--text); }

/* Password strength */
.pw-strength {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 6px;
}
.strength-bar {
  flex: 1;
  height: 4px;
  background: var(--green-dark);
  border-radius: 4px;
  overflow: hidden;
}
.strength-fill {
  height: 100%;
  border-radius: 4px;
  transition: width .3s, background .3s;
}
.strength-fill.weak   { background: #f87171; }
.strength-fill.fair   { background: #fb923c; }
.strength-fill.good   { background: #facc15; }
.strength-fill.strong { background: #3F9C30; }
.strength-label {
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
}
.strength-label.weak   { color: #f87171; }
.strength-label.fair   { color: #fb923c; }
.strength-label.good   { color: #facc15; }
.strength-label.strong { color: #3F9C30; }

.mismatch-hint {
  font-size: 12px;
  color: #f87171;
  margin-top: 2px;
}

.form-actions {
  margin-top: 4px;
}

/* ── Feedback ───────────────────────────────────────────────────────────── */
.feedback {
  margin-top: 12px;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  animation: fadeIn .2s ease;
}
.feedback.success {
  background: rgba(173,243,108,.12);
  border: 1px solid rgba(173,243,108,.3);
  color: var(--green-dark);
}
.feedback.error {
  background: rgba(248,113,113,.1);
  border: 1px solid rgba(248,113,113,.3);
  color: #f87171;
}

/* ── Buttons ────────────────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all .18s;
}
.btn:disabled { opacity: .55; cursor: not-allowed; }
.btn-primary {
  background: var(--green-dark);
  color: var(--text);
}
.btn-primary:not(:disabled):hover {
  background: #c5f27a;
  transform: translateY(-1px);
}
.btn-ghost {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border);
}
.btn-ghost:hover { background: var(--green-light); color: var(--green-dark); }
.btn-sm { padding: 7px 14px; font-size: 13px; }

/* ── Spinner ────────────────────────────────────────────────────────────── */
.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin .7s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-4px); } }
</style>