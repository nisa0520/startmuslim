<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Bot, Check, ChevronLeft, ChevronRight, Sparkles } from 'lucide-vue-next'
import { auth } from '../auth'
import { lang, setLang } from '../i18n'
import logo from '../assets/logo.png'

const router = useRouter()
const index = ref(0)
const answers = ref([null, null, null, [], null])
const showingResult = ref(false)
const storageKey = `startmuslim-student-quiz:${auth.user.id}`

try {
  const saved = JSON.parse(localStorage.getItem(storageKey) || 'null')
  if (saved && Array.isArray(saved.answers) && saved.answers.length === 5) {
    answers.value = saved.answers
    index.value = Math.min(Math.max(saved.index || 0, 0), 4)
  }
} catch {
  localStorage.removeItem(storageKey)
}

watch([index, answers], () => {
  localStorage.setItem(storageKey, JSON.stringify({ index: index.value, answers: answers.value }))
}, { deep: true })

const copy = computed(() => lang.code === 'en' ? {
  title: 'Learning Placement Quiz',
  question: 'QUESTION',
  of: 'of',
  back: 'Back',
  next: 'Continue',
  result: 'See results',
  skip: 'Want to skip the quiz?',
  skipLink: 'Go to my classes',
  chooseMany: 'You can choose more than one.',
  selectOne: 'Choose one answer to continue.',
  resultTitle: 'Your learning starting point',
  resultIntro: 'Based on your answers, this is a useful place to begin.',
  foundation: 'Build your foundations',
  foundationText: 'Start with the essentials and take each topic at a comfortable pace.',
  growing: 'Keep growing steadily',
  growingText: 'You have some foundations in place. Strengthen them with a regular learning routine.',
  deepening: 'Deepen what you know',
  deepeningText: 'You already have a good foundation. Continue with focused study and consistent practice.',
  focus: 'Your learning goals',
  time: 'Time you can set aside',
  finish: 'Go to my dashboard',
  chatbot: 'Open learning assistant',
  chatbotMessage: 'The learning assistant is not connected yet.',
  questions: [
    { title: 'What is your background in Islam?', hint: 'Choose what best describes you right now.', options: ['I recently embraced Islam', 'I have been Muslim since birth, but have not learned much yet', 'I have studied before and want to revisit the basics', 'I want to deepen what I already know'] },
    { title: 'How are you doing with your prayers?', options: ['I have not started praying yet', 'I am learning how to pray', 'I pray, but have not memorized the recitations yet', 'I pray all five prayers regularly'] },
    { title: 'How familiar are you with the Qur’an?', options: ['I do not know the Arabic letters yet', 'I can read, but still slowly', 'I can read and have memorized a few short surahs', 'I read fluently and regularly'] },
    { title: 'What are your main learning goals?', hint: 'You can choose more than one.', multiple: true, options: ['Understand the foundations of Islam', 'Learn to pray correctly', 'Understand Qur’an recitation', 'Improve my character', 'Learn basic Arabic', 'Become more consistent in worship'] },
    { title: 'How much time can you set aside to learn?', options: ['Whenever I have a little time', '15–30 minutes a day', 'An hour or more a day', 'An intensive period over a few weeks'] },
  ],
} : {
  title: 'Kuis Penempatan Belajar',
  question: 'PERTANYAAN',
  of: 'dari',
  back: 'Kembali',
  next: 'Lanjut',
  result: 'Lihat Hasil',
  skip: 'Ingin lewati kuis?',
  skipLink: 'Langsung ke kelas saya',
  chooseMany: 'Boleh pilih lebih dari satu.',
  selectOne: 'Pilih satu jawaban untuk melanjutkan.',
  resultTitle: 'Titik awal belajarmu',
  resultIntro: 'Berdasarkan jawabanmu, ini titik awal belajar yang bisa kamu coba.',
  foundation: 'Bangun fondasi belajar',
  foundationText: 'Mulai dari hal-hal mendasar dan pelajari setiap topik dengan ritme yang nyaman.',
  growing: 'Terus bertumbuh dengan konsisten',
  growingText: 'Kamu sudah punya sebagian fondasi. Perkuat dengan rutinitas belajar yang teratur.',
  deepening: 'Perdalam ilmu yang sudah dimiliki',
  deepeningText: 'Fondasi belajarmu sudah baik. Lanjutkan dengan materi yang lebih terarah dan latihan rutin.',
  focus: 'Tujuan belajarmu',
  time: 'Waktu belajar yang tersedia',
  finish: 'Lanjut ke dashboard',
  chatbot: 'Buka asisten belajar',
  chatbotMessage: 'Asisten belajar belum disambungkan.',
  questions: [
    { title: 'Bagaimana latar belakang Islam kamu?', hint: 'Pilih yang paling menggambarkan kondisimu saat ini.', options: ['Saya mualaf / baru masuk Islam', 'Muslim sejak lahir, tapi belum banyak belajar', 'Sudah belajar tapi ingin mengulang dari dasar', 'Ingin memperdalam ilmu yang sudah ada'] },
    { title: 'Bagaimana dengan sholatmu saat ini?', options: ['Belum sholat sama sekali', 'Sedang belajar tata cara sholat', 'Sudah sholat tapi belum hafal bacaannya', 'Sudah sholat 5 waktu dengan rutin'] },
    { title: 'Seberapa jauh perkenalanmu dengan Al-Qur’an?', options: ['Belum mengenal huruf hijaiyah', 'Bisa baca, tapi masih terbata-bata', 'Bisa baca dan hafal beberapa surat pendek', 'Bisa baca lancar dan rutin membaca'] },
    { title: 'Apa tujuan utama belajarmu di sini?', hint: 'Boleh pilih lebih dari satu.', multiple: true, options: ['Memahami dasar-dasar Islam', 'Belajar sholat dengan benar', 'Memahami bacaan Al-Qur’an', 'Memperbaiki akhlak dan karakter', 'Belajar bahasa Arab dasar', 'Konsisten beribadah (istiqomah)'] },
    { title: 'Berapa waktu yang bisa kamu luangkan untuk belajar?', options: ['Sesekali kalau ada waktu', '15–30 menit per hari', '1 jam atau lebih per hari', 'Belajar intensif selama beberapa minggu'] },
  ],
})

const current = computed(() => copy.value.questions[index.value])
const progress = computed(() => ((index.value + 1) / copy.value.questions.length) * 100)
const selectedGoals = computed(() => (answers.value[3] || []).map((choice) => copy.value.questions[3].options[choice]).filter(Boolean))
const timeAnswer = computed(() => copy.value.questions[4].options[answers.value[4]] || '')
const score = computed(() => {
  const [background, prayer, quran] = answers.value
  if (background === null || prayer === null || quran === null) return 0
  return [ [0, 1, 1, 2][background], [0, 0, 1, 2][prayer], [0, 1, 2, 3][quran] ].reduce((sum, value) => sum + value, 0)
})
const recommendation = computed(() => {
  if (score.value <= 2) return { title: copy.value.foundation, text: copy.value.foundationText }
  if (score.value <= 5) return { title: copy.value.growing, text: copy.value.growingText }
  return { title: copy.value.deepening, text: copy.value.deepeningText }
})

function isSelected(optionIndex) {
  return current.value.multiple
    ? answers.value[index.value].includes(optionIndex)
    : answers.value[index.value] === optionIndex
}

function choose(optionIndex) {
  if (current.value.multiple) {
    const selected = answers.value[index.value]
    answers.value[index.value] = selected.includes(optionIndex)
      ? selected.filter((value) => value !== optionIndex)
      : [...selected, optionIndex]
    return
  }
  answers.value[index.value] = optionIndex
}

function goBack() {
  if (showingResult.value) {
    showingResult.value = false
    return
  }
  if (index.value > 0) index.value -= 1
}

function continueQuiz() {
  if (answers.value[index.value] === null || (current.value.multiple && !answers.value[index.value].length)) return
  if (index.value < copy.value.questions.length - 1) {
    index.value += 1
  } else {
    showingResult.value = true
  }
}

function goToDashboard() {
  localStorage.removeItem(storageKey)
  router.push('/dashboard')
}

function openAssistant() {
  window.alert(copy.value.chatbotMessage)
}
</script>

<template>
  <main class="placement-page">
    <header class="placement-header">
      <RouterLink class="placement-logo" to="/" aria-label="StartMuslim">
        <img :src="logo" alt="StartMuslim" />
      </RouterLink>
      <div class="placement-languages" role="group" aria-label="Bahasa">
        <button :class="{ active: lang.code === 'id' }" @click="setLang('id')">ID</button>
        <button :class="{ active: lang.code === 'en' }" @click="setLang('en')">EN</button>
      </div>
      <span class="placement-header-title">{{ copy.title }}</span>
    </header>

    <section class="placement-content" :aria-label="copy.title">
      <div v-if="!showingResult" class="placement-progress" aria-live="polite">
        <div class="placement-progress-label">
          <span>{{ copy.question }} {{ index + 1 }} {{ copy.of }} {{ copy.questions.length }}</span>
          <span>{{ Math.round(progress) }}%</span>
        </div>
        <div class="placement-progress-track" role="progressbar" :aria-valuenow="progress" aria-valuemin="0" aria-valuemax="100">
          <span :style="{ width: `${progress}%` }"></span>
        </div>
      </div>

      <article v-if="!showingResult" class="placement-card">
        <p class="placement-eyebrow"><Sparkles :size="15" /> {{ copy.question }} {{ index + 1 }}</p>
        <h1>{{ current.title }}</h1>
        <p v-if="current.hint" class="placement-hint">{{ current.hint }}</p>
        <div class="placement-options" role="group" :aria-label="current.title">
          <button
            v-for="(option, optionIndex) in current.options"
            :key="option"
            type="button"
            class="placement-option"
            :class="{ selected: isSelected(optionIndex) }"
            :aria-pressed="isSelected(optionIndex)"
            @click="choose(optionIndex)"
          >
            <span class="placement-choice-mark"><Check v-if="isSelected(optionIndex)" :size="14" /></span>
            <span>{{ option }}</span>
          </button>
        </div>
      </article>

      <article v-else class="placement-card placement-result" aria-live="polite">
        <p class="placement-eyebrow"><Sparkles :size="15" /> {{ copy.resultTitle }}</p>
        <h1>{{ recommendation.title }}</h1>
        <p class="placement-hint">{{ copy.resultIntro }}</p>
        <p class="placement-result-text">{{ recommendation.text }}</p>
        <div v-if="selectedGoals.length" class="placement-summary">
          <h2>{{ copy.focus }}</h2>
          <ul><li v-for="goal in selectedGoals" :key="goal">{{ goal }}</li></ul>
        </div>
        <div class="placement-summary">
          <h2>{{ copy.time }}</h2>
          <p>{{ timeAnswer }}</p>
        </div>
      </article>

      <div class="placement-actions">
        <button class="placement-back" type="button" :disabled="index === 0 && !showingResult" @click="goBack">
          <ChevronLeft :size="16" /> {{ copy.back }}
        </button>
        <button v-if="showingResult" class="placement-next" type="button" @click="goToDashboard">
          {{ copy.finish }} <ChevronRight :size="16" />
        </button>
        <button v-else class="placement-next" type="button" :disabled="answers[index] === null || (current.multiple && !answers[index].length)" @click="continueQuiz">
          {{ index === copy.questions.length - 1 ? copy.result : copy.next }} <ChevronRight :size="16" />
        </button>
      </div>
      <p class="placement-skip">
        {{ copy.skip }} <button type="button" @click="goToDashboard">{{ copy.skipLink }}</button>
      </p>
    </section>

    <button class="placement-assistant" type="button" :aria-label="copy.chatbot" :title="copy.chatbot" @click="openAssistant">
      <Bot :size="20" />
    </button>
  </main>
</template>

<style scoped>
.placement-page {
  --quiz-green: #075c38;
  --quiz-ink: #153c2d;
  --quiz-gold: #e6a31a;
  --quiz-mint: #c7e5d6;
  min-height: 100svh;
  color: var(--quiz-ink);
  background:
    repeating-linear-gradient(135deg, rgba(15, 61, 46, 0.012) 0 1px, transparent 1px 7px),
    linear-gradient(160deg, #fbf8f1 0%, #f5f3ec 52%, #fbf8f1 100%);
  font-family: var(--font-body);
}
.placement-header {
  min-height: 3.8rem;
  padding: 0.55rem max(1.25rem, calc((100vw - 42rem) / 2));
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid #d9e6d9;
}
.placement-logo { justify-self: start; display: inline-flex; align-items: center; }
.placement-logo img { display: block; width: 6.4rem; height: auto; }
.placement-languages {
  display: inline-flex;
  align-items: center;
  gap: 0.12rem;
  padding: 0.15rem;
  border: 1px solid #c9dfd0;
  border-radius: 999px;
}
.placement-languages button {
  min-width: 1.55rem;
  min-height: 1.45rem;
  padding: 0 0.4rem;
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: #527466;
  font: 600 0.68rem var(--font-body);
  cursor: pointer;
}
.placement-languages button.active { background: var(--quiz-green); color: white; }
.placement-header-title { justify-self: end; font-size: 0.72rem; font-weight: 600; color: #496759; text-align: right; }
.placement-content { width: min(100% - 2rem, 26.4rem); margin: 1.6rem auto 3rem; }
.placement-progress { margin-bottom: 1.35rem; }
.placement-progress-label { display: flex; justify-content: space-between; gap: 1rem; margin-bottom: 0.3rem; font-size: 0.68rem; color: #52695f; }
.placement-progress-track { height: 4px; overflow: hidden; border-radius: 99px; background: #c8e5d7; }
.placement-progress-track span { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, #006338, #63a34e 60%, var(--quiz-gold)); transition: width 220ms ease; }
.placement-card {
  padding: 1.55rem 1.7rem 1.65rem;
  border: 1px solid #c6e2d3;
  border-radius: 1.35rem;
  background: rgba(251, 248, 241, 0.9);
  box-shadow: 0 1px 2px rgba(16, 66, 45, 0.12);
  animation: quiz-enter 260ms ease both;
}
@keyframes quiz-enter { from { opacity: 0; transform: translateY(7px); } to { opacity: 1; transform: translateY(0); } }
.placement-eyebrow { display: flex; align-items: center; gap: 0.45rem; margin-bottom: 0.55rem; color: #d98200; font-size: 0.66rem; font-weight: 800; letter-spacing: 0.05em; }
.placement-card h1 { margin: 0; color: #073f2b; font: 700 1.48rem/1.26 var(--font-display); letter-spacing: 0; }
.placement-hint { margin-top: 0.35rem; color: #64766e; font-size: 0.72rem; line-height: 1.5; }
.placement-options { display: grid; gap: 0.48rem; margin-top: 1.15rem; }
.placement-option {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  width: 100%;
  min-height: 2.42rem;
  padding: 0.45rem 0.72rem;
  border: 1px solid #c6e2d3;
  border-radius: 999px;
  background: transparent;
  color: #152d24;
  text-align: left;
  font: 500 0.72rem/1.4 var(--font-body);
  cursor: pointer;
  transition: border-color 150ms ease, background 150ms ease, transform 150ms ease;
}
.placement-option:hover { border-color: #6cae88; transform: translateY(-1px); }
.placement-option.selected { border-color: #16804e; background: #eaf4eb; }
.placement-choice-mark { flex: 0 0 0.9rem; width: 0.9rem; height: 0.9rem; display: grid; place-items: center; border: 1px solid #b8c8bd; border-radius: 50%; color: white; }
.selected .placement-choice-mark { border-color: #087342; background: #087342; }
.placement-actions { display: flex; justify-content: space-between; align-items: center; gap: 1rem; margin: 1.25rem 0 0; }
.placement-back, .placement-next { display: inline-flex; align-items: center; justify-content: center; gap: 0.3rem; min-height: 2.45rem; border: 0; font: 700 0.76rem var(--font-body); cursor: pointer; }
.placement-back { padding: 0 0.6rem; background: transparent; color: #102c20; }
.placement-back:disabled { color: #9ba49d; cursor: default; }
.placement-next { max-width: 70%; padding: 0.55rem 1.05rem; border-radius: 999px; background: linear-gradient(105deg, #7eae92, #98c3a0 65%, #eac66a); color: white; box-shadow: 0 4px 12px rgba(39, 89, 60, 0.12); }
.placement-next:disabled { opacity: 0.5; cursor: not-allowed; }
.placement-skip { margin: 0.85rem auto 0; text-align: center; color: #75877d; font-size: 0.65rem; }
.placement-skip button { padding: 0; border: 0; background: none; color: #00633a; font: inherit; font-weight: 700; cursor: pointer; }
.placement-result { padding-bottom: 1.5rem; }
.placement-result-text { margin-top: 0.8rem; color: #405b4d; font-size: 0.82rem; }
.placement-summary { margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid #dce9df; }
.placement-summary h2 { margin: 0 0 0.35rem; color: #315d46; font: 700 0.7rem var(--font-body); }
.placement-summary p, .placement-summary li { color: #4f685b; font-size: 0.72rem; line-height: 1.5; }
.placement-summary ul { display: grid; gap: 0.2rem; padding-left: 1.1rem; }
.placement-assistant { position: fixed; right: 1.25rem; bottom: 1.25rem; display: grid; place-items: center; width: 2.8rem; aspect-ratio: 1; border: 0; border-radius: 50%; background: #00683d; color: white; box-shadow: 0 5px 15px #123c2b30; cursor: pointer; }
@media (max-width: 560px) {
  .placement-header { min-height: 3.5rem; padding-inline: 0.9rem; grid-template-columns: 1fr auto; gap: 0.55rem; }
  .placement-logo img { width: 5.8rem; }
  .placement-header-title { display: none; }
  .placement-content { width: min(100% - 1.25rem, 26.4rem); margin-top: 1.25rem; }
  .placement-card { padding: 1.25rem 1rem 1.3rem; border-radius: 1.1rem; }
  .placement-card h1 { font-size: 1.34rem; }
  .placement-option { min-height: 2.65rem; font-size: 0.74rem; }
  .placement-actions { margin-top: 1rem; }
  .placement-assistant { right: 0.8rem; bottom: 0.8rem; }
}
</style>