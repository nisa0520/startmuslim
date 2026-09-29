import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './theme.js' // set data-theme di <html> sebelum halaman dirender, biar tidak "kedip"
import './style.css'

createApp(App).use(router).mount('#app')
