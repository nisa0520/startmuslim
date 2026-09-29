<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'
import { auth } from '../auth'
import { t } from '../i18n'
import NavBar from '../components/NavBar.vue'

const router = useRouter()
const notes = ref([])
const text = ref('')
const err = ref('')

onMounted(async () => { try { notes.value = await api('/notes') } catch (e) { err.value = e.message } })

async function add() {
  if (!text.value.trim()) return
  err.value = ''
  try { notes.value.unshift(await api('/notes', { method: 'POST', body: { text: text.value } })); text.value = '' }
  catch (e) { err.value = e.message }
}
async function del(n) {
  await api('/notes/' + n.id, { method: 'DELETE' })
  notes.value = notes.value.filter((x) => x.id !== n.id)
}
async function logout() {
  await api('/auth/logout', { method: 'POST' })
  auth.user = null
  router.push('/')
}
</script>

<template>
  <NavBar />
  <main class="wrap dash">
    <div class="dash-head">
      <h2>Assalamu'alaikum, {{ auth.user.nickname || auth.user.name }}</h2>
      <button class="btn sm ghost" @click="logout">{{ t('keluar') }}</button>
    </div>
    <p class="role-badge"><span class="pill">{{ t(auth.user.role) }}</span></p>
    <p v-if="auth.user.status === 'pending'" class="note">{{ t('kontributor_note') }}</p>
    <p>Catat apa yang Anda pelajari hari ini. Catatan tersimpan di akun Anda.</p>
    <form class="addnote" @submit.prevent="add">
      <input v-model="text" maxlength="1000" placeholder="Hari ini saya belajar…" aria-label="Catatan belajar" />
      <button class="btn">Simpan catatan</button>
    </form>
    <p v-if="err" class="msg error" role="alert">{{ err }}</p>
    <ul class="notes">
      <li v-for="n in notes" :key="n.id"><span>{{ n.text }}</span><button class="del" @click="del(n)">Hapus</button></li>
    </ul>
    <p v-if="!notes.length" class="note">Belum ada catatan. Tulis hal pertama yang Anda pelajari hari ini.</p>
  </main>
</template>
