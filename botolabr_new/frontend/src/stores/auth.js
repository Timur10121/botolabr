import { defineStore } from 'pinia'
import { AuthAPI, ProfileAPI } from '../api/index'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user:  JSON.parse(localStorage.getItem('user') || 'null'),
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
