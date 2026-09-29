<script setup>
import { computed, nextTick, onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Eye, EyeOff, GraduationCap, Users } from 'lucide-vue-next'
import { api } from '../api'
import { auth } from '../auth'
import { lang, setLang, t } from '../i18n'
import logo from '../assets/logo.png'
import mosque from '../assets/mosque.jpg'

const props = defineProps({ mode: String })
const router = useRouter()
const isReg = computed(() => props.mode === 'register')

// login | role | siswa | kontributor
const step = ref(isReg.value ? 'role' : 'login')

const f = reactive({
  name: '',
  nickname: '',
  country: '',
  city: '',
  phone: '',
  birthdate: '',
  email: '',
  password: '',
  digitalTrail: '',
  expertise: '',
})
const cvFile = ref(null)
const certFile = ref(null)
const err = ref('')
const busy = ref(false)
const showPass = ref(false)
const googleSignInEnabled = false
const googleButton = ref(null)
const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID || ''
let googleScriptPromise

const countries = [
  { code: 'ID', name: 'Indonesia', dial: '+62', cities: ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang', 'Makassar', 'Palembang', 'Depok', 'Tangerang', 'Bekasi', 'Yogyakarta', 'Malang', 'Bogor', 'Batam', 'Pekanbaru'] },
  { code: 'MY', name: 'Malaysia', dial: '+60', cities: ['Kuala Lumpur', 'Johor Bahru', 'Penang', 'Ipoh', 'Shah Alam', 'Malacca', 'Kota Kinabalu', 'Kuching'] },
  { code: 'SG', name: 'Singapore', dial: '+65', cities: ['Singapore'] },
  { code: 'BN', name: 'Brunei', dial: '+673', cities: ['Bandar Seri Begawan', 'Kuala Belait', 'Seria'] },
  { code: 'SA', name: 'Saudi Arabia', dial: '+966', cities: ['Riyadh', 'Jeddah', 'Mecca', 'Medina', 'Dammam'] },
  { code: 'AE', name: 'United Arab Emirates', dial: '+971', cities: ['Dubai', 'Abu Dhabi', 'Sharjah', 'Ajman'] },
  { code: 'EG', name: 'Egypt', dial: '+20', cities: ['Cairo', 'Alexandria', 'Giza', 'Luxor'] },
  { code: 'TR', name: 'Turkey', dial: '+90', cities: ['Istanbul', 'Ankara', 'Izmir', 'Bursa'] },
  { code: 'PK', name: 'Pakistan', dial: '+92', cities: ['Karachi', 'Lahore', 'Islamabad', 'Rawalpindi'] },
  { code: 'BD', name: 'Bangladesh', dial: '+880', cities: ['Dhaka', 'Chittagong', 'Khulna'] },
  { code: 'IN', name: 'India', dial: '+91', cities: ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai'] },
  { code: 'US', name: 'United States', dial: '+1', cities: ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Washington DC'] },
  { code: 'GB', name: 'United Kingdom', dial: '+44', cities: ['London', 'Manchester', 'Birmingham', 'Leeds'] },
  { code: 'AU', name: 'Australia', dial: '+61', cities: ['Sydney', 'Melbourne', 'Brisbane', 'Perth'] },
  { code: 'DZ', name: 'Algeria', dial: '+213', cities: ['Algiers', 'Oran', 'Constantine'] },
  { code: 'MA', name: 'Morocco', dial: '+212', cities: ['Casablanca', 'Rabat', 'Marrakech', 'Fes'] },
  { code: 'NG', name: 'Nigeria', dial: '+234', cities: ['Lagos', 'Abuja', 'Kano', 'Ibadan'] },
  { code: 'OTHER', name: 'Lainnya / Other', dial: '+', cities: [] },
]

const selectedCountry = computed(() => countries.find(c => c.code === f.country) || null)
const dialCode = computed(() => selectedCountry.value?.dial || '')
const cityOptions = computed(() => selectedCountry.value?.cities || [])

watch(() => f.country, () => { f.city = '' })

function loadGoogleIdentity() {
  if (window.google?.accounts?.id) return Promise.resolve()
  if (googleScriptPromise) return googleScriptPromise

  googleScriptPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true
    script.defer = true
    script.onload = resolve
    script.onerror = () => reject(new Error('Google Sign-In gagal dimuat. Periksa koneksi internet.'))
    document.head.appendChild(script)
  })
  return googleScriptPromise
}

async function completeGoogleSignIn(credential) {
  busy.value = true
  err.value = ''
  try {
    const result = await api('/auth/google', { method: 'POST', body: { credential } })
    auth.user = result.user
    router.push(result.is_new && result.user.role === 'siswa' ? '/student/quiz' : '/dashboard')
  } catch (e) {
    err.value = e.message
  } finally {
    busy.value = false
  }
}

async function renderGoogleButton() {
  if (!googleSignInEnabled) return
  if (!googleButton.value) return
  if (!googleClientId) return
  try {
    await loadGoogleIdentity()
    if (!googleButton.value) return
    window.google.accounts.id.initialize({
      client_id: googleClientId,
      callback: ({ credential }) => completeGoogleSignIn(credential),
    })
    googleButton.value.replaceChildren()
    window.google.accounts.id.renderButton(googleButton.value, {
      theme: 'outline',
      size: 'large',
      shape: 'pill',
      text: step.value === 'login' ? 'signin_with' : 'signup_with',
      width: Math.min(googleButton.value.clientWidth || 360, 400),
    })
  } catch (e) {
    err.value = e.message
  }
}

watch(step, async () => {
  await nextTick()
  renderGoogleButton()
})

onMounted(renderGoogleButton)

function pickRole(role) {
  step.value = role
  err.value = ''
}
function backToRole() {
  step.value = 'role'
  err.value = ''
}
function onCvChange(e) {
  cvFile.value = e.target.files?.[0] || null
}
function onCertChange(e) {
  certFile.value = e.target.files?.[0] || null
}
function openChat() {
  alert(t('chatbot_belum_tersedia'))
}

async function submit() {
  busy.value = true
  err.value = ''
  try {
    if (step.value === 'login') {
      auth.user = await api('/auth/login', {
        method: 'POST',
        body: { email: f.email, password: f.password },
      })
    } else {
      const body = {
        role: step.value,
        name: f.name,
        nickname: f.nickname,
        country: f.country,
        city: f.city,
        phone: `${dialCode.value}${f.phone}`.replace(/\s/g, ''),
        birthdate: f.birthdate,
        email: f.email,
        password: f.password,
      }
      if (step.value === 'kontributor') {
        body.digitalTrail = f.digitalTrail
        body.expertise = f.expertise
        if (cvFile.value) body.cvName = cvFile.value.name
        if (certFile.value) body.certName = certFile.value.name
      }
      auth.user = await api('/auth/register', { method: 'POST', body })
    }
    router.push(step.value === 'siswa' ? '/student/quiz' : '/dashboard')
  } catch (e) {
    err.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <aside class="auth-brand" :style="{ '--auth-mosque-image': `url(${mosque})` }">
      <div class="auth-brand-top">
        <RouterLink to="/" class="auth-logo">
          <img :src="logo" alt="StartMuslim" />
        </RouterLink>
        <div class="lang auth-lang" role="group" aria-label="Bahasa">
          <span class="lang-indicator" :class="lang.code" aria-hidden="true"></span>
          <button :class="{ on: lang.code === 'id' }" @click="setLang('id')">ID</button>
          <button :class="{ on: lang.code === 'en' }" @click="setLang('en')">EN</button>
        </div>
      </div>

      <div class="auth-brand-body">
        <h1 class="auth-title">{{ t('auth_title') }}</h1>
        <p class="auth-lead">{{ t('auth_lead') }}</p>
      </div>

    </aside>

    <main class="auth-form-wrap">
      <!-- LOGIN -->
      <template v-if="step === 'login'">
        <RouterLink to="/" class="auth-back">← {{ t('kembali') }}</RouterLink>
        <form class="auth-form" @submit.prevent="submit">
          <p class="auth-hint">{{ t('wajib') }}</p>
          <label class="auth-field">
            <span>{{ t('email') }} <em>*</em></span>
            <input v-model.trim="f.email" type="email" required autocomplete="email" :placeholder="t('email_ph')" />
          </label>
          <label class="auth-field">
            <span>{{ t('password') }} <em>*</em></span>
            <div class="pass-wrap">
              <input v-model="f.password" :type="showPass ? 'text' : 'password'" required minlength="8" autocomplete="current-password" :placeholder="t('password_ph')" />
              <button type="button" class="pass-toggle" @click="showPass = !showPass">
                <EyeOff v-if="showPass" :size="18" /><Eye v-else :size="18" />
              </button>
            </div>
          </label>
          <div class="auth-forgot"><RouterLink to="/lupa-kata-sandi">{{ t('lupa') }}</RouterLink></div>
          <button class="auth-submit" type="submit" :disabled="busy">
            {{ busy ? t('memproses') : t('masuk') + ' →' }}
          </button>
          <p v-if="err" class="msg error" role="alert">{{ err }}</p>
          <template v-if="googleSignInEnabled">
            <div class="auth-or"><span>{{ t('atau') }}</span></div>
            <div v-if="googleClientId" ref="googleButton" class="google-button-host"></div>
            <p v-else class="google-config-note">
              {{ lang.code === 'en' ? 'Set VITE_GOOGLE_CLIENT_ID to enable Google Sign-In.' : 'Atur VITE_GOOGLE_CLIENT_ID untuk mengaktifkan Google Sign-In.' }}
            </p>
          </template>
          <p class="auth-switch">
            {{ t('belum_akun') }}
            <RouterLink to="/daftar">{{ t('daftar_link') }}</RouterLink>
          </p>
        </form>
      </template>

      <!-- PILIH PERAN -->
      <template v-else-if="step === 'role'">
        <RouterLink to="/" class="auth-back">← {{ t('kembali') }}</RouterLink>
        <div class="auth-form">
          <h2 class="auth-form-title">{{ t('pilih_peran') }}</h2>
          <p class="auth-form-sub">{{ t('pilih_peran_sub') }}</p>
          <button type="button" class="role-card" @click="pickRole('siswa')">
            <span class="role-ic"><GraduationCap :size="22" /></span>
            <span class="role-text">
              <strong>{{ t('siswa') }}</strong>
              <small>{{ t('siswa_desc') }}</small>
            </span>
          </button>
          <button type="button" class="role-card" @click="pickRole('kontributor')">
            <span class="role-ic"><Users :size="22" /></span>
            <span class="role-text">
              <strong>{{ t('kontributor') }}</strong>
              <small>{{ t('kontributor_desc') }}</small>
            </span>
          </button>
          <p class="auth-switch">
            {{ t('sudah_akun') }}
            <RouterLink to="/masuk">{{ t('masuk') }}</RouterLink>
          </p>
        </div>
      </template>

      <!-- FORM SISWA / KONTRIBUTOR -->
      <template v-else>
        <button type="button" class="auth-back auth-back-btn" @click="backToRole">← {{ t('kembali_peran') }}</button>
        <form class="auth-form auth-form-wide" @submit.prevent="submit">
          <h2 class="auth-form-title">{{ step === 'siswa' ? t('siswa') : t('kontributor') }}</h2>
          <p class="auth-hint">{{ t('wajib') }}</p>
          <p v-if="step === 'kontributor'" class="auth-note">{{ t('kontributor_note') }}</p>

          <div class="auth-row">
            <label class="auth-field">
              <span>{{ t('nama') }} <em>*</em></span>
              <input v-model.trim="f.name" type="text" required autocomplete="name" />
            </label>
            <label class="auth-field">
              <span>{{ t('nama_panggil') }} <em>*</em></span>
              <input v-model.trim="f.nickname" type="text" required />
            </label>
          </div>

          <div class="auth-row">
            <label class="auth-field">
              <span>{{ t('negara') }} <em>*</em></span>
              <select v-model="f.country" required>
                <option value="" disabled>{{ t('pilih_negara') }}</option>
                <option v-for="c in countries" :key="c.code" :value="c.code">{{ c.name }}</option>
              </select>
            </label>
            <label class="auth-field">
              <span>{{ t('kota') }} <em>*</em></span>
              <select v-if="cityOptions.length" v-model="f.city" required :disabled="!f.country">
                <option value="" disabled>{{ !f.country ? t('pilih_negara_dulu') : t('pilih_kota') }}</option>
                <option v-for="city in cityOptions" :key="city" :value="city">{{ city }}</option>
              </select>
              <input v-else v-model.trim="f.city" type="text" required :disabled="!f.country" :placeholder="!f.country ? t('pilih_negara_dulu') : t('kota_ph')" />
            </label>
          </div>

          <div class="auth-row">
            <label class="auth-field">
              <span>{{ t('whatsapp') }} <em>*</em></span>
              <div class="phone-wrap">
                <span class="dial" :class="{ on: dialCode }">{{ dialCode || '+' }}</span>
                <input v-model.trim="f.phone" type="tel" required inputmode="numeric" pattern="[0-9]{6,15}" placeholder="81234567890" :disabled="!f.country" />
              </div>
            </label>
            <label class="auth-field">
              <span>{{ t('tgl_lahir') }} <em>*</em></span>
              <input v-model="f.birthdate" type="date" required max="2015-12-31" />
            </label>
          </div>

          <div class="auth-divider">{{ t('data_akun') }}</div>

          <label class="auth-field">
            <span>{{ t('email') }} <em>*</em></span>
            <input v-model.trim="f.email" type="email" required autocomplete="email" :placeholder="t('email_ph')" />
          </label>
          <label class="auth-field">
            <span>{{ t('password') }} <em>*</em></span>
            <div class="pass-wrap">
              <input v-model="f.password" :type="showPass ? 'text' : 'password'" required minlength="8" autocomplete="new-password" :placeholder="t('password_ph')" />
              <button type="button" class="pass-toggle" @click="showPass = !showPass">
                <EyeOff v-if="showPass" :size="18" /><Eye v-else :size="18" />
              </button>
            </div>
            <small class="field-hint">{{ t('password_hint') }}</small>
          </label>

          <template v-if="step === 'kontributor'">
            <div class="auth-divider">{{ t('info_kontributor') }}</div>
            <label class="auth-field">
              <span>{{ t('jejak') }} <small>({{ t('opsional') }})</small></span>
              <textarea v-model.trim="f.digitalTrail" rows="2" :placeholder="t('jejak_ph')"></textarea>
            </label>
            <label class="auth-field">
              <span>{{ t('keahlian') }}</span>
              <input v-model.trim="f.expertise" type="text" :placeholder="t('keahlian_ph')" />
            </label>
            <label class="auth-field">
              <span>{{ t('cv') }} <small>({{ t('opsional') }})</small></span>
              <input type="file" accept=".pdf,.doc,.docx,image/*" class="file-input" @change="onCvChange" />
            </label>
            <label class="auth-field">
              <span>{{ t('sertifikat') }} <em>*</em></span>
              <input type="file" accept=".pdf,.doc,.docx,image/*" required class="file-input" @change="onCertChange" />
            </label>
          </template>

          <button class="auth-submit" type="submit" :disabled="busy">
            {{ busy ? t('memproses') : (step === 'siswa' ? t('daftar') + ' →' : t('daftar_kontributor') + ' →') }}
          </button>
          <p v-if="err" class="msg error" role="alert">{{ err }}</p>

          <template v-if="step === 'siswa' && googleSignInEnabled">
            <div class="auth-or"><span>{{ t('atau') }}</span></div>
            <div v-if="googleClientId" ref="googleButton" class="google-button-host"></div>
            <p v-else class="google-config-note">
              {{ lang.code === 'en' ? 'Set VITE_GOOGLE_CLIENT_ID to enable Google Sign-In.' : 'Atur VITE_GOOGLE_CLIENT_ID untuk mengaktifkan Google Sign-In.' }}
            </p>
          </template>
        </form>
      </template>
    </main>

    <div class="float-actions">
      <button
        type="button"
        class="float-btn float-chat"
        :aria-label="t('buka_chatbot')"
        :title="t('chatbot')"
        @click="openChat"
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M4 6a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H9l-4 3v-3a3 3 0 0 1-1-2.2V6z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" />
          <circle cx="9" cy="10" r="1" fill="currentColor" />
          <circle cx="12" cy="10" r="1" fill="currentColor" />
          <circle cx="15" cy="10" r="1" fill="currentColor" />
        </svg>
      </button>
      <a
        class="float-btn float-wa"
        href="https://wa.me/6281234567890"
        target="_blank"
        rel="noopener"
        :aria-label="t('hubungi_whatsapp')"
        title="WhatsApp"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M17.47 14.38c-.3-.15-1.77-.87-2.04-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.95 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.8-1.49-1.78-1.66-2.08-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.87 1.22 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.63.71.23 1.36.2 1.87.12.57-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35z" />
          <path d="M12.04 2C6.5 2 2.02 6.48 2.02 12.02c0 1.77.46 3.45 1.28 4.92L2 22l5.2-1.36A9.96 9.96 0 0 0 12.04 22C17.58 22 22 17.52 22 11.98 22 6.48 17.58 2 12.04 2zm0 18.15c-1.58 0-3.05-.45-4.3-1.23l-.31-.18-3.09.81.83-3.01-.2-.33a8.1 8.1 0 0 1-1.25-4.34c0-4.5 3.66-8.15 8.17-8.15 4.5 0 8.15 3.65 8.15 8.15 0 4.51-3.65 8.15-8.15 8.15z" />
        </svg>
      </a>
    </div>
  </div>
</template>