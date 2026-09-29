<script setup>
import { BookOpen, Route, BarChart3, CircleHelp, Files, Clock, LayoutGrid, ClipboardCheck, Award,
  GraduationCap, Users, FileText, Bell, PlayCircle, Headphones, User, UserPlus, Laptop, Globe, ArrowRight,
  ChevronDown, ChevronLeft, ChevronRight, Quote } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { content, contentEn } from '../data/content.js'
import { lang } from '../i18n'
import NavBar from '../components/NavBar.vue'
import logo from '../assets/logo.png'
import mosqueInterior from '../assets/mosque-interior.jpg'
import muslim from '../assets/muslim.jpg'
import belajar from '../assets/belajar.jpg'
import primaryPhoto from '../assets/primary.jpg'
import studentPhoto from '../assets/student.jpg'
import contributorPhoto from '../assets/contributor.jpg'
import lampu from '../assets/lampu.png'
const c = computed(() => lang.code === 'en' ? contentEn : content)
const audiencePhotos = [primaryPhoto, studentPhoto, contributorPhoto]
const featuredFlowSteps = computed(() => c.value.flow.steps.filter(
  ([iconName]) => iconName !== 'Route' && iconName !== 'ArrowRight',
))
const icons = { BookOpen, Route, BarChart3, CircleHelp, Files, Clock, LayoutGrid, ClipboardCheck, Award,
  GraduationCap, Users, FileText, Bell, PlayCircle, Headphones, User, UserPlus, Laptop, Globe, ArrowRight }

// TODO: sambungkan ke widget chatbot beneran (mis. Crisp/Tawk.to) kalau sudah dipilih
function openChat() {
  alert(lang.code === 'en'
    ? 'The chatbot is not connected yet.'
    : 'Chatbot belum disambungkan.')
}

const testimonialsId = [
  { quote: 'Learning Path memberi urutan yang jelas. Saya jadi tahu materi dasar mana yang perlu dipelajari lebih dulu.', name: 'Aisha R.', role: 'Student, Bandung' },
  { quote: 'Materi dan format audio membantu saya tetap belajar saat jadwal sedang padat.', name: 'Dinda M.', role: 'Student, Jakarta' },
  { quote: 'Progres belajar terlihat jelas. Setelah satu kelas selesai, saya lebih mudah menentukan langkah berikutnya.', name: 'Farhan A.', role: 'Student, Surabaya' },
  { quote: 'Kelas berdasarkan tema membuat saya lebih mudah memilih topik yang sedang ingin dipelajari.', name: 'Zahra N.', role: 'Student, Yogyakarta' },
  { quote: 'Pre-test dan post-test memberi gambaran bagian yang sudah saya pahami dan yang perlu diulang.', name: 'Rafiq H.', role: 'Student, Medan' },
  { quote: 'Contributor Area memberi ruang yang lebih teratur untuk menyiapkan materi pembelajaran.', name: 'Hana S.', role: 'Contributor, Depok' },
]
const testimonialsEn = [
  { quote: 'The Learning Path gives me a clear sequence. I know which foundational topics to study first.', name: 'Aisha R.', role: 'Student, Bandung' },
  { quote: 'The materials and audio format help me keep learning when my schedule gets busy.', name: 'Dinda M.', role: 'Student, Jakarta' },
  { quote: 'My progress is easy to see. After finishing a class, it is easier to choose what to learn next.', name: 'Farhan A.', role: 'Student, Surabaya' },
  { quote: 'Classes organized by topic make it easier to find what I want to learn about.', name: 'Zahra N.', role: 'Student, Yogyakarta' },
  { quote: 'The pre- and post-tests show me what I understand and what I may want to review.', name: 'Rafiq H.', role: 'Student, Medan' },
  { quote: 'The Contributor Area gives me a more organized space to prepare learning materials.', name: 'Hana S.', role: 'Contributor, Depok' },
]
const testimonials = computed(() => lang.code === 'en' ? testimonialsEn : testimonialsId)
const testimonialPage = ref(0)
const testimonialPages = computed(() => Array.from(
  { length: Math.ceil(testimonials.value.length / 3) },
  (_, pageIndex) => testimonials.value.slice(pageIndex * 3, pageIndex * 3 + 3),
))
const visibleTestimonials = computed(() => testimonialPages.value[testimonialPage.value] || [])
const testimonialPageKey = computed(() => `${lang.code}-${testimonialPage.value}`)
const testimonialDirection = ref(1)
const testimonialTransitionName = computed(() => testimonialDirection.value > 0
  ? 'testimonial-next'
  : 'testimonial-previous')

function showTestimonialPage(pageIndex, direction = pageIndex < testimonialPage.value ? -1 : 1) {
  const pageCount = testimonialPages.value.length
  testimonialDirection.value = direction
  testimonialPage.value = (pageIndex + pageCount) % pageCount
}

function previousTestimonials() {
  showTestimonialPage(testimonialPage.value - 1, -1)
}

function nextTestimonials() {
  showTestimonialPage(testimonialPage.value + 1, 1)
}

// Jawaban diambil dari fakta yang sudah ada di deck, bukan karangan baru.
const faqId = [
  { q: 'Apa itu StartMuslim?', a: 'StartMuslim adalah Islamic Learning Management System (LMS) yang dirancang untuk membantu Student belajar Islam dari dasar dengan cara yang terstruktur dan mudah dipahami. Di dalam platform ini, Student mengikuti kurikulum yang jelas, menapaki Learning Path bertahap, melihat evaluasi kemampuan, serta memantau progress belajar secara konsisten agar proses pembelajaran terasa lebih terarah, terukur, dan menyenangkan.' },
  { q: 'Siapa yang bisa menggunakan StartMuslim?', a: 'StartMuslim melayani Primary Student (mualaf & Muslim beginner), Student (pembelajar umum/self-paced), dan Contributor (kontributor materi Islamic Learning).' },
  { q: 'Apakah semua materi berbayar?', a: 'Tidak. StartMuslim menyediakan akses ke materi gratis dan materi berbayar dengan kualitas terkurasi.' },
  { q: 'Bagaimana cara kerja Learning Path?', a: 'Alurnya: Curriculum → Learning Path → Learn → Evaluate → Progress → Continue, sehingga Student tahu harus mulai dari mana, apa yang dipelajari, dan langkah berikutnya.' },
  { q: 'Apakah saya mendapat sertifikat setelah selesai belajar?', a: 'Ya, Student dapat memperoleh Sertifikat Hasil Belajar setelah menyelesaikan kelas sesuai ketentuan yang berlaku pada kelas tersebut.' },
  { q: 'Bisakah saya belajar kapan saja?', a: 'Bisa. StartMuslim mendukung kelas live streaming, video on demand, dan pembelajaran audio, jadi bisa diakses sesuai waktu dan ritme masing-masing.' },
  { q: 'Bagaimana jika saya ingin menjadi pengajar/kontributor?', a: 'StartMuslim menyediakan Contributor Area, ruang khusus untuk para pengajar dan kontributor berkontribusi pada materi pembelajaran.' },
  { q: 'Apakah StartMuslim tersedia di luar Indonesia?', a: 'Fokus dua tahun awal StartMuslim adalah Indonesia. Ekspansi ke selected Arab markets adalah visi berikutnya setelah proses validasi dan lokalisasi.' },
]
const faqEn = [
  { q: 'What is StartMuslim?', a: 'StartMuslim is an Islamic Learning Management System (LMS) designed to help students learn Islam from the basics in a structured and easy-to-follow way. Within the platform, students follow a clear curriculum, progress through a step-by-step Learning Path, complete evaluations, and track their learning progress consistently so the journey feels more focused, measurable, and motivating.' },
  { q: 'Who can use StartMuslim?', a: 'StartMuslim serves Primary Students (new Muslims and Muslim beginners), Students (general or self-paced learners), and Contributors (Islamic learning content contributors).' },
  { q: 'Are all learning materials paid?', a: 'No. StartMuslim offers access to both free and paid materials, with curated quality.' },
  { q: 'How does the Learning Path work?', a: 'The journey is Curriculum → Learning Path → Learn → Evaluate → Progress → Continue, so students know where to start, what to learn, and what comes next.' },
  { q: 'Will I receive a certificate after completing a class?', a: 'Students may receive a Certificate of Learning after completing a class, subject to that class’s requirements.' },
  { q: 'Can I learn anytime?', a: 'Yes. StartMuslim supports live streaming, video on demand, and audio learning, so you can learn on your own schedule and at your own pace.' },
  { q: 'How can I become a teacher or contributor?', a: 'StartMuslim provides a Contributor Area, a dedicated space for teachers and contributors to contribute learning materials.' },
  { q: 'Is StartMuslim available outside Indonesia?', a: 'StartMuslim’s focus for its first two years is Indonesia. Expansion to selected Arab markets is a future vision after validation and localization.' },
]
const faq = computed(() => lang.code === 'en' ? faqEn : faqId)
const labels = computed(() => lang.code === 'en' ? {
  testimonials: 'What People Say',
  testimonialsLead: 'Testimonials from StartMuslim students and contributors.',
  testimonialNavigation: 'Testimonial pages',
  previousTestimonials: 'Previous testimonials',
  nextTestimonials: 'Next testimonials',
  testimonialPage: 'Show testimonial page',
  faq: 'Frequently Asked Questions',
  learn: 'Learn',
  continue: 'Continue',
  startToday: 'Take your first step today',
  footerDescription: 'An online Islamic learning platform designed especially for beginners and new Muslims. Start your learning journey today.',
  navigation: 'Navigation',
  home: 'Home',
  classes: 'Classes',
  learningPath: 'Learning Path',
  contributors: 'Contributors',
  about: 'About Us',
  contact: 'Contact',
  privacy: 'Privacy Policy',
  terms: 'Terms & Conditions',
  openChat: 'Open chatbot',
  chatbot: 'Chatbot',
  whatsapp: 'Contact us on WhatsApp',
} : {
  testimonials: 'Apa Kata Mereka',
  testimonialsLead: 'Testimoni dari Student dan Contributor StartMuslim.',
  testimonialNavigation: 'Halaman testimoni',
  previousTestimonials: 'Testimoni sebelumnya',
  nextTestimonials: 'Testimoni berikutnya',
  testimonialPage: 'Tampilkan halaman testimoni',
  faq: 'Pertanyaan yang Sering Diajukan',
  learn: 'Belajar',
  continue: 'Lanjut',
  startToday: 'Mulai langkah pertamamu hari ini',
  footerDescription: 'Platform belajar Islam online yang dirancang khusus untuk pemula dan mualaf. Mulai perjalanan belajarmu hari ini.',
  navigation: 'Navigasi',
  home: 'Beranda',
  classes: 'Kelas',
  learningPath: 'Jalur Belajar',
  contributors: 'Kontributor',
  about: 'Tentang Kami',
  contact: 'Kontak',
  privacy: 'Kebijakan Privasi',
  terms: 'Syarat & Ketentuan',
  openChat: 'Buka chatbot',
  chatbot: 'Chatbot',
  whatsapp: 'Hubungi via WhatsApp',
})
</script>

<template>
  <NavBar />
  <main class="landing-page">
    <section id="about" class="hero-wrap">

      <section class="hero wrap">
        <div class="hero-copy">
          <p class="tag">{{ c.hero.tag }}</p>
          <h1>{{ c.hero.title[0] }}<em>{{ c.hero.title[1] }}</em>{{ c.hero.title[2] }}</h1>
          <p class="lead">{{ c.hero.description }}</p>
          <ul class="hero-benefits">
            <li v-for="benefit in c.hero.benefits" :key="benefit[1]">
              <span class="hero-benefit-icon"><component :is="icons[benefit[0]]" :size="23" aria-hidden="true" /></span>
              <span>{{ benefit[1] }}</span>
            </li>
          </ul>
        </div>
        <div class="arch">
          <img class="arch-image" :src="mosqueInterior" :alt="lang.code === 'en' ? 'An ornate mosque interior with arches' : 'Interior masjid dengan lengkungan arsitektur Islam'" />
        </div>
      </section>
    </section>

    <section class="sec wrap problem-section">
      <div class="problem-layout">
        <div class="problem-intro">
          <h2 class="problem-heading">{{ c.problems.title }}</h2>
          <div class="problem-visual">
            <img :src="muslim" :alt="lang.code === 'en' ? 'A Muslim woman studying on a laptop' : 'Seorang Muslimah sedang belajar menggunakan laptop'" />
          </div>
        </div>
        <div class="problem-list">
          <article v-for="i in c.problems.items" :key="i[1]" class="card row hover-fill-card" tabindex="0">
            <span class="ic"><component :is="icons[i[0]]" :size="26" /></span><div><h3>{{ i[1] }}</h3><p>{{ i[2] }}</p></div>
          </article>
        </div>
      </div>
    </section>

    <section id="flow" class="sec tint flow-section">
      <div class="wrap flow-layout">
        <div class="flow-copy">
          <h2>{{ c.flow.title }}</h2>
          <p class="flow-description">{{ c.flow.text }}</p>
          <ul class="outcomes">
            <li v-for="o in c.flow.outcomes" :key="o">{{ o }}</li>
          </ul>
        </div>
        <div class="flow-visual">
          <img :src="belajar" :alt="lang.code === 'en' ? 'Students learning together' : 'Para pelajar sedang belajar bersama'" />
          <ol class="flow-steps">
            <li v-for="s in featuredFlowSteps" :key="s[1]">
              <span class="flow-step-icon"><component :is="icons[s[0]]" :size="24" aria-hidden="true" /></span>
              <span>{{ s[1] }}</span>
            </li>
          </ol>
        </div>
      </div>
    </section>

    <section class="sec wrap">
      <h2>{{ c.features.title }}</h2>
      <div class="grid g3">
        <article v-for="i in c.features.items" :key="i[1]" class="card feature-card hover-fill-card" tabindex="0">
          <span class="ic"><component :is="icons[i[0]]" :size="26" /></span><h3>{{ i[1] }}</h3><p>{{ i[2] }}</p>
        </article>
      </div>
    </section>

    <section class="sec tint"><div class="wrap">
      <h2>{{ c.audience.title }}</h2><p class="narrow">{{ c.audience.text }}</p>
      <div class="grid g3">
        <article v-for="(i, index) in c.audience.items" :key="i[1]" class="card audience-card">
          <img class="audience-photo" :src="audiencePhotos[index]" alt="" />
          <div class="audience-copy">
            <h3>{{ i[1] }}</h3><strong>{{ i[2] }}</strong><p>{{ i[3] }}</p>
          </div>
        </article>
      </div>
    </div></section>

    <section class="sec wrap different-section">
      <div class="different-grid">
        <div class="different-intro">
          <h2>{{ c.different.title }}</h2>
          <p>{{ c.different.text }}</p>
        </div>
        <article v-for="i in c.different.items" :key="i[1]" class="card different-card hover-fill-card" tabindex="0">
          <span class="ic"><component :is="icons[i[0]]" :size="26" /></span>
          <h3>{{ i[1] }}</h3>
          <p>{{ i[2] }}</p>
        </article>
      </div>
    </section>

    <section id="testimoni" class="sec tint testimonial-section">
      <div class="wrap">
        <header class="testimonial-heading">
          <h2>{{ labels.testimonials }}</h2>
          <p>{{ labels.testimonialsLead }}</p>
        </header>
        <Transition :name="testimonialTransitionName" mode="out-in">
          <div :key="testimonialPageKey" class="grid g3 testimonial-grid">
            <article v-for="t in visibleTestimonials" :key="t.name" class="card testimonial">
              <Quote class="testimonial-quote-icon" :size="26" :stroke-width="2.5" aria-hidden="true" />
              <p class="testimonial-quote">{{ t.quote }}</p>
              <div class="testimonial-author">
                <span class="testimonial-avatar"><User :size="22" aria-hidden="true" /></span>
                <div class="testimonial-author-copy">
                  <strong>{{ t.name }}</strong>
                  <span>{{ t.role }}</span>
                </div>
              </div>
            </article>
          </div>
        </Transition>
        <nav class="testimonial-controls" :aria-label="labels.testimonialNavigation">
          <button
            type="button"
            class="testimonial-control"
            :aria-label="labels.previousTestimonials"
            :title="labels.previousTestimonials"
            @click="previousTestimonials"
          >
            <ChevronLeft :size="18" aria-hidden="true" />
          </button>
          <div class="testimonial-dots">
            <button
              v-for="(_, pageIndex) in testimonialPages"
              :key="pageIndex"
              type="button"
              class="testimonial-dot"
              :class="{ active: testimonialPage === pageIndex }"
              :aria-label="`${labels.testimonialPage} ${pageIndex + 1}`"
              :aria-pressed="testimonialPage === pageIndex"
              @click="showTestimonialPage(pageIndex)"
            ></button>
          </div>
          <button
            type="button"
            class="testimonial-control"
            :aria-label="labels.nextTestimonials"
            :title="labels.nextTestimonials"
            @click="nextTestimonials"
          >
            <ChevronRight :size="18" aria-hidden="true" />
          </button>
        </nav>
      </div>
    </section>

    <section id="faq" class="sec wrap faq-section">
      <h2 class="faq-heading">{{ labels.faq }}</h2>
      <div class="faq-list">
        <details v-for="(item, i) in faq" :key="i" class="faq-item">
          <summary>{{ item.q }}<ChevronDown class="faq-chevron" :size="18" /></summary>
          <div class="faq-answer"><p>{{ item.a }}</p></div>
        </details>
      </div>
    </section>

    <section class="sec cta">
      <img class="cta-lamp" :src="lampu" alt="" aria-hidden="true" />
      <div class="wrap two">
      <div>
        <h2>{{ c.hero.title.join('') }}</h2>
        <p>{{ c.hero.sub }}</p><p>{{ c.cta.text }}</p>
        <p class="quote">{{ c.cta.quote }}</p>
      </div>
      <div class="cta-side">
        <ul class="steps3"><li><span class="ic"><BookOpen :size="24" /></span>{{ labels.learn }}</li><li><span class="ic"><BarChart3 :size="24" /></span>Progress</li><li><span class="ic"><Route :size="24" /></span>{{ labels.learningPath }}</li></ul>
        <a class="btn gold" href="https://startmuslim.com"><Globe :size="18" /> startmuslim.com <ArrowRight :size="18" /></a>
        <p class="hint">{{ labels.startToday }}</p>
      </div>
      </div>
    </section>
  </main>
    <footer class="site-footer">
    <div class="footer-main">
      <div class="footer-brand">
        <RouterLink to="/" class="footer-logo">
          <img :src="logo" alt="StartMuslim" />
        </RouterLink>
        <p>{{ labels.footerDescription }}</p>
      </div>

      <div class="footer-col">
        <h4>{{ labels.navigation }}</h4>
                <nav>
          <RouterLink to="/">{{ labels.home }}</RouterLink>
          <a href="#">{{ labels.classes }}</a>
          <a href="/#flow">{{ labels.learningPath }}</a>
          <a href="#">{{ labels.contributors }}</a>
          <a href="/#testimoni">{{ lang.code === 'en' ? 'Testimonials' : 'Testimoni' }}</a>
          <a href="/#faq">FAQ</a>
          <a href="/#about">{{ labels.about }}</a>
        </nav>
      </div>

      <div class="footer-col">
        <h4>{{ labels.contact }}</h4>
        <a class="footer-contact" href="mailto:info@startmuslim.com">
          <span class="fc-ic">✉</span>
          info@startmuslim.com
        </a>
        <a
          class="footer-contact"
          href="https://wa.me/6281234567890"
          target="_blank"
          rel="noopener"
        >
          <span class="fc-ic wa">wa</span>
          +62 812 3456 7890
        </a>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="footer-bottom-inner">
        <p>© 2026 StartMuslim. All rights reserved.</p>
        <div class="footer-legal">
          <a href="#">{{ labels.privacy }}</a>
          <a href="#">{{ labels.terms }}</a>
        </div>
      </div>
    </div>
  </footer>
      <!-- Floating actions: chatbot + WhatsApp -->
  <div class="float-actions">
    <!-- Chatbot — ganti href/# dengan link chatbot kamu nanti -->
    <button
      type="button"
      class="float-btn float-chat"
      :aria-label="labels.openChat"
      :title="labels.chatbot"
      @click="openChat"
    >
      <!-- ikon chat sederhana -->
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M4 6a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H9l-4 3v-3a3 3 0 0 1-1-2.2V6z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
        <circle cx="9" cy="10" r="1" fill="currentColor"/>
        <circle cx="12" cy="10" r="1" fill="currentColor"/>
        <circle cx="15" cy="10" r="1" fill="currentColor"/>
      </svg>
    </button>

    <a
      class="float-btn float-wa"
      href="https://wa.me/6281234567890"
      target="_blank"
      rel="noopener"
      :aria-label="labels.whatsapp"
      title="WhatsApp"
    >
      <!-- logo WhatsApp -->
      <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <path d="M17.47 14.38c-.3-.15-1.77-.87-2.04-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.95 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.8-1.49-1.78-1.66-2.08-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.87 1.22 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.63.71.23 1.36.2 1.87.12.57-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35z"/>
        <path d="M12.04 2C6.5 2 2.02 6.48 2.02 12.02c0 1.77.46 3.45 1.28 4.92L2 22l5.2-1.36A9.96 9.96 0 0 0 12.04 22C17.58 22 22 17.52 22 11.98 22 6.48 17.58 2 12.04 2zm0 18.15c-1.58 0-3.05-.45-4.3-1.23l-.31-.18-3.09.81.83-3.01-.2-.33a8.1 8.1 0 0 1-1.25-4.34c0-4.5 3.66-8.15 8.17-8.15 4.5 0 8.15 3.65 8.15 8.15 0 4.51-3.65 8.15-8.15 8.15z"/>
      </svg>
    </a>
  </div>
</template>
