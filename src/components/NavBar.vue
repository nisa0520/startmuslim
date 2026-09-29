<script setup>
import { computed, ref } from 'vue'
import { Sun, Moon, Monitor, Menu, X } from 'lucide-vue-next'
import { auth } from '../auth'
import { theme, cycleTheme } from '../theme'
import { lang, setLang, t } from '../i18n'
import logo from '../assets/logo.png'

const menuItems = [
  { label: 'kelas', href: '#' },
  { label: 'jalur', href: '/#flow' },
  { label: 'kontributor', href: '#' },
  { label: 'testimoni', href: '/#testimoni' },
  { label: 'faq', href: '/#faq' },
  { label: 'tentang', href: '/#about' },
]

const themeIcon = computed(() => ({ light: Sun, dark: Moon, system: Monitor }[theme.mode]))
const themeLabel = computed(() => ({ light: 'Terang', dark: 'Gelap', system: 'Sistem' }[theme.mode]))

const mobileOpen = ref(false)
function closeMobile() {
  mobileOpen.value = false
}
</script>

<template>
  <header class="topbar">
    <RouterLink class="brand" to="/" @click="closeMobile">
      <img :src="logo" alt="StartMuslim" class="brand-logo" />
    </RouterLink>

    <nav class="menu" aria-label="Menu utama">
      <a v-for="m in menuItems" :key="m.label" :href="m.href">
        {{ t(m.label) }}
      </a>
    </nav>

    <div class="topbar-actions">
      <RouterLink v-if="!auth.user" class="link auth-btn" to="/masuk">
        {{ t('masuk') }}
      </RouterLink>
      <RouterLink v-if="!auth.user" class="btn sm gold auth-btn" to="/daftar">
        {{ t('daftar') }}
      </RouterLink>
      <RouterLink v-if="auth.user" class="btn sm gold auth-btn" to="/dashboard">
        {{ t('dashboard') }}
      </RouterLink>

      <div class="lang" role="group" aria-label="Bahasa">
        <span class="lang-indicator" :class="lang.code" aria-hidden="true"></span>
        <button :class="{ on: lang.code === 'id' }" @click="setLang('id')">ID</button>
        <button :class="{ on: lang.code === 'en' }" @click="setLang('en')">EN</button>
      </div>

      <button
        class="theme-toggle"
        @click="cycleTheme"
        :aria-label="'Tema: ' + themeLabel"
        :title="'Tema: ' + themeLabel"
      >
        <Transition name="spin" mode="out-in">
          <component :is="themeIcon" :key="theme.mode" :size="18" />
        </Transition>
      </button>

      <button
        class="hamburger"
        @click="mobileOpen = !mobileOpen"
        :aria-expanded="mobileOpen"
        aria-label="Buka menu"
      >
        <Transition name="spin" mode="out-in">
          <X v-if="mobileOpen" key="close" :size="20" />
          <Menu v-else key="open" :size="20" />
        </Transition>
      </button>
    </div>

    <Transition name="drop">
      <nav v-if="mobileOpen" class="mobile-menu" aria-label="Menu mobile">
        <a
          v-for="m in menuItems"
          :key="m.label"
          :href="m.href"
          @click="closeMobile"
        >
          {{ t(m.label) }}
        </a>

        <div class="mobile-auth">
          <RouterLink
            v-if="!auth.user"
            class="link"
            to="/masuk"
            @click="closeMobile"
          >
            {{ t('masuk') }}
          </RouterLink>
          <RouterLink
            v-if="!auth.user"
            class="btn sm gold"
            to="/daftar"
            @click="closeMobile"
          >
            {{ t('daftar') }}
          </RouterLink>
          <RouterLink
            v-if="auth.user"
            class="btn sm gold"
            to="/dashboard"
            @click="closeMobile"
          >
            {{ t('dashboard') }}
          </RouterLink>
        </div>
      </nav>
    </Transition>
  </header>
</template>