import { defineStore } from 'pinia'
import { AuthAPI, ProfileAPI } from '../api/index'
 
function safeParseUser() {
  try {
    const raw = localStorage.getItem('user')
    if (!raw || raw === 'undefined' || raw === 'null') return null
    return JSON.parse(raw)
  } catch {
    localStorage.removeItem('user')
    return null
  }
}
 
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user:  safeParseUser(),
    token: localStorage.getItem('token') || null,
  }),
 
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
 
  actions: {
    async login(credentials) {
      const res = await AuthAPI.login(credentials)
      this.token = res.data.token
      this.user  = res.data.user
      localStorage.setItem('token', this.token)
      localStorage.setItem('user',  JSON.stringify(this.user))
      return res.data
    },
 
    async register(data) {
      const res = await AuthAPI.register(data)
      this.token = res.data.token
      this.user  = res.data.user
      localStorage.setItem('token', this.token)
      localStorage.setItem('user',  JSON.stringify(this.user))
      return res.data
    },
 
    async logout() {
      try { await AuthAPI.logout() } catch {}
      this.token = null
      this.user  = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
 
    async fetchMe() {
      const res = await ProfileAPI.getMe()
      this.user = res.data
      localStorage.setItem('user', JSON.stringify(this.user))
      return res.data
    },
  },
})