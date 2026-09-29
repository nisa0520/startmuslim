<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { Eye, EyeOff } from 'lucide-vue-next'
import { api } from '../api'
import { lang, setLang } from '../i18n'
import logo from '../assets/logo.png'

defineProps({ mode: String })
const route = useRoute()
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const busy = ref(false)
const sent = ref(false)
const changed = ref(false)
const error = ref('')
const resetUrl = ref('')
const token = computed(() => typeof route.query.token === 'string' ? route.query.token : '')
const copy = computed(() => lang.code === 'en' ? {
  title: 'Reset your password',
  intro: 'Enter your account email and we’ll send instructions to reset your password.',
  email: 'Email address',
  request: 'Send reset link',
  sent: 'If that email is registered, reset instructions are on their way.',
  localLink: 'Local development reset link',
  newPassword: 'New password',
  confirm: 'Confirm new password',
  save: 'Change password',
  mismatch: 'The passwords do not match.',
  changed: 'Your password has been changed. You can now log in with it.',
  invalid: 'This reset link is missing or invalid. Request a new link to continue.',
  back: 'Back to log in',
  passwordHint: 'At least 8 characters.',
  showPassword: 'Show password',
  hidePassword: 'Hide password',
} : {
  title: 'Atur ulang kata sandi',
  intro: 'Masukkan email akunmu. Kami akan mengirim instruksi untuk mengatur ulang kata sandi.',
  email: 'Alamat email',
  request: 'Kirim tautan reset',
  sent: 'Jika email tersebut terdaftar, instruksi reset akan segera dikirim.',
  localLink: 'Tautan reset untuk pengembangan lokal',
  newPassword: 'Kata sandi baru',
  confirm: 'Konfirmasi kata sandi baru',
  save: 'Ubah kata sandi',
  mismatch: 'Kata sandi tidak cocok.',
  changed: 'Kata sandi berhasil diubah. Sekarang kamu bisa masuk dengan kata sandi baru.',
  invalid: 'Tautan reset tidak ada atau tidak valid. Minta tautan baru untuk melanjutkan.',
  back: 'Kembali ke halaman masuk',
  passwordHint: 'Minimal 8 karakter.',
  showPassword: 'Tampilkan kata sandi',
  hidePassword: 'Sembunyikan kata sandi',
})

async function submitRequest() {
  busy.value = true
  error.value = ''
  try {
    const result = await api('/auth/password-reset/request', { method: 'POST', body: { email: email.value } })
    resetUrl.value = result.reset_url || ''
    sent.value = true
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}

async function submitReset() {
  error.value = ''
  if (password.value !== confirmPassword.value) {
    error.value = copy.value.mismatch
    return
  }
  busy.value = true
  try {
    await api('/auth/password-reset/confirm', {
      method: 'POST',
      body: { token: token.value, password: password.value },
    })
    changed.value = true
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <aside class="auth-brand">
      <div class="auth-brand-top">
        <RouterLink to="/" class="auth-logo"><img :src="logo" alt="StartMuslim" /></RouterLink>
        <div class="lang auth-lang" role="group" aria-label="Bahasa">
          <span class="lang-indicator" :class="lang.code" aria-hidden="true"></span>
          <button :class="{ on: lang.code === 'id' }" @click="setLang('id')">ID</button>
          <button :class="{ on: lang.code === 'en' }" @click="setLang('en')">EN</button>
        </div>
      </div>
      <div class="auth-brand-body">
        <div class="auth-icon" aria-hidden="true">🔐</div>
        <h1 class="auth-title">{{ copy.title }}</h1>
        <p class="auth-lead">{{ copy.intro }}</p>
      </div>
    </aside>

    <main class="auth-form-wrap">
      <RouterLink to="/masuk" class="auth-back">← {{ copy.back }}</RouterLink>

      <form v-if="mode === 'request' && !sent" class="auth-form" @submit.prevent="submitRequest">
        <h2 class="auth-form-title">{{ copy.title }}</h2>
        <p class="auth-form-sub">{{ copy.intro }}</p>
        <label class="auth-field">
          <span>{{ copy.email }}</span>
          <input v-model.trim="email" type="email" required autocomplete="email" placeholder="nama@email.com" />
        </label>
        <button class="auth-submit" type="submit" :disabled="busy">{{ busy ? '…' : copy.request }}</button>
        <p v-if="error" class="msg error" role="alert">{{ error }}</p>
      </form>

      <section v-else-if="mode === 'request'" class="auth-form" aria-live="polite">
        <h2 class="auth-form-title">{{ copy.title }}</h2>
        <p class="msg ok">{{ copy.sent }}</p>
        <div v-if="resetUrl" class="reset-dev-link">
          <span>{{ copy.localLink }}</span>
          <a :href="resetUrl">{{ resetUrl }}</a>
        </div>
      </section>

      <form v-else-if="!changed && token" class="auth-form" @submit.prevent="submitReset">
        <h2 class="auth-form-title">{{ copy.title }}</h2>
        <label class="auth-field">
          <span>{{ copy.newPassword }}</span>
          <div class="pass-wrap">
            <input v-model="password" :type="showPassword ? 'text' : 'password'" required minlength="8" maxlength="128" autocomplete="new-password" :placeholder="copy.passwordHint" />
            <button type="button" class="pass-toggle" :aria-label="showPassword ? copy.hidePassword : copy.showPassword" :title="showPassword ? copy.hidePassword : copy.showPassword" @click="showPassword = !showPassword">
              <EyeOff v-if="showPassword" :size="18" /><Eye v-else :size="18" />
            </button>
          </div>
        </label>
        <label class="auth-field">
          <span>{{ copy.confirm }}</span>
          <div class="pass-wrap">
            <input v-model="confirmPassword" :type="showConfirmPassword ? 'text' : 'password'" required minlength="8" maxlength="128" autocomplete="new-password" :placeholder="copy.passwordHint" />
            <button type="button" class="pass-toggle" :aria-label="showConfirmPassword ? copy.hidePassword : copy.showPassword" :title="showConfirmPassword ? copy.hidePassword : copy.showPassword" @click="showConfirmPassword = !showConfirmPassword">
              <EyeOff v-if="showConfirmPassword" :size="18" /><Eye v-else :size="18" />
            </button>
          </div>
        </label>
        <button class="auth-submit" type="submit" :disabled="busy">{{ busy ? '…' : copy.save }}</button>
        <p v-if="error" class="msg error" role="alert">{{ error }}</p>
      </form>

      <section v-else class="auth-form" aria-live="polite">
        <h2 class="auth-form-title">{{ copy.title }}</h2>
        <p v-if="changed" class="msg ok">{{ copy.changed }}</p>
        <p v-else class="msg error">{{ copy.invalid }}</p>
      </section>

      <RouterLink class="reset-login-link" to="/masuk">{{ copy.back }}</RouterLink>
    </main>
  </div>
</template>

<style scoped>
.reset-dev-link { display: grid; gap: 0.45rem; padding: 0.8rem; border: 1px solid var(--border); border-radius: 10px; background: var(--surface-warm); overflow-wrap: anywhere; }
.reset-dev-link span { color: var(--ink-muted); font-size: 0.8rem; font-weight: 600; }
.reset-dev-link a { color: var(--green2); font-size: 0.85rem; }
.reset-login-link { margin-top: 1rem; color: var(--green2); font-size: 0.85rem; font-weight: 600; }
</style>