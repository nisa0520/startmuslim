import { reactive, watchEffect } from 'vue'

const KEY = 'startmuslim-theme'
const mql = window.matchMedia('(prefers-color-scheme: dark)')

export const theme = reactive({
  mode: localStorage.getItem(KEY) || 'system', // 'light' | 'dark' | 'system'
})

function apply() {
  const effective = theme.mode === 'system' ? (mql.matches ? 'dark' : 'light') : theme.mode
  document.documentElement.setAttribute('data-theme', effective)
}

watchEffect(() => {
  localStorage.setItem(KEY, theme.mode)
  apply()
})
mql.addEventListener('change', () => { if (theme.mode === 'system') apply() })

export function cycleTheme() {
  theme.mode = { light: 'dark', dark: 'system', system: 'light' }[theme.mode]
}