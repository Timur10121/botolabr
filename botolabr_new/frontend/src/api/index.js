import api from './client'

// ── Auth ────────────────────────────────────────────────────────────────────
export const AuthAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login:    (data) => api.post('/api/auth/login',    data),
  logout:   ()     => api.post('/api/auth/logout'),
}

// ── Profile ─────────────────────────────────────────────────────────────────
export const ProfileAPI = {
  getMe:          ()     => api.get('/api/me'),
  update:         (data) => api.patch('/api/me', data),
  changePassword: (data) => api.post('/api/me/password', data),
  uploadAvatar:   (data) => api.post('/api/me/avatar-base64', data),
}

// ── Bots ────────────────────────────────────────────────────────────────────
export const BotsAPI = {
  getAll:      ()        => api.get('/api/bots'),
  check:       (token)   => api.post('/api/bots/check', { token }),
  connect:     (token)   => api.post('/api/bots', { token }),
  delete:      (id)      => api.delete(`/api/bots/${id}`),
  toggle:      (id)      => api.patch(`/api/bots/${id}/toggle`),
  setWebhook:  (id, url) => api.post(`/api/bots/${id}/set-webhook`,    { base_url: url }),
  delWebhook:  (id)      => api.delete(`/api/bots/${id}/set-webhook`),
  webhookInfo: (id)      => api.get(`/api/bots/${id}/webhook-info`),
}

// ── Scenarios ────────────────────────────────────────────────────────────────
export const ScenariosAPI = {
  getAll:  (botId)       => api.get('/api/scenarios', { params: { bot_id: botId } }),
  get:     (id)          => api.get(`/api/scenarios/${id}`),
  create:  (data)        => api.post('/api/scenarios', data),
  update:  (id, data)    => api.patch(`/api/scenarios/${id}`, data),
  delete:  (id)          => api.delete(`/api/scenarios/${id}`),
}
