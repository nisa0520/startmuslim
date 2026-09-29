import { reactive } from 'vue'
import { api } from './api'

export const auth = reactive({ user: null, ready: false })

export async function loadUser() {
  try { auth.user = await api('/auth/me') } catch { auth.user = null }
  auth.ready = true
}
